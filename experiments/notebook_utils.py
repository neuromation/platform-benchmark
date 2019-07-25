from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from PIL.Image import Image as TImage
from dataset import CLASSES_NAMES, get_datasets
from network import CifarResnet18
from utils import get_device, get_image_by_url, confusion_matrix_as_img


def show_single_predict(model: CifarResnet18, image_url: str) -> None:
    image = get_image_by_url(image_url)
    i_class = model.predict(image=image, device=get_device())
    name = CLASSES_NAMES[i_class]

    plt.figure(figsize=(4, 4))
    plt.imshow(image)
    plt.axis('off')
    plt.title(f'Class: {i_class} ({name})')
    plt.show()


def compute_and_show_conf_mat(test_dir: Path, path_to_ckpt: Path) -> None:
    conf_mat = compute_conf_mat(test_dir=test_dir, path_to_ckpt=path_to_ckpt)

    plt.figure(figsize=(12, 12))
    plt.imshow(conf_mat)
    plt.axis('off')
    plt.title('Confusion matrix')
    plt.show()


def compute_conf_mat(test_dir: Path, path_to_ckpt: Path) -> TImage:
    model = CifarResnet18.from_ckpt(path_to_ckpt)

    _, test_set = get_datasets(train_root=test_dir, test_root=test_dir)

    preds, gts = model.evaluate(dataset=test_set, batch_size=512,
                                device=get_device())

    conf_mat = confusion_matrix_as_img(gts=np.array(gts),
                                       preds=np.array(preds),
                                       classes=CLASSES_NAMES)

    return conf_mat
