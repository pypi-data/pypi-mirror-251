import torch 
import torch.nn as nn

def count_parameters(model: nn.Module) -> int:
    """    
    Counts the number of parameters of a nn module
    """
    return sum(p.numel() for p in model.parameters() if p.requires_grad)