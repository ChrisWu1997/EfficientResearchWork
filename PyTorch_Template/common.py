import os
from utils import ensure_dirs
import argparse
import json
import shutil


def get_config(phase):
    config = Config(phase)
    return config


class Config(object):
    """Base class of Config, provide necessary hyperparameters. 
    """
    def __init__(self, phase):
        self.is_train = phase == "train"

        # init hyperparameters and parse from command-line
        parser, args = self.parse()

        # set as attributes
        print("----Experiment Configuration-----")
        for k, v in args.__dict__.items():
            print("{0:20}".format(k), v)
            self.__setattr__(k, v)

        # experiment paths
        self.exp_dir = os.path.join(self.proj_dir, self.exp_name)
        if phase == "train" and args.cont is not True and os.path.exists(self.exp_dir):
            response = input('Experiment log/model already exists, overwrite? (y/n) ')
            if response != 'y':
                exit()
            shutil.rmtree(self.exp_dir)

        self.log_dir = os.path.join(self.exp_dir, 'log')
        self.model_dir = os.path.join(self.exp_dir, 'model')
        ensure_dirs([self.log_dir, self.model_dir])

        # GPU usage
        if args.gpu_ids is not None:
            os.environ["CUDA_VISIBLE_DEVICES"] = str(args.gpu_ids)

        # create soft link to experiment log directory
        if not os.path.exists('train_log'):
            os.symlink(self.exp_dir, 'train_log')

        # save this configuration
        if self.is_train:
            with open('train_log/config.txt', 'w') as f:
                json.dump(args.__dict__, f, indent=2)

    def parse(self):
        """initiaize argument parser. Define default hyperparameters and collect from command-line arguments."""
        parser = argparse.ArgumentParser()
        
        # basic configuration
        self._add_basic_config_(parser)

        # dataset configuration
        self._add_dataset_config_(parser)

        # model configuration
        self._add_network_config_(parser)

        # training or testing configuration
        self._add_training_config_(parser)

        # additional parameters if needed
        pass

        args = parser.parse_args()
        return parser, args

    def _add_basic_config_(self, parser):
        """add general hyperparameters"""
        group = parser.add_argument_group('basic')
        group.add_argument('--proj_dir', type=str, default="your-proj-dir", help="path to project folder where models and logs will be saved")
        group.add_argument('--data_root', type=str, default="your-data-root", help="path to source data folder")
        group.add_argument('--exp_name', type=str, default=os.getcwd().split('/')[-1], help="name of this experiment")
        group.add_argument('-g', '--gpu_ids', type=str, default=None, help="gpu to use, e.g. 0  0,1,2. CPU not supported.")

    def _add_dataset_config_(self, parser):
        """add hyperparameters for dataset configuration"""
        group = parser.add_argument_group('dataset')
        group.add_argument('--batch_size', type=int, default=64, help="batch size")
        group.add_argument('--num_workers', type=int, default=8, help="number of workers for data loading")

    def _add_network_config_(self, parser):
        """add hyperparameters for network architecture"""
        group = parser.add_argument_group('network')
        # group.add_argument("--z_dim", type=int, default=128)
        pass

    def _add_training_config_(self, parser):
        """training configuration"""
        group = parser.add_argument_group('training')
        group.add_argument('--nr_epochs', type=int, default=1000, help="total number of epochs to train")
        group.add_argument('--lr', type=float, default=1e-3, help="initial learning rate")
        group.add_argument('--lr_step_size', type=int, default=400, help="step size for learning rate decay")
        group.add_argument('--continue', dest='cont',  action='store_true', help="continue training from checkpoint")
        group.add_argument('--ckpt', type=str, default='latest', required=False, help="desired checkpoint to restore")
        group.add_argument('--vis', action='store_true', default=False, help="visualize output in training")
        group.add_argument('--save_frequency', type=int, default=100, help="save models every x epochs")
        group.add_argument('--val_frequency', type=int, default=10, help="run validation every x iterations")
        group.add_argument('--vis_frequency', type=int, default=10, help="visualize output every x iterations")
