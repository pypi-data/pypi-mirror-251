"""
Some useful utilities for working with PyTorch tensor and Numpy array

"""
import torch
from torch import Tensor
import numpy as np
import matplotlib.pyplot as plt
import torchvision.transforms as transforms
from einops import rearrange, asnumpy
import pathlib
from PIL import Image
from typing import BinaryIO, List, Optional, Tuple, Union

_TensorArray = Union[Tensor, np.ndarray]


def plot_image(x, title='', colorbar=False, show=True, vmin=None, vmax=None, cmap='gray', axes=False):
    """
    Displays a torch image x with plenty of options.

    INPUT: 
        - x : image of size WxH or 3xWxH or WxHx3
        - title='': string for the title
        - colorbar = False : for a colorbar 
        - show = True
        - vmin = None, vmax = None: min and max value for plotting with similar 
        - cmap = 'gray' : colormap
        - axes = False: axes or not
    """
    if show:
        plt.figure()

    if axes is False:
        plt.axis("off")
    elif axes != True:
        plt.axis(axes)

    xx = x.cpu().detach()
    if (xx.dim() == 2):
        plt.imshow(xx, vmin=vmin, vmax=vmax, cmap=cmap)
    elif (xx.shape[0] == 1 and xx.dim() == 3):
        plt.imshow(xx[0], vmin=vmin, vmax=vmax, cmap=cmap)
    elif (xx.shape[0] == 3 and xx.dim() == 3):
        plt.imshow(xx.permute(1, 2, 0), vmin=vmin, vmax=vmax, cmap=cmap)
    elif (xx.shape[2] == 3 and xx.dim() == 3):
        plt.imshow(xx, vmin=vmin, vmax=vmax, cmap=cmap)
    else:
        raise ValueError(
            "Image x should be 2 or 3-dimensional with 3 channels (first or last place)")

    if colorbar:
        plt.colorbar()

    plt.title(title)
    if show:
        plt.show()


def plot_image_batch(x, title='', colorbar=False, show=True, vmin=None, vmax=None, cmap='gray', axes=False):
    """    
    Displays a batch of torch images x with plenty of options.
    Same as plot_image, except that this function loops over the batch elements

    INPUT: 
        - x : image of size NxWxH or Nx3xWxH or NxWxHx3
        - title='': string for the title
        - colorbar = False : for a colorbar 
        - show = True
        - vmin = None, vmax = None: min and max value for plotting with similar 
        - cmap = 'gray' : colormap
        - axes = False: axes or not
    """
    for i in range(x.shape[0]):
        plot_image(x[i], title='', colorbar=False, show=True,
                   vmin=None, vmax=None, cmap='gray', axes=False)


def subplot_image_batch(x, title=[''], colorbar=[False], vmin=None, vmax=None, cmap=['gray'], axes=[False]):
    """   
    Displays a list of batch of torch images x with plenty of options.
    Example: subplot_image_batch([x_t,x_est_t], title=['true','est'])
    Note: all options can be specified as a list

    INPUT: 
        - x: list of images of size NxWxH or Nx3xWxH or NxWxHx3
        - title=['']: list of titles
        - colorbar=[False]: list of colorbars
        - vmin=None, vmax=None: min and max value for plotting with similar levels
        - cmap=['gray']: list of colormaps
        - axes=[False]: list of True or False

    OUTPUT: 
        - a list of matplotlib.pyplot subplots. The length of the list is the batch size.
    """
    num_plot = len(x)
    if len(title) == 1:
        title = ['']*num_plot
    if len(colorbar) == 1:
        colorbar = [colorbar[0]]*num_plot
    if len(cmap) == 1:
        cmap = [cmap[0]]*num_plot
    if len(axes) == 1:
        axes = [axes[0]]*num_plot

    num_img = x[0].shape[0]

    for i in range(num_img):
        for j in range(num_plot):
            plt.subplot(1, num_plot, j+1)
            plot_image(x[j][i], title[j], colorbar=colorbar[j], vmin=vmin,
                       vmax=vmax, cmap=cmap[j], axes=axes[j], show=False)
        plt.show()


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


def show(imgs: List):
    """
    Show image or list of images
    """
    if not isinstance(imgs, list):
        imgs = [imgs]
    fig, axs = plt.subplots(ncols=len(imgs), squeeze=False)

    for i, img in enumerate(imgs):
        img = img.detach()
        mode = "RGB" if img.shape[0] == 3 else "L"
        img = transforms.functional.to_pil_image(img, mode)
        if mode == "RGB":
            axs[0, i].imshow(np.asarray(img))
        else:
            axs[0, i].imshow(np.asarray(img), cmap="gray")
        axs[0, i].set(xticklabels=[], yticklabels=[], xticks=[], yticks=[])
    plt.show()


def save_images(imgs: Union[_TensorArray, List[_TensorArray], Tuple[_TensorArray]],
                filename: Union[str, pathlib.Path, BinaryIO],
                format: Optional[str] = None,
                batched: bool = False,
                ncols: int = None,
                show: bool = False):
    """
    Function so save an image or list of images 

    imgs: float tensor or array, of shape (B, c, H, W) or (B, H, W, c) or (c, H, W) or (H, W, c) or (H, W)
    filename:   
    batched: boolean, if the imgs is presented in batch or not 
    ncols: number of columns if there are many images
    """

    if isinstance(imgs, List) or isinstance(imgs, Tuple):
        if isinstance(imgs[0], np.ndarray):
            imgs = np.array(imgs)
        elif isinstance(imgs[0], torch.Tensor):
            imgs = asnumpy(torch.stack(imgs))
    else:
        imgs = asnumpy(imgs)

    # If batch of 3-channel images
    if imgs.ndim == 4:
        c = np.argmin(imgs.shape[1:])

        if c == 0:
            imgs = rearrange(imgs, "b c h w -> (b h) w c")
        elif c == 1:
            imgs = rearrange(imgs, "b h c w -> (b h) w c")
        elif c == 2:
            imgs = rearrange(imgs, "b h w c -> (b h) w c")

        if ncols is not None:
            imgs = rearrange(
                imgs, "(ncols bh) w c -> bh (ncols w) c", ncols=ncols)

    # A single RGB image or batch of gray images
    elif imgs.ndim == 3:
        if not batched:
            c = np.argmin(imgs.shape)
            if c == 0:
                imgs = rearrange(imgs, "c h w -> h w c")
            elif c == 1:
                imgs = rearrange(imgs, "h c w -> h w c")
        else:
            imgs = rearrange(imgs, "b h w -> (b h) w")
            if ncols is not None:
                imgs = rearrange(
                    imgs, "(ncols bh) w -> bh (ncols w)", ncols=ncols)

    imgs = np.uint8(np.clip(imgs * 255. + 0.5, 0, 255)).squeeze()

    if show:
        plt.figure()
        if np.min(imgs.shape) == 3:
            plt.imshow(imgs)
        else:
            plt.imshow(imgs, cmap="gray")
        plt.xticks = []
        plt.yticks = []
        plt.show()

    Image.fromarray(imgs).save(filename, format=format)


def show_images(imgs: Union[_TensorArray, List[_TensorArray], Tuple[_TensorArray]],
                format: Optional[str] = None,
                batched: bool = False,
                ncols: int = None):
    """
    Function so save an image or list of images 

    imgs: float tensor or array, of shape (B, C, H, W) or (B, H, W, C) or (C, H, W) or (H, W, C) or (H, W)
    batched: boolean, if the imgs is presented in batch or not 
    ncols: number of columns if there are many images
    """

    if isinstance(imgs, List) or isinstance(imgs, Tuple):
        if isinstance(imgs[0], np.ndarray):
            imgs = np.array(imgs)
        elif isinstance(imgs[0], torch.Tensor):
            imgs = asnumpy(torch.stack(imgs))
    else:
        imgs = asnumpy(imgs)

    # If batch of 3-channel images
    if imgs.ndim == 4:
        c = np.argmin(imgs.shape[1:])

        if c == 0:
            imgs = rearrange(imgs, "b c h w -> (b h) w c")
        elif c == 1:
            imgs = rearrange(imgs, "b h c w -> (b h) w c")
        elif c == 2:
            imgs = rearrange(imgs, "b h w c -> (b h) w c")

        if ncols is not None:
            imgs = rearrange(
                imgs, "(ncols bh) w c -> bh (ncols w) c", ncols=ncols)

    # A single RGB image or batch of gray images
    elif imgs.ndim == 3:
        if not batched:
            c = np.argmin(imgs.shape)
            if c == 0:
                imgs = rearrange(imgs, "c h w -> h w c")
            elif c == 1:
                imgs = rearrange(imgs, "h c w -> h w c")
        else:
            imgs = rearrange(imgs, "b h w -> (b h) w")
            if ncols is not None:
                imgs = rearrange(
                    imgs, "(ncols bh) w -> bh (ncols w)", ncols=ncols)

    # imgs = np.uint8(np.clip(imgs * 255. + 0.5, 0, 255)).squeeze()

    plt.figure()
    if np.min(imgs.shape) == 3:
        plt.imshow(imgs)
    else:
        plt.imshow(imgs, cmap="gray")
    # plt.xticks([])
    # plt.yticks([])
    plt.axis("off")
    plt.show()


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


if __name__ == "__main__":
    import sys

    def _exclude(exclusions: list) -> list:
        import types

        # add everything as long as it's not a module and not prefixed with _
        functions = [name for name, function in globals().items()
                     if not (name.startswith('_') or isinstance(function, types.ModuleType))]

        # remove the exclusions from the functions
        for exclusion in exclusions:
            if exclusion in functions:
                functions.remove(exclusion)

        del types  # deleting types from scope, introduced from the import
        return functions

    # the _ prefix is important, to not add these to the __all__
    _exclusions = []
    __all__ = _exclude(_exclusions)
    print(f"All functions in {sys.modules[__name__]} are : ", __all__)
