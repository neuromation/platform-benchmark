# Benchmark for platforms comparison.


## Intro
This repository is an application for comparison of machine learning platforms
which we made in [Neuromation](https://neuromation.io/). In our point of view, for
a fair comparison it is necessary to run the same typical task on each
participating platform.

In the `master` branch, you can find the code and commands needed to run the task on
your local gpu server. For each platform, we created an additional branch so that you
can clearly see what commands and changes you need to add to the project 
to run the proposed task.

**Disclaimer**. Please note that we do not use techniques to improve the accuracy of the model
(sush as data augmentations, learning rate scheduling e.t.c), since our goal is to compare
platforms. As a result, we made the code as simple as possible.


## Task defenition
As a benchmark, we propose to solve the task of images classification on
[CIFAR10](https://www.cs.toronto.edu/~kriz/cifar.html) dataset.
The dataset consists of 60000 32x32 colour images in 10 classes,
with 6000 images per class. There are 50000 training images and 10000 test images. 

We have prepared images in `.png` format arranged in folders
[here](https://drive.google.com/open?id=1a-X4mZ5y6hQ0aX6-bNG6HU-Tfdom1lh6) [140 MB].
Also, dataset is also available by writing one line of code in
[pytorch](https://pytorch.org/docs/stable/torchvision/datasets.html#cifar),
but in our opinion working with files give a more knowledge of the platforms.

We will follow a common scenario when working with each platform
and write down all our actions in [Scenario.md](Scenario.md)
(please, change a branch to see scenario implementation for each platform).


## Comparison results
At all points of comparison, we rated 1, 2 or 3.

|                     | Convenience of working with data | Remote debugging | Sharing with engineers   |  Sharing with non engineers  | Sharing of environment |
|---------------------|:--------------------------------:|:----------------:|----------------------------|--------------------------------|------------------------|
| neuro               |                 3                |        3         |              3             |               3                |          3             |
| AWS SageMaker       |                                  |                  |                            |                                |                        |
| Google AI Platform  |                                  |                  |                            |                                |                        |
| Floydhub            |                                  |                  |                            |                                |                        |
| Paperspace Gradient |                                  |                  |                            |                                |                        |
| Azure AI            |                                  |                  |                            |                                |                        |
| Determined.ai       |                                  |                  |                            |                                |                        |
| Databricks          |                                  |                  |                            |                                |                        |
