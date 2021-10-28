import torch
import torch.nn as nn
import random


def get_network(config):
    return MyNetwork(config)


class MyNetwork(nn.Module):
    def __init__(self, config):
        super(MyNetwork, self).__init__()
        pass

    def forward(self, x):
        pass


def test():
    pass


if __name__ == '__main__':
    test()
