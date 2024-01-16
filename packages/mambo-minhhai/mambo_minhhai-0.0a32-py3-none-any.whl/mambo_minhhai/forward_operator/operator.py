
"""
@author: pweiss and mhnguyen
"""

import torch
import torch.nn as nn
from torch import Tensor
from functools import partial

from typing import Optional, Callable, Tuple


class LinearOperator(nn.Module):
    """
    Main linear operator class: A(theta) x 
    Args: theta 
    """

    def __init__(self, A: Optional[Callable] = None, theta: Optional[Tensor] = None) -> None:
        super().__init__()
        self.theta = theta
        self.x_jacobian = None
        self.A = A

    def forward(self, x: Tensor, theta: Optional[Tensor] = None) -> Tensor:
        """
        Forward operator: A(theta) x
        """
        if self.x_jacobian is None or self.x_jacobian.shape != x[0:1, ...].shape:
            self.x_jacobian = torch.randn_like(x[0:1, ...])

        # Check if theta is existed or not
        self._check_theta_exists(theta)

        return self.A(x, self.theta)

    def adjoint(self, y: Tensor, theta: Optional[Tensor] = None) -> Tensor:
        if self.x_jacobian is None:
            raise ValueError(
                "The input size has never been given. Apply A(x) once to call A.adjoint.")

        # Check if theta is existed or not
        self._check_theta_exists(theta)

        fn = partial(self.forward, theta=self.theta)

        def jtv_fn(y):
            _, jtv_fn = torch.func.vjp(fn, self.x_jacobian)
            return jtv_fn(y)[0]

        jtv_fn_vmap = torch.vmap(
            jtv_fn, in_dims=1, out_dims=0, randomness="same")
        return jtv_fn_vmap(y[None])[:, 0]

    def forward_and_adjoint(self, x: Tensor, y: Tensor, theta: Optional[Tensor] = None) -> Tuple[Tensor]:
        """
        Compute forward and adjoint at the same time: Ax and ATy

        Return: (Ax, ATy)
        """
        # Check if theta is existed or not
        self._check_theta_exists(theta)

        fn = partial(self.forward, theta=self.theta)

        return torch.autograd.functional.vjp(fn, x, y, create_graph=False, strict=True)

    def _check_theta_exists(self, theta: Tensor) -> None:
        if theta is None:
            if self.theta is None:
                raise ValueError("Theta must be provided.")
        else:
            self.theta = theta


if __name__ == '__main__':
    import torch.nn as nn
    import torch.nn.functional as F

    device = 'cuda'
    dtype = torch.float32
    torch.set_default_dtype(dtype)
    torch.set_default_device(device)

    # %% validating the function
    batch_size = 2
    psf_size = 5
    img_size = 100
    n_channel = 1

    # %% We define a linear operator
    def myconv(x, theta):
        return F.conv2d(x, theta, padding='valid')

    for i in range(10):
        theta = torch.randn((1, n_channel, psf_size, psf_size)).type(
            dtype).to(device)
        A = LinearOperator(myconv, theta=theta)

        x = torch.randn(
            (batch_size, n_channel, img_size, img_size), device=device)
        y = torch.randn((batch_size, n_channel, img_size -
                        psf_size + 1, img_size - psf_size + 1), device=device)

        Ax = A(x)

        ATy = A.adjoint(y)

        val = (torch.sum(Ax * y) - torch.sum(x * ATy)).item()

        print(val)
