"""
@author: pweiss
"""

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


def write_image(x, name, scale=True):
    """
    Writes a torch image x to a file called name. 
    The image is coded over 8 bits

    INPUT: 
        - x : image of size WxH or 3xWxH or WxHx3
        - name : string of the name to save
        - scale=True : rescale to [0,1] before converting to uint8
    """
    if scale:
        xx = to_uint8(x, scale=True)
    else:
        xx = to_uint8(x, scale=False)

    if (xx.dim() == 2):
        io.imwrite(name, xx)
    elif (xx.dim() == 3 and xx.shape[0] == 1):
        io.imwrite(name, xx[0])
    elif (xx.dim() == 3 and xx.shape[0] == 3):
        io.imwrite(name, xx.permute(1, 2, 0))
    elif (xx.dim() == 3 and xx.shape[2] == 3):
        io.imwrite(name, xx)
    elif (xx.dim() == 3 and xx.shape[2] == 1):
        io.imwrite(name, xx[:, :])
    else:
        raise ValueError(
            "Image x should be 2 or 3-dimensional with 1 or 3 channels (first or last place)")


def write_image_batch(x, prefix, folder=None, scale=True):
    """
    Writes a batch of N torch images of size NxCxWxH or NxWxHxC in png format

    INPUT: 
        - x : batch of images of size NxCxWxH or NxWxHxC or NxWxH
        - prefix : string of the name to save (%i_prefix.png)
        - folder=None: you can specify a folder where to save this is just a string
        - scale=True : if true, rescale to [0,1] before converting to uint8
    """

    batch_size = x.shape[0]
    for i in range(batch_size):
        if (folder == None):
            name = prefix + ("%02d_" % i) + ".png"
        else:
            Path(folder).mkdir(parents=True, exist_ok=True)
            filename = prefix + ("%02d_" % i) + ".png"
            name = Path(folder) / filename

        write_image(x[i], name=name, scale=scale)



