from argparse import ArgumentParser, Namespace
from pathlib import Path

from dataset import get_datasets
from network import CifarResnet18
from trainer import Trainer


def main(args: Namespace) -> None:
    train_set, test_set = get_datasets(train_root=args.data_root / 'train',
                                       test_root=args.data_root / 'test')

    model = CifarResnet18(pretrained=True)

    trainer = Trainer(train_set=train_set, test_set=test_set,
                      model=model, log_dir=args.log_dir,
                      batch_size=args.batch_size)

    trainer.train(n_epoch=args.n_epoch)


def get_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument('--data_root', dest='data_root', type=Path)
    parser.add_argument('--log_dir', dest='log_dir', type=Path)

    parser.add_argument('--n_epoch', dest='n_epoch', type=int, default=5)
    parser.add_argument('--bs', dest='batch_size', type=int, default=512)
    return parser


if __name__ == '__main__':
    main(args=get_parser().parse_args())
