# Adding the function to only train based on the tree (without sequences)

#!/usr/bin/env python3
import time

import torch
import os
import math
import torch.nn as nn
from depp import submodule
from depp import data
from depp import utils
from pytorch_lightning.core.lightning import LightningModule
from torch.utils.data import DataLoader
from typing import List, Dict, Optional, Callable, Union
from torch.optim.optimizer import Optimizer
import numpy as np
import treeswift as ts
import math
import omegaconf


class encoder(nn.Module):
    def __init__(self, args):
        super(encoder, self).__init__()
        channel = 4

        self.conv = nn.Conv1d(channel, args.h_channel, 1)
        self.relu = nn.ReLU()
        self.celu = nn.CELU()
        resblocks = []
        for i in range(args.resblock_num):
            resblocks.append(submodule.resblock(args.h_channel,
                                                args.h_channel,
                                                5, 0.3))
        self.resblocks = nn.Sequential(*resblocks)

        self.linear = nn.Conv1d(args.h_channel,
                                args.embedding_size,
                                args.sequence_length)
        self.args = args
        self.train_loss = 0
        self.distance_ratio = nn.Parameter(torch.tensor([1.0]), requires_grad=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        bs, channel, seq_length = x.shape

        x = self.celu(self.conv(x))
        x = self.resblocks(x)
        x = self.linear(x).squeeze(-1)
        x = x.view(bs, -1)
        return x * self.distance_ratio.item()

class tree_leaves_encoder(nn.Module):
    def __init__(self, args, embedding_size, current_model):
        super(tree_leaves_encoder, self).__init__()
        if args.backbone_tree_file is None and args.backbone_seq_file is None:
            tree = ts.read_tree_newick(f"{args.seqdir}/{current_model}.fa")
        else:
            tree = ts.read_tree_newick(args.backbone_tree_file)
        self.tree_leaves_emb = nn.ParameterDict(
            {i.label: nn.Parameter(torch.rand(embedding_size) * 1e-3, requires_grad=True)
             for i in tree.traverse_leaves()})

    def forward(self, nodes):
        return torch.stack([self.tree_leaves_emb[s] for s in nodes], dim=0)


class classifier(nn.Module):
    def __init__(self, args, cluster_num=None):
        super(classifier, self).__init__()
        channel = 4

        self.conv = nn.Conv1d(channel, args.h_channel, 1)
        self.relu = nn.ReLU()
        self.celu = nn.CELU()
        resblocks = []
        for i in range(args.resblock_num):
            resblocks.append(submodule.resblock(args.h_channel,
                                                args.h_channel,
                                                5, 0.3))

        if args.classifier_seqdir is not None:
            seqdir = args.classifier_seqdir
        else:
            seqdir = args.seqdir
        if cluster_num is None:
            cluster_num = len([i for i in range(len(os.listdir(seqdir))) if os.path.isfile(f'{seqdir}/{i}.fa')])

        self.resblocks = nn.Sequential(*resblocks)

        self.linear = nn.Conv1d(args.h_channel,
                                cluster_num,
                                args.sequence_length)
        self.args = args
        self.train_loss = 0

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        bs, channel, seq_length = x.shape

        x = self.celu(self.conv(x))
        x = self.resblocks(x)
        x = self.linear(x).squeeze(-1)
        x = x.view(bs, -1)
        return x


class model(LightningModule):
    def __init__(self, args, current_model):
        super(model, self).__init__()
        self.save_hyperparameters(args)
        if not self.hparams.sequence_length:
            utils.get_seq_length(self.hparams)

        if current_model != -1:
            embedding_size = self.hparams.embedding_size
            self.hparams.embedding_size = embedding_size[current_model]
            self.encoder = encoder(self.hparams)
            self.hparams.embedding_size = embedding_size
            self.embedding_size = embedding_size[current_model]
        else:
            self.classifier = classifier(self.hparams)
        self.channel = 4
        # self.hparams.distance_ratio = math.sqrt(float(1.0 / 128 / 10 * float(self.hparams.distance_alpha)))

        self.dis_loss_w = 100
        self.train_loss = []
        self.val_loss = float('inf')

        self.testing = False
        if current_model == -1:
            self.training_classifier = True
        else:
            self.training_classifier = False
        self.current_model = current_model
        self.counting = 0

        self.save_hyperparameters(self.hparams)


    def get_distance_ratio(self):
        loader = DataLoader(self.train_data,
                            batch_size=self.hparams.batch_size,
                            num_workers=self.hparams.num_worker,
                            shuffle=True,
                            drop_last=True)
        with torch.no_grad():
            init_distance = []
            for batch_idx, batch in enumerate(loader):
                seq = batch['seqs'].float().to(self.device)
                model_idx = batch['cluster_idx'].long()
                encoding = self(seq, model_idx[0])
                distance = utils.distance(encoding, encoding.detach(),
                                          self.hparams.distance_mode)

                not_self = torch.ones_like(distance)
                not_self[torch.arange(0, len(distance)), torch.arange(0, len(distance))] = 0
                init_distance.append(distance[not_self == 1])
            init_distance = torch.cat(init_distance)
            mean_init_distance = init_distance.mean()
        mean_tree_distance = np.sqrt(self.train_data.distance_matrix.values).mean().mean()
        self.encoder.distance_ratio[:] = (mean_tree_distance / mean_init_distance).item()


    def forward(self, x, model_idx=None) -> torch.Tensor:
        if self.training_classifier:
            return self.classifier(x)
        return self.encoder(x)

    def train_tree_leave_emb(self):
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        tree_leaves_emb = tree_leaves_encoder(self.hparams,
                                              current_model=self.current_model,
                                              embedding_size=self.embedding_size).to(device)
        optimizer = torch.optim.Adam(tree_leaves_emb.parameters(), lr=0.05)
        leaves = np.array(list(tree_leaves_emb.tree_leaves_emb.keys()))
        np.random.shuffle(leaves)

        # Size of chunks (C)
        C = 32

        # Split the randomized array into chunks
        chunks = [leaves[i:i + C] for i in range(0, len(leaves), C)]

        running_loss = 0
        t = time.time()
        for epoch in range(201):
            for i, nodes in enumerate(chunks):
                encoding = tree_leaves_emb(nodes)
                gt_distance = self.train_data.true_distance(nodes, nodes).to(device)

                distance = utils.distance(encoding, encoding.detach(), self.hparams.distance_mode)

                not_self = torch.ones_like(distance)
                not_self[torch.arange(0, len(distance)), torch.arange(0, len(distance))] = 0
                dis_loss = utils.mse_loss(distance[not_self == 1], gt_distance[not_self == 1],
                                          'square_root_be')
                loss = dis_loss
                running_loss += loss.item()
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
            np.random.shuffle(leaves)
            chunks = [leaves[i:i + C] for i in range(0, len(leaves), C)]
            if epoch % 10 == 0:
                print("epoch: {}, loss: {:.2f}, time: {:.2f}".format(epoch, running_loss / len(chunks), time.time()-t))
                t = time.time()
                running_loss = 0
                for param_group in optimizer.param_groups:
                    param_group['lr'] = param_group['lr'] * 0.5 + 2e-5
        self.tree_leaves_emb = {k: tree_leaves_emb.tree_leaves_emb[k].detach() for k in tree_leaves_emb.tree_leaves_emb}
        tree_leaves_emb.requires_grad = False
        os.makedirs(f'{self.hparams.model_dir}/{self.current_model}', exist_ok=True)
        torch.save(self.tree_leaves_emb, f'{self.hparams.model_dir}/{self.current_model}/tree_emb.pt')

    def training_step(self, batch, batch_idx):

        if self.trainer.current_epoch == 0 and batch_idx == 0 and self.hparams.train_mode == 'all':
            self.train_tree_leave_emb()

        nodes = batch['nodes']
        seq = batch['seqs'].float()
        model_idx = batch['cluster_idx'].long()
        device = seq.device

        if self.training_classifier:
            c = self(seq)
            loss = nn.functional.cross_entropy(c, model_idx)
            self.val_loss += loss
            return {'loss': loss}
        else:

            encoding = self(seq, model_idx[0])
            gt_distance = self.train_data.true_distance(nodes, nodes).to(device)

            distance = utils.distance(encoding, encoding.detach(), self.hparams.distance_mode)

            not_self = torch.ones_like(distance)
            not_self[torch.arange(0, len(distance)), torch.arange(0, len(distance))] = 0

            if self.hparams.train_mode == 'partial':
                dis_loss = utils.mse_loss(distance[not_self == 1], gt_distance[not_self == 1],
                                          self.hparams.weighted_method)
                loss = self.dis_loss_w * dis_loss * self.hparams.dis_loss_ratio
            else:
                gt_emb = torch.stack([self.tree_leaves_emb[s] for s in nodes], dim=0).detach()
                loss = torch.nn.functional.mse_loss(encoding, gt_emb)

            if loss.isnan().any():
                breakpoint()

            self.val_loss += loss

            return {'loss': loss}

    def training_epoch_end(
            self,
            outputs: Union[List[Dict[str, torch.Tensor]], List[List[Dict[str, torch.Tensor]]]]
    ) -> Dict[str, Dict[str, torch.Tensor]]:
        self.dis_loss_w = 100 + 1e-3 * (self.trainer.current_epoch - 1e4) * (self.trainer.current_epoch > 1e4)
        self.counting += 1
        if self.trainer.current_epoch % 100 == 0:
            if self.training_classifier:
                subdir = 'classifier'
            else:
                subdir = self.current_model
            os.makedirs(f'{self.hparams.model_dir}/{subdir}', exist_ok=True)
            self.trainer.save_checkpoint(f'{self.hparams.model_dir}/{subdir}/epoch-{self.trainer.current_epoch}.pth')
            if self.trainer.current_epoch > 0:
                try:
                    os.remove(f'{self.hparams.model_dir}/{subdir}/epoch-{self.trainer.current_epoch - 100}.pth')
                except:
                    pass


    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=self.hparams.lr)

    def train_dataloader(self) -> DataLoader:
        # self.train_data = self.train_data_list[0]
        loader = DataLoader(self.train_data,
                            batch_size=self.hparams.batch_size,
                            num_workers=self.hparams.num_worker,
                            shuffle=True,
                            drop_last=True)

        if self.current_model != -1:
            self.get_distance_ratio()
            print(f'Distance ratio is {self.encoder.distance_ratio.item()}')

        return loader

    def validation_step(self, batch, batch_idx):
        return {}

    def validation_epoch_end(self, outputs):
        val_loss = self.val_loss
        self.val_loss = 0
        self.log('val_loss', val_loss)

    def val_dataloader(self):
        # TODO: do a real train/val split
        # self.train_data = data.data(self.hparams, calculate_distance_matrix=True)
        # self.train_data_list = data.make_datalist(self.hparams)
        if not self.training_classifier:
            print(f'training {self.current_model} model...')
            self.train_data = data.get_data(self.current_model, self.hparams)

        else:
            # self.train_data = self.train_data_list[-1]
            print(f'training classifier...')
            self.train_data = data.get_data(-1, self.hparams)
        loader = DataLoader(self.train_data,
                            batch_size=self.hparams.batch_size,
                            shuffle=False,
                            num_workers=self.hparams.num_worker,
                            drop_last=True)
        return loader

    def optimizer_step(
            self,
            epoch: int,
            batch_idx: int,
            optimizer: Optimizer,
            optimizer_idx: int,
            optimizer_closure: Optional[Callable] = None,
            on_tpu: bool = False,
            using_native_amp: bool = False,
            using_lbfgs: bool = False,
    ) -> None:

        if self.counting == self.hparams.lr_update_freq:
            # if (epoch + 1) % self.hparams.lr_decay == 0:
            # lr = 3e-5 + self.hparams.lr * (0.1 ** ((self.trainer.current_epoch + 1) / self.hparams.lr_decay))
            # print('lr', lr)
            for param_group in optimizer.param_groups:
                param_group['lr'] = param_group['lr'] * 0.1 + 2e-5
            print('lr', param_group['lr'])
            print(self.counting, self.hparams.lr_update_freq)
            self.counting = 0


        super(model, self).optimizer_step(
            epoch,
            batch_idx,
            optimizer,
            optimizer_idx,
            optimizer_closure,
            on_tpu,
            using_native_amp,
            using_lbfgs,
        )


