from pathlib import Path
from typing import List

import PIL
import matplotlib.pyplot as plt
import numpy as np
import torch
from PIL.Image import Image
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from sklearn.metrics import confusion_matrix
from sklearn.utils.multiclass import unique_labels
from torch.cuda import is_available as is_avai

from network import CIFAR_SIZE
from network import CifarResnet18
from train import get_datasets


def canvas_to_img(canvas: FigureCanvas) -> PIL.Image:
    canvas.draw()
    string, (width, height) = canvas.print_to_buffer()
    img = np.fromstring(string, np.uint8).reshape((height, width, 4))
    pil_image = PIL.Image.fromarray(img, mode='RGBA')
    return pil_image


def confusion_matrix_as_img(gts: np.ndarray,
                            preds: np.ndarray,
                            classes: List[str]
                            ) -> Image:
    font = 20
    conf_mat = confusion_matrix(y_true=gts, y_pred=preds)
    classes = np.array(classes)[unique_labels(gts, preds)]

    conf_mat = conf_mat.astype('float') / conf_mat.sum(axis=1)[:, np.newaxis]

    fig = Figure(figsize=(16, 16))
    canvas = FigureCanvas(fig)
    ax = fig.gca()

    ax.imshow(conf_mat, interpolation='nearest', cmap=plt.cm.Blues)

    ax.set(xticks=np.arange(conf_mat.shape[1]),
           yticks=np.arange(conf_mat.shape[0]),
           xticklabels=classes, yticklabels=classes,
           ylabel='Ground Truth', xlabel='Predicted')

    ax.xaxis.label.set_fontsize(font)
    ax.yaxis.label.set_fontsize(font)

    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor", fontsize=font)
    plt.setp(ax.get_yticklabels(), fontsize=font)

    for i in range(conf_mat.shape[0]):
        for j in range(conf_mat.shape[1]):
            txt = '0' if conf_mat[i, j] == 0 else format(conf_mat[i, j], '.2f')
            is_more = conf_mat[i, j] > conf_mat.max() / 2.
            ax.text(x=j, y=i, s=txt,
                    ha="center", va="center",
                    color="white" if is_more else "black",
                    size=int(0.6 * font)
                    )

    fig.tight_layout()
    pil_image = canvas_to_img(canvas)
    return pil_image


def compute_conf_mat(test_dir: Path, path_to_ckpt: Path) -> Image:
    model = CifarResnet18.from_ckpt(path_to_ckpt)

    _, test_set = get_datasets(train_root=test_dir, test_root=test_dir)

    device = torch.device('cuda:0') if is_avai() else torch.device('cpu')
    preds, gts = model.evaluate(dataset=test_set, batch_size=512, device=device)
    classes = [f'#{i}' for i in range(CIFAR_SIZE)]
    conf_mat = confusion_matrix_as_img(gts=np.array(gts),
                                       preds=np.array(preds),
                                       classes=classes)

    return conf_mat


def compute_and_show_conf_mat(test_dir: Path, path_to_ckpt: Path) -> None:
    conf_mat = compute_conf_mat(test_dir=test_dir, path_to_ckpt=path_to_ckpt)

    plt.figure(figsize=(12, 12))
    plt.imshow(conf_mat)
    plt.axis('off')
    plt.title('Confusion matrix')
    plt.show()
