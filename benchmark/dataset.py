from pathlib import Path
from typing import Tuple

import PIL
from torchvision import transforms as t
from torchvision.datasets import DatasetFolder

CIFAR_SIZE = 10

CLASSES_NAMES = [
    'airplane', 'automobile', 'bird', 'cat', 'deer',
    'dog', 'frog', 'horse', 'ship', 'truck'
]


def get_transforms() -> t.Compose:
    std = (0.229, 0.224, 0.225)  # for pretrained on Imagenet
    mean = (0.485, 0.456, 0.406)  # for pretrained on Imagenet
    transforms = t.Compose([t.ToTensor(), t.Normalize(mean=mean, std=std)])
    return transforms


def get_datasets(train_root: Path,
                 test_root: Path
                 ) -> Tuple[DatasetFolder, DatasetFolder]:
    read_func, ext = PIL.Image.open, ['png']

    transforms = get_transforms()

    train_set = DatasetFolder(root=train_root, loader=read_func,
                              extensions=ext, transform=transforms,
                              target_transform=None)

    test_set = DatasetFolder(root=test_root, loader=read_func,
                             extensions=ext, transform=transforms,
                             target_transform=None)

    for c, c1, c2 in zip(CLASSES_NAMES, train_set.classes, test_set.classes):
        assert c == c1 == c2

    return train_set, test_set
