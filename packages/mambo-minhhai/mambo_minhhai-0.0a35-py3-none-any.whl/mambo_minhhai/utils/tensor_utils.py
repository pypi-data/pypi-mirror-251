import torch
import imageio as io
from pathlib import Path
import matplotlib.pyplot as plt


def to_uint8(x, scale=True):
    """
    transforms input data to uint8 in [0,255]
    scale = True does (x-x.min())/(x.max() - x.min())*255
    """
    if scale:
        x_norm = (x - x.min()) / (x.max() - x.min())
    else:
        x_norm = x

    xx = x_norm.clone().detach().cpu() * 255
    return xx.to(torch.uint8)


def to_gpu(x, device='cuda', dtype=torch.float32):
    """
    return torch.tensor(x, device = device, dtype = dtype)
    """
    return torch.tensor(x, device=device, dtype=dtype)


def to_cpu(x):
    """
    x.cpu().detach()
    """
    return x.cpu().detach()


def to_numpy(x):
    """
    return x.detach().cpu().numpy()
    """
    return x.detach().cpu().numpy()
