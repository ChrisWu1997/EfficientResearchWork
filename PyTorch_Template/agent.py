from utils import TrainClock
import os
import torch
import torch.optim as optim
import torch.nn as nn
from abc import abstractmethod
from tensorboardX import SummaryWriter
import numpy as np
from networks import get_network


def get_agent(config):
    return MyAgent(config)


class BaseAgent(object):
    """Base trainer that provides common training behavior.
        All customized trainer should be subclass of this class.
    """
    def __init__(self, config):
        self.log_dir = config.log_dir
        self.model_dir = config.model_dir
        self.clock = TrainClock()
        self.batch_size = config.batch_size

        # build network
        self.net = self.build_net(config)
        # print('-----network architecture-----')
        # print(self.net)

        # set loss function
        self.set_loss_function()

        # set optimizer and scheduler
        self.set_optimizer(config)
        self.set_scheduler(config)

        # set tensorboard writer
        self.train_tb = SummaryWriter(os.path.join(self.log_dir, 'train.events'))
        self.val_tb = SummaryWriter(os.path.join(self.log_dir, 'val.events'))

    @abstractmethod
    def build_net(self, config):
        raise NotImplementedError

    def set_loss_function(self):
        """set loss function used in training"""
        pass

    def set_optimizer(self, config):
        """set optimizer and lr scheduler used in training"""
        self.optimizer = optim.Adam(self.net.parameters(), config.lr)

    def set_scheduler(self, config):
        self.scheduler = None # optim.lr_scheduler.StepLR(self.optimizer, config.lr_step_size)

    def save_ckpt(self, name=None):
        """save checkpoint during training for future restore"""
        if name is None:
            save_path = os.path.join(self.model_dir, "ckpt_epoch{}.pth".format(self.clock.epoch))
            print("Saving checkpoint epoch {}...".format(self.clock.epoch))
        else:
            save_path = os.path.join(self.model_dir, "{}.pth".format(name))

        if isinstance(self.net, nn.DataParallel):
            model_state_dict = self.net.module.cpu().state_dict()
        else:
            model_state_dict = self.net.cpu().state_dict()

        torch.save({
            'clock': self.clock.make_checkpoint(),
            'model_state_dict': model_state_dict,
            'optimizer_state_dict': self.optimizer.state_dict(),
            'scheduler_state_dict': self.scheduler.state_dict() if self.scheduler is not None else None,
        }, save_path)

        self.net.cuda()

    def load_ckpt(self, name=None):
        """load checkpoint from saved checkpoint"""
        name = name if name == 'latest' else "ckpt_epoch{}".format(name)
        load_path = os.path.join(self.model_dir, "{}.pth".format(name))
        if not os.path.exists(load_path):
            raise ValueError("Checkpoint {} not exists.".format(load_path))

        checkpoint = torch.load(load_path)
        print("Loading checkpoint from {} ...".format(load_path))
        if isinstance(self.net, nn.DataParallel):
            self.net.module.load_state_dict(checkpoint['model_state_dict'])
        else:
            self.net.load_state_dict(checkpoint['model_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        if self.scheduler is not None:
            self.scheduler.load_state_dict(checkpoint['scheduler_state_dict'])
        self.clock.restore_checkpoint(checkpoint['clock'])

    @abstractmethod
    def forward(self, data):
        """forward logic for your network"""
        """should return network outputs, losses(dict)"""
        raise NotImplementedError

    def update_network(self, loss_dict):
        """update network by back propagation"""
        loss = sum(loss_dict.values())
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def update_learning_rate(self):
        """record and update learning rate"""
        self.train_tb.add_scalar('learning_rate', self.optimizer.param_groups[-1]['lr'], self.clock.epoch)
        if self.scheduler is not None:
            self.scheduler.step(self.clock.epoch)

    def record_losses(self, loss_dict, mode='train'):
        """record loss to tensorboard"""
        losses_values = {k: v.item() for k, v in loss_dict.items()}

        tb = self.train_tb if mode == 'train' else self.val_tb
        for k, v in losses_values.items():
            tb.add_scalar(k, v, self.clock.step)

    def train_func(self, data):
        """one step of training"""
        self.net.train()

        outputs, losses = self.forward(data)

        self.update_network(losses)
        self.record_losses(losses, 'train')

        return outputs, losses

    def val_func(self, data):
        """one step of validation"""
        self.net.eval()

        with torch.no_grad():
            outputs, losses = self.forward(data)

        self.record_losses(losses, 'validation')

        return outputs, losses

    def visualize_batch(self, data, tb, **kwargs):
        """write visualization results to tensorboard writer"""
        raise NotImplementedError


class MyAgent(BaseAgent):
    def build_net(self, config):
        # customize your build_net function
        # should return the built network
        net = get_network(config).cuda()
        return net

    def forward(self, data):
        # customize your forward function
        # should return the network outputs and losses

        # input_vox3d = data['vox3d'].cuda()
        # target_vox3d = input_vox3d.clone().detach()

        # output_vox3d = self.net(input_vox3d)

        # loss = self.criterion(output_vox3d, target_vox3d)
        # return output_vox3d, {"mse": loss}
        pass
