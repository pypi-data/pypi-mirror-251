# %%
"""
Some useful utilities for working with PyTorch tensor and Numpy array

"""
import torch
from torch import Tensor
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

import torchvision.transforms as transforms
from einops import rearrange, asnumpy
import pathlib
from PIL import Image
from typing import BinaryIO, List, Optional, Tuple, Union

_TensorArray = Union[Tensor, np.ndarray]


def update_plt_params(dict=None):
    if dict is not None:
        plt.rcParams.update(dict)
    else:
        default_params = {"tex.usetex": True,
                          "figure.dpi": 120,
                          "axes.titlesize": 24,
                          "xtick.labelsize": 16,
                          "ytick.labelsize": 16}
        plt.rcParams.update(default_params)


def plot_image(x, title: str = '',
               colorbar: bool = False,
               show: bool = True,
               vmin: float = None,
               vmax: float = None,
               cmap: str = 'gray',
               axes: bool = False,
               ax=None):
    """
    def plot_image(x, title='', colorbar=False, show=True, vmin=None, vmax=None, cmap='gray', axes=False):

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

    if axes == False:
        plt.axis("off")
    elif axes != True:
        plt.axis(axes)

    if ax == None:
        ishow = plt.imshow
    else:
        ishow = ax.imshow

    xx = x.detach().cpu()
    if (xx.dim() == 2):
        H = xx.shape[0]
        W = xx.shape[1]
        im = ishow(xx, vmin=vmin, vmax=vmax, cmap=cmap)
    elif (xx.shape[0] == 1 and xx.dim() == 3):
        H = xx.shape[1]
        W = xx.shape[2]
        im = ishow(xx[0], vmin=vmin, vmax=vmax, cmap=cmap)
    elif (xx.shape[0] == 3 and xx.dim() == 3):
        H = xx.shape[1]
        W = xx.shape[2]
        im = ishow(xx.permute(1, 2, 0), vmin=vmin, vmax=vmax, cmap=cmap)
    elif (xx.shape[2] == 3 and xx.dim() == 3):
        H = xx.shape[0]
        W = xx.shape[1]
        im = ishow(xx, vmin=vmin, vmax=vmax, cmap=cmap)
    else:
        raise ValueError(
            "Image x should be 2 or 3-dimensional with 3 channels (first or last place)")
    if title:
        if ax is None:
            plt.title(title)
        else:
            ax.set_title(title)

    if colorbar:
        if ax == None:
            plt.colorbar()
        else:
            divider = make_axes_locatable(ax)
            cax = divider.append_axes("right", size="3%", pad=0.1)
            plt.colorbar(im, cax=cax)

    if show:
        plt.show()


def plot_image_batch(x, title='', colorbar=False, show=True, vmin=None, vmax=None, cmap='gray', axes=False):
    """
    def plot_image_batch(x, title='', colorbar=False, show=True, vmin=None, vmax=None, cmap='gray', axes=False):

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
        plot_image(x[i], title=title, colorbar=colorbar, show=show,
                   vmin=vmin, vmax=vmax, cmap=cmap, axes=axes)


def subplot_image_batch(x, title=[''], suptitle='', colorbar=[False], vmin=None, vmax=None, cmap='gray', axes=False, returns=False):
    """
    def subplot_image_batch(x, title='', colorbar=False, vmin=None, vmax=None, cmap='gray', axes=False):

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

    if type(colorbar) is bool:
        colorbar = [colorbar]
    if (type(cmap) is str) or (cmap is None):
        cmap = [cmap]
    if type(axes) is bool:
        axes = [axes]

    if len(title) == 1:
        title = title*num_plot
    if len(colorbar) == 1:
        colorbar = [colorbar[0]]*num_plot
    if len(cmap) == 1:
        cmap = [cmap[0]]*num_plot
    if len(axes) == 1:
        axes = [axes[0]]*num_plot

    num_img = x[0].shape[0]
    if returns:
        fig_list = []
    for i in range(num_img):

        fig = plt.figure()
        # fig, axs = plt.subplots(1, num_plot, constrained_layout=True)

        for j in range(num_plot):
            ax = plt.subplot(1, num_plot, j+1)
            plot_image(x[j][i], title[j], colorbar=colorbar[j], vmin=vmin,
                       vmax=vmax, cmap=cmap[j], axes=axes[j], show=False, ax=ax)

        if suptitle is not None:
            if title[0] != '':
                fig.tight_layout(rect=[0, 0.03, 1, 1.2])
            else:
                fig.tight_layout(rect=[0, 0.03, 1, 1.25])
            fig.suptitle(suptitle)
        else:
            fig.tight_layout()
        if returns:
            fig_list.append(fig)
        plt.show()

    if returns:
        return fig_list


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

    if show:
        plt.figure()
        if np.min(imgs.shape) == 3:
            plt.imshow(imgs)
        else:
            plt.imshow(imgs, cmap="gray")
            plt.colorbar()
        plt.xticks([])
        plt.yticks([])
        plt.axis("off")
        plt.show()

    imgs = np.uint8(np.clip(imgs * 255. + 0.5, 0, 255)).squeeze()
    Image.fromarray(imgs).save(filename, format=format)


def show_images(imgs: Union[_TensorArray, List[_TensorArray], Tuple[_TensorArray]],
                title=None,
                batched: bool = False,
                ncols: int = None,
                colorbar: Optional[bool] = False,
                vmin: Optional[float] = None,
                vmax: Optional[float] = None,
                ):
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

    fig, ax = plt.subplots()
    if np.min(imgs.shape) == 3:
        im = ax.imshow(imgs, vmin=vmin, vmax=vmax)
    else:
        im = ax.imshow(imgs, vmin=vmin, vmax=vmax, cmap="gray")
    if colorbar:
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="3%", pad=0.1)
        plt.colorbar(im, cax=cax)
    if title:
        ax.set_title(title)
    ax.set_xticks([])
    ax.set_yticks([])
    plt.show()


# %%
if __name__ == "__main__":
    import sys
    from skimage import data
    from common import channel_last_to_channel_first

    imgs = [data.astronaut(), data.astronaut()]
    imgs = torch.stack([torch.from_numpy(img) for img in imgs])
    imgs = channel_last_to_channel_first(imgs) / 255.

    show_images(imgs, title="show_images", ncols=2, colorbar=True)
    plot_image_batch(imgs, title="plot_image_batch", colorbar=True)
    subplot_image_batch(imgs, suptitle="subplot_image_batch", title=["Img 1", "Img 2"],
                        colorbar=True, cmap="gray")
    subplot_image_batch(imgs, suptitle="subplot_image_batch", title=[""],
                        colorbar=True, cmap="gray")

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

# %%
