from torch.utils.data import Dataset, DataLoader
import torch
import glob
import numpy as np
import os
import json
import h5py

DATA_ROOT = ""

def get_dataloader(phase, batch_size=4, num_workers=4):
    is_shuffle = phase == 'train'

    dataset = MyDataset(phase)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=is_shuffle, num_workers=num_workers,
                            worker_init_fn=np.random.seed())
    return dataloader


class MyDataset(Dataset):
    def __init__(self, phase):
        super(MyDataset, self).__init__()
        self.data_root = DATA_ROOT
        self.aug = phase == "train"

    def __getitem__(self, index):
        pass

    def __len__(self):
        pass


def test():
    pass


if __name__ == "__main__":
    test()