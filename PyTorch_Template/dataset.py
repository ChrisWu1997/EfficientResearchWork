from torch.utils.data import Dataset, DataLoader
import torch
import glob
import numpy as np
import os
import json
import h5py


def get_dataloader(phase, config):
    is_shuffle = phase == 'train'

    dataset = MyDataset(phase, config.data_root)
    dataloader = DataLoader(dataset, batch_size=config.batch_size, shuffle=is_shuffle, num_workers=config.num_workers,
                            worker_init_fn=np.random.seed())
    return dataloader


class MyDataset(Dataset):
    def __init__(self, phase, data_root):
        super(MyDataset, self).__init__()
        self.data_root = data_root
        self.aug = phase == "train"

    def __getitem__(self, index):
        pass

    def __len__(self):
        pass


def test():
    pass


if __name__ == "__main__":
    test()
