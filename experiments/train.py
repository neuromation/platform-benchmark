import itertools
import shutil
from argparse import ArgumentParser, Namespace
from pathlib import Path
import subprocess

from google.cloud import storage

from experiments.dataset import get_datasets
from experiments.network import CifarResnet18
from experiments.trainer import Trainer


def download_folder(gs_path: str, local_path: Path):
    shutil.rmtree(local_path, ignore_errors=True)
    local_path.mkdir(parents=True, exist_ok=True)

    command = ['gsutil', '-m', 'cp', '-r', gs_path, str(local_path)]
    print(' '.join(command))
    ret = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert ret.returncode == 0


def upload_folder(local_path: Path, gs_path: str):
    command = ['gsutil', '-m', 'cp', '-r', str(local_path), gs_path]
    print(' '.join(command))
    ret = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert ret.returncode == 0


def main(args: Namespace) -> None:
    dataset_path = Path('./dataset/cifar10')
    logs_path = Path('./logs')

    download_folder(args.dataset_gs_path, dataset_path.parent)

    train_set, test_set = get_datasets(train_root=dataset_path / 'train',
                                       test_root=dataset_path / 'test')

    model = CifarResnet18(pretrained=False)

    trainer = Trainer(
        train_set=train_set, test_set=test_set, model=model, log_dir=Path('./logs'), batch_size=args.batch_size
    )

    trainer.train(n_epoch=args.n_epoch)

    upload_folder(logs_path, args.logs_gs_path)


def get_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument('--dataset-gs-path', type=str, required=True)
    parser.add_argument('--logs-gs-path', type=str, required=True)

    parser.add_argument('--n_epoch', dest='n_epoch', type=int, default=5)
    parser.add_argument('--bs', dest='batch_size', type=int, default=512)

    return parser


if __name__ == '__main__':
    main(args=get_parser().parse_args())
