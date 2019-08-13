## Neuro Project Template 

_"The best is the enemy of the good." Voltaire_

This template aims to be a very basic starting point. 

Everything related to project documentation, remote debug, and CI/CD is out of scope.

### Docker image creation

```
git clone https://github.com/ufoym/deepo.git
cd deepo/generator
python generate.py Dockerfile tensorflow pytorch jupyter jupyterlab python==3.6
docker build -t neuro/base .
```

```
neuro image push neuro/base
```


### Docker folders contract

```
data/ -> /project/data/
code/ -> /project/code/
notebooks/ -> /project/notebooks/
logs and results -> /project/results/
```


### Project structure

```
code/ - a place for all code, including tests
  __init__.py - an empty file to keep this folder under Git
data/ - a place for the data
  .gitignore - a file excluding the content of this folder from Git
notebooks/ - a place for Jupyter notebooks
  .gitignore - an empty file to keep this folder under Git
requirements/ - a place for requirements, used by Makefile to setup environment
  apt.txt - a file with system requirements
  pip.txt - a file with pip requirements

.gitignore - standard Python exclusions + ML specific
Makefile - main entry point, to be described later
README.md - should include Makefile reference
setup.cfg - linter settings
```


### Makefile commands

#### Setup 
| Command | Scope | Purpose | Notes |
|---|---|---|---|
| setup | remote | install system and pip dependencies | ... |

#### Storage
| Command | Scope | Purpose | Notes |
|---|---|---|---|
| upload_code | remote | ... | use `cp` |
| clean_code | remote | ... | ... |
| upload_data | remote | ... | use `storage upload` |
| clean_data | remote | ... | ... |
| upload_notebooks | remote | ... | use `cp` |
| clean_notebooks | remote | ... | ... |
| upload | remote | upload everything (code, data, and notebooks) | ... |
| clean | remote | ... | ... |

#### Jobs
| Command | Scope | Purpose | Notes |
|---|---|---|---|
| run_training | remote | run training | run image and pass training command as parameter |
| kill_training | remote | kill training job | ... |
| connect_training | remote | connect to a training job with bash | ... |
| run_jupyter | remote | run Jupyter | run image with Jupyter and open browser |
| kill_jupyter | remote | kill Jupyter job | ... |
| run_tensorboard | remote | run Tensorboard | run Tensorboard in tersorflow/tensorflow and open browser |
| kill_tensorboard | remote | kill Tensorboard job | ... |
| run_filebrowser | remote | run Filebrowser | run Filebrowser in filebrowser/filebrowser and open browser |
| kill_filebrowser | remote | kill Filebrowser job | ... |
| kill | remote | kill all jobs | kill all of the above by name, ignoring errors |

#### Misc
| Command | Scope | Purpose | Notes |
|---|---|---|---|
| lint | local | ... | ... |
| ps | remote | look at the list of jobs | ... |


### Open questions and ideas

* How to create a directory on storage when copying everything?
* Do we need more local operations in Makefile?
* Is Keras included in tensorflow package or should we install it separately?
* Is Tensorboard included to the image we build with generator? 
If so, should we use our image instead of `tensorflow/tensorflow`?
* We can add SSH support in Docker; then we'll need to run a develop job 
and port-forward it.
