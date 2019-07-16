import torch
import torch.nn as nn
import random


# Functions
##############################################################################
def get_network(config):
    return MyNetwork(config)


def set_requires_grad(nets, requires_grad=False):
    """Set requies_grad=Fasle for all the networks to avoid unnecessary computations
    Parameters:
        nets (network list)   -- a list of networks
        requires_grad (bool)  -- whether the networks require gradients or not
    """
    if not isinstance(nets, list):
        nets = [nets]
    for net in nets:
        if net is not None:
            for param in net.parameters():
                param.requires_grad = requires_grad


# Functions
##############################################################################
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
