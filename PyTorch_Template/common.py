import os
import utils
import torch
from abc import abstractmethod


def get_config(args):
    config = MyConfig()
    os.environ["CUDA_VISIBLE_DEVICES"] = str(args.gpu_ids)
    config.device = torch.device("cuda:0")
    return config


class Config(object):
    """Base class of Config, provide necessary hyperparameters. 
    """
    def __init__(self):
        # general
        self.device = None

        # experiment paths
        self.proj_dir = "some_path"
        self.exp_name = os.getcwd().split('/')[-1]
        self.exp_dir = os.path.join(self.proj_dir, self.exp_name)

        self.log_dir, self.model_dir = self.set_exp_paths()
        utils.ensure_dirs([self.log_dir, self.model_dir])

        # network configuration
        self.set_network_info()

        # training configuration
        self.nr_epochs = 1000
        self.batch_size = 64
        self.num_workers = 8
        self.lr = 1e-4
        self.lr_step_size = 400

        self.save_frequency = 100
        self.val_frequency = 100
        self.visualize_frequency = 100

        self.points_batch_size = None

    def __repr__(self):
        return "epochs: {}\nbatch size: {}\nlr: {}\nworkers: {}\ndevice: {}\n".format(
            self.nr_epochs, self.batch_size, self.lr, self.num_workers, self.device
        )

    def set_exp_paths(self):
        return os.path.join(self.exp_dir, 'log'), os.path.join(self.exp_dir, 'model')

    def set_network_info(self):
        raise NotImplementedError


class MyConfig(Config):
    def set_network_info(self):
        # customize your set_network_info function
        # should set hyperparameters for network architecture 

        # self.en_n_layers = 5
        # self.en_ef_dim = 32
        # self.en_df_dim = 32
        # self.en_z_dim = 128

        # self.de_n_layers = 6
        # self.de_f_dim = 128
        pass

