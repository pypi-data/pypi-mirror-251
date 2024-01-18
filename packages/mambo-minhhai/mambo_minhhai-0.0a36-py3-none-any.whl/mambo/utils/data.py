import torch.utils.data as data
from PIL import Image
from typing import List, Union

import os
import glob


class ImageDataset(data.Dataset):
    """
    A general class for image dataset.

    Args: 

    """

    def __init__(self, root, transform=None, format="RGB", img_exts: Union[List[str], str] = "jpg"):
        self.root = root
        self.transform = transform
        self.img_names = []

        if isinstance(img_exts, List):
            for ext in img_exts:
                self.img_names += glob.glob(os.path.join(root, f"*.{ext}"))
        else:
            self.img_names += glob.glob(os.path.join(root, f"*.{img_exts}"))

        assert format in ["RGB", "rgb",  "multi",
                          "Gray", "gray", "grayscale", "single"]
        self.format = format

    def __len__(self):
        return len(self.img_names)

    def __getitem__(self, idx):

        img_path = os.path.join(self.root, self.img_names[idx])
        if self.format in ["RGB", "rgb", "multi"]:
            img = Image.open(img_path).convert("RGB")   # PIL Image
        else:
            img = Image.open(img_path).convert("L")

        if self.transform is not None:
            img_processed = self.transform(img)

            return img_processed
        else:
            return img
