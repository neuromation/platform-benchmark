from pathlib import Path

import torch
from torch import Tensor
from torch import nn
from torchvision.models import resnet18

CIFAR_SIZE = 10


class CifarResnet18(nn.Module):

    def __init__(self, pretrained: bool):
        super().__init__()

        self._model = resnet18(pretrained=pretrained)
        self._model.avgpool = nn.AdaptiveAvgPool2d(1)

        hide_dim = self._model.fc.in_features
        self.fc = nn.Linear(in_features=hide_dim, out_features=CIFAR_SIZE)

    def forward(self, img_batch: Tensor) -> Tensor:  # type: ignore
        return self._model(img_batch)

    def save(self, path_to_ckpt: Path) -> None:
        checkpoint = {'state_dict': self._model.state_dict()}
        torch.save(checkpoint, path_to_ckpt)

    @classmethod
    def from_ckpt(cls, path_to_ckpt: Path) -> nn.Module:
        cifar_resnet18 = cls(pretrained=False)

        checkpoint = torch.load(path_to_ckpt, map_location='cpu')
        cifar_resnet18._model.load_state_dict(checkpoint['state_dict'])

        return cifar_resnet18
