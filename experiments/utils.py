from io import BytesIO
from typing import List

import PIL
import numpy as np
import requests
import torch
from PIL.Image import Image as TImage
from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from sklearn.metrics import confusion_matrix
from sklearn.utils.multiclass import unique_labels
from torch.cuda import is_available as is_avai


def get_device() -> torch.device:
    device = torch.device('cuda:0') if is_avai() else torch.device('cpu')
    return device


def get_image_by_url(image_url: str) -> TImage:
    data = requests.get(image_url).content
    im = PIL.Image.open(BytesIO(data))
    return im


def canvas_to_img(canvas: FigureCanvas) -> TImage:
    canvas.draw()
    string, (width, height) = canvas.print_to_buffer()
    img = np.fromstring(string, np.uint8).reshape((height, width, 4))
    pil_image = PIL.Image.fromarray(img, mode='RGBA')
    return pil_image


def confusion_matrix_as_img(gts: np.ndarray,
                            preds: np.ndarray,
                            classes: List[str]
                            ) -> TImage:
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
