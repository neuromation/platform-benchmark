from pathlib import Path
from typing import List

import numpy as np
import torch
from tensorboardX import SummaryWriter
from torch import device
from torch import nn
from torch import optim
from torch.utils.data import DataLoader
from torchvision.datasets import DatasetFolder
from tqdm import tqdm

from network import CifarResnet18


class Trainer:

    def __init__(self,
                 train_set: DatasetFolder,
                 test_set: DatasetFolder,
                 model: CifarResnet18,
                 log_dir: Path,
                 batch_size: int
                 ):
        self._train_set = train_set
        self._test_set = test_set
        self._model = model
        self._batch_size = batch_size

        self._writer = SummaryWriter(log_dir / 'board')

        self._criterion = nn.CrossEntropyLoss()
        self._optimizer = optim.SGD(params=self._model.parameters(), lr=1e-1)
        self._device = device('cuda:0') if torch.cuda.is_available() else device('cpu')
        self._i_global = 0

    def train_epoch(self) -> None:
        self._model.to(self._device)
        self._model.train()

        loader = DataLoader(dataset=self._train_set, batch_size=self._batch_size,
                            shuffle=True, num_workers=4, drop_last=True)

        for img, label in tqdm(loader):
            self._optimizer.zero_grad()

            pred = self._model(img.to(self._device))
            loss = self._criterion(pred, label.to(self._device))
            loss.backward()
            self._optimizer.step()

            loss_v = float(loss.detach().cpu())

            self._writer.add_scalar('loss', loss_v, self._i_global)
            self._i_global += 1

    def test(self) -> float:
        self._model.to(self._device)
        self._model.eval()

        loader = DataLoader(dataset=self._test_set, batch_size=self._batch_size,
                            shuffle=False, num_workers=4, drop_last=False)

        preds: List[int] = []
        gts: List[int] = []

        with torch.no_grad():
            for img, label in tqdm(loader):
                pred = torch.argmax(self._model(img.to(self._device)), dim=1)

                preds.extend(pred.detach().cpu().numpy().tolist())
                gts.extend(label)

        accuracy = (np.array(preds) == np.array(gts)) / len(preds)
        return accuracy

    def train(self, n_epoch: int) -> None:
        for i in range(1, n_epoch + 1):
            self.train_epoch()
            self.test()

        self._model.save(self.log_dir / 'last.ckpt')
