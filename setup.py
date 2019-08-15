from distutils.core import setup

REQUIREMENTS = [
    'torchvision==0.2.2.post3',
    'torch==1.1.0',
    'tqdm==4.32.1',
    'matplotlib==3.0.3',
    'numpy==1.16.4',
    'tensorboardX==1.2',
    'requests==2.20.1',
    'scikit-learn==0.21.2',
]

setup(
    name='experiments',
    packages=['experiments'],
    install_requires=REQUIREMENTS,
)
