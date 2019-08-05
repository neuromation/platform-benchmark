# Benchmark for platforms comparison


## Intro
This repository is an application for the comparison of machine learning platforms
which we made in [Neuromation](https://neu.ro). From our point of view, for
a fair comparison it is necessary to run the same typical task on each
participating platform.

In the `master` branch, you can find the code and commands required to run the task on
your local gpu server. For each platform, we created an additional branch so that you
can clearly see what commands and changes you need to apply to the project 
to run the proposed task.

**Disclaimer**. Please note that we do not use techniques to improve the accuracy of the model
(such as data augmentations, learning rate scheduling, etc), since our goal is to compare
platforms. As a result, we made the code as simple as possible.


## Task definition
As a benchmark, we propose to solve the task of images classification on
[CIFAR10](https://www.cs.toronto.edu/~kriz/cifar.html) dataset.
The dataset consists of 60000 32x32 color images in 10 classes,
with 6000 images per class. There are 50000 training images and 10000 test images. 

We have prepared images in `.png` format arranged in folders
[here](https://drive.google.com/open?id=1a-X4mZ5y6hQ0aX6-bNG6HU-Tfdom1lh6) [140 MB]. 
This dataset is also accessible by writing one line of code in
[pytorch](https://pytorch.org/docs/stable/torchvision/datasets.html#cifar),
but for the purpose of this comparison we work with data as if it was a 
custom dataset.

While working with each platform we follow a specific scenario 
and write down all our actions in [Scenario.md](Scenario.md)
(please, change a branch to see scenario implementation for each platform).


## Comparison results
At all points of comparison, we rated 0, 1, 2, or 3.

|                     | Setting up an environment | Data ingestion | Remote debugging | Sharing with engineers | Sharing with non-engineers | Sharing datasets and environments |
|---------------------|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|
| Neuro               |   1   |   2   |   2   |   3   |   3   |   3   |
| AWS SageMaker       |       |       |       |       |       |       |
| Google AI Platform  |       |       |       |       |       |       |
| Azure AI            |       |       |       |       |       |       |
| Floydhub            |       |       |       |       |       |       |
| Paperspace Gradient |       |       |       |       |       |       |
| Determined.ai       |       |       |       |       |       |       |
| Databricks          |       |       |       |       |       |       |
