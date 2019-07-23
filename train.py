from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Tuple

import PIL
import torchvision.transforms as t
from torchvision.datasets import DatasetFolder

from network import CifarResnet18
from trainer import Trainer


def get_datasets(data_root: Path) -> Tuple[DatasetFolder, DatasetFolder]:
    std = (0.229, 0.224, 0.225)  # for pretrained on Imagenet
    mean = (0.485, 0.456, 0.406)  # for pretrained on Imagenet

    transforms = t.Compose([t.ToTensor(), t.Normalize(mean=mean, std=std)])

    read_func, ext = PIL.Image.open, ['png']

    train_set = DatasetFolder(root=data_root / 'train', loader=read_func, extensions=ext,
                              transform=transforms, target_transform=None)

    test_set = DatasetFolder(root=data_root / 'test', loader=read_func, extensions=ext,
                             transform=transforms, target_transform=None)

    return train_set, test_set


def main(args: Namespace) -> None:
    train_set, test_set = get_datasets(data_root=args.data_root)

    model = CifarResnet18(pretrained=True)

    trainer = Trainer(train_set=train_set, test_set=test_set,
                      model=model, log_dir=args.log_dir, batch_size=args.batch_size)

    trainer.train(n_epoch=args.n_epoch)


def get_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument('--data_root', dest='data_root', type=Path)
    parser.add_argument('--log_dir', dest='log_dir', type=Path)

    parser.add_argument('--n_epoch', dest='n_epoch', type=int, default=100)
    parser.add_argument('--batch_size', dest='batch_size', type=int, default=512)
    return parser


if __name__ == '__main__':
    main(args=get_parser().parse_args())
