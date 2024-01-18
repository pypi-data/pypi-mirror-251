import torch
import numpy as np
from torch import Tensor
from einops import rearrange
from PIL import Image

from typing import Union, List, Tuple

_TensorArray = Union[Tensor, np.ndarray]


def to_flattened_numpy(x):
    """Flatten a torch tensor `x` and convert it to numpy."""
    return x.detach().cpu().numpy().reshape((-1,))


def from_flattened_numpy(x, shape):
    """Form a torch tensor with the given `shape` from a flattened numpy array `x`."""
    return torch.from_numpy(x.reshape(shape))


def is_one_dim_tensor(x):
    """
    Check if input is an one-dimensional tensor or not
    """
    if isinstance(x, Tensor):
        return True if x.ndim == 1 else False
    else:
        return False


def channel_fist_to_channel_last(images: Union[List[_TensorArray], Tuple[_TensorArray]]):
    """
    Reorder images: (B, C, H, W) to (B, H, W, C) or (C, H, W) to (H, W, C)

    Input: list or tuple of tensors or numpy arrays
    """
    if isinstance(images, list):
        return [rearrange(img, "c h w -> h w c") for img in images]
    elif isinstance(images, tuple):
        return (rearrange(img, "c h w -> h w c") for img in images)
    else:
        if images.ndim == 4:
            return rearrange(images, "b c h w -> b h w c")
        elif images.ndim == 3:
            return rearrange(images, "c h w -> h w c")


def channel_last_to_channel_first(images: Union[List[_TensorArray], Tuple[_TensorArray]]):
    """
    Reorder images: (B, H, W, C) to (B, C, H, W) or (H, W, C) to (C, H, W)

    Input: list or tuple of tensors or numpy arrays
    """
    if isinstance(images, list):
        return [rearrange(img, "h w c -> c h w") for img in images]
    elif isinstance(images, tuple):
        return (rearrange(img, "h w c -> c h w") for img in images)
    else:
        if images.ndim == 4:
            return rearrange(images, "b h w c -> b c h w")
        elif images.ndim == 3:
            return rearrange(images, "h w c -> c h w")


def numpy_to_PIL(images: List[np.ndarray]):
    """
    Transform list of float numpy images  to PIL Image
    """

    def _normalize_clip(input):
        input = input / input.max()
        return np.uint8(np.clip(input * 255. + 0.5, 0, 255))

    if isinstance(images, list):
        return [Image.fromarray(_normalize_clip(img)) for img in images]
    else:
        if images.ndim == 4:
            return [Image.fromarray(_normalize_clip(img)) for img in images]
        else:
            return Image.fromarray(_normalize_clip(images))


def to_numpy(input: Tensor):
    return input.detach().cpu().numpy()


def make_gif(images: List[np.ndarray], name: str, duration: float = 1.):
    frames = numpy_to_PIL(images)
    frame_one = frames[0]
    frame_one.save(name, format="GIF", append_images=frames,
                   save_all=True, duration=duration, loop=0)
