from torch.utils.data import Dataset, DataLoader
import numpy as np


def get_dataloader(phase, config):
    is_shuffle = phase == 'train'

    dataset = MyDataset(phase, config)
    dataloader = DataLoader(dataset, batch_size=config.batch_size, shuffle=is_shuffle, num_workers=config.num_workers,
                            worker_init_fn=np.random.seed())
    return dataloader


class MyDataset(Dataset):
    def __init__(self, phase, config):
        super(MyDataset, self).__init__()
        self.data_root = config.data_root
        self.aug = phase == "train"

    def __getitem__(self, index):
        pass

    def __len__(self):
        pass


def test():
    pass


if __name__ == "__main__":
    test()
