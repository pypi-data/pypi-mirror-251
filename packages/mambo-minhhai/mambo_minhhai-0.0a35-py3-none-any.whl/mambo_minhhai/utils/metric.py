"""
Author: mhnguyen
"""

import torch
import numpy as np


def snr(input, target, reduce=True):
    """
    Signal-to-noise ration 
        10 log10(signal ** 2 / noise**2)

    Args: input, target: Tensor or array of the same dimension
    """
    if torch.is_tensor(input):
        with torch.no_grad():
            if input.dim() == 4:
                input = input.flatten(1, -1)
                target = target.flatten(1, -1)
                err = ((target - input)**2).sum(dim=1) / \
                    ((target**2).sum(dim=1) + 1e-16)
                snr = -10 * torch.log10(err + 1e-16)
                if reduce:
                    return torch.mean(snr).item()
                else:
                    return snr.tolist()
            else:
                input = input.ravel()
                target = target.ravel()
                err = ((target - input)**2).sum() / ((target**2).sum() + 1e-16)
                snr = -10 * torch.log10(err + 1e-16)
                return snr.item()
    else:
        if input.ndim == 4:
            input = input.flatten(1, -1)
            target = target.flatten(1, -1)
            err = ((target - input)**2).sum(dim=1) / \
                ((target**2).sum(dim=1) + 1e-16)
            snr = -10 * np.log10(err + 1e-16)
            if reduce:
                return np.mean(snr)
            else:
                return snr.tolist()
        else:
            input = input.ravel()
            target = target.ravel()
            err = ((target - input)**2).sum() / ((target**2).sum() + 1e-16)
            snr = -10 * np.log10(err + 1e-16)
            return snr


def psnr(input, target, reduce=True, max_value=1.):
    """
    Peak Signal-to-noise ration 
        -10 log10(noise**2 / max_value)

    Args: input, target: Tensor or array of the same dimension
    """
    if torch.is_tensor(input):
        with torch.no_grad():
            if input.dim() == 4:
                input = input.flatten(1, -1)
                target = target.flatten(1, -1)
                err = ((target - input)**2).sum(dim=1) / max_value
                psnr = -10 * torch.log10(err + 1e-16)
                if reduce:
                    return torch.mean(psnr).item()
                else:
                    return psnr.tolist()
            else:
                input = input.ravel()
                target = target.ravel()
                err = ((target - input)**2).sum() / max_value
                psnr = -10 * torch.log10(err + 1e-16)
                return psnr.item()
    else:
        if input.ndim == 4:
            input = input.flatten(1, -1)
            target = target.flatten(1, -1)
            err = ((target - input)**2).sum(dim=1) / max_value
            psnr = -10 * np.log10(err + 1e-16)
            if reduce:
                return np.mean(psnr)
            else:
                return psnr.tolist()
        else:
            input = input.ravel()
            target = target.ravel()
            err = ((target - input)**2).sum() / max_value
            psnr = -10 * np.log10(err + 1e-16)
            return psnr
