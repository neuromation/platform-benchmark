from pathlib import Path
from typing import List, Tuple

import torch
from PIL.Image import Image
from dataset import get_transforms, CIFAR_SIZE
from torch import Tensor
from torch import nn
from torch.utils.data import DataLoader
from torchvision.datasets import DatasetFolder
from torchvision.models import resnet18
from tqdm import tqdm


class CifarResnet18(nn.Module):

    def __init__(self, pretrained: bool):
        super().__init__()

        self._model = resnet18(pretrained=pretrained)
        self._model.avgpool = nn.AdaptiveAvgPool2d(1)

        hide_dim = self._model.fc.in_features
        self._model.fc = nn.Linear(in_features=hide_dim,
                                   out_features=CIFAR_SIZE)

    def forward(self, img_batch: Tensor) -> Tensor:  # type: ignore
        return self._model(img_batch)

    def save(self, path_to_ckpt: Path) -> None:
        checkpoint = {'state_dict': self._model.state_dict()}
        torch.save(checkpoint, path_to_ckpt)

    def evaluate(self,
                 device: torch.device,
                 dataset: DatasetFolder,
                 batch_size: int
                 ) -> Tuple[List[int], List[int]]:
        self._model.to(device)
        self._model.eval()

        loader = DataLoader(dataset=dataset, shuffle=False,
                            num_workers=4, batch_size=batch_size,
                            drop_last=False)

        preds: List[int] = []
        gts: List[int] = []

        with torch.no_grad():
            for img, label in tqdm(loader):
                pred = torch.argmax(self._model(img.to(device)), dim=1)

                preds.extend(pred.detach().cpu().numpy().tolist())
                gts.extend(label.numpy().tolist())

        return preds, gts

    def predict(self, image: Image, device: torch.device) -> int:
        self._model.to(device)
        self._model.eval()

        img = get_transforms()(image).unsqueeze(0)
        i_class = int(torch.argmax(self._model(img.to(device)), dim=1))
        return i_class

    @classmethod
    def from_ckpt(cls, path_to_ckpt: Path) -> 'CifarResnet18':
        cifar_resnet18 = cls(pretrained=False)

        checkpoint = torch.load(path_to_ckpt, map_location='cpu')
        cifar_resnet18._model.load_state_dict(checkpoint['state_dict'])

        return cifar_resnet18
