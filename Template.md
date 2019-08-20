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
data/ -> storage:{project_path}/data -> /project/data/
code/ -> storage:{project_path}/code -> /project/code/
notebooks/ -> storage:{project_path}/notebooks -> /project/notebooks/
requirements/ -> storage:{project_path}/requirements -> /project/requirements/
logs and results -> storage:{project_path}/results -> /project/results/
```


### Project structure

```
{project_name}/ - a place for all code, including tests
  __init__.py - an empty file to keep this folder under Git
data/ - a place for the data
  .gitignore - a file excluding the content of this folder from Git
notebooks/ - a place for Jupyter notebooks
  .gitignore - an empty file to keep this folder under Git
requirements/ - a place for requirements, used by Makefile to setup environment
  apt.txt - a file with system requirements
  pip.txt - a file with pip requirements

.gitignore - standard Python exclusions + ML specific
LICENCE - MIT licence
Makefile - the main entry point, to be described later
README.md - should include Makefile reference
setup.cfg - linter settings
setup.py - basic installation information
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
| download_notebooks | remote | ... | to keep notebooks synced | 
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
| run_tensorboard | remote | run TensorBoard | run TensorBoard in tersorflow/tensorflow and open browser |
| kill_tensorboard | remote | kill TensorBoard job | ... |
| run_filebrowser | remote | run FileBrowser | run FileBrowser in filebrowser/filebrowser and open browser |
| kill_filebrowser | remote | kill FileBrowser job | ... |
| kill | remote | kill all jobs | kill all of the above by name, ignoring errors |


#### Local
| Command | Scope | Purpose | Notes |
|---|---|---|---|
| setup_local | local | ... | setup requirements to make IDE happy |
| lint | local | ... | ... |
| install | local | ... | install a project locally using pip |


#### Misc
| Command | Scope | Purpose | Notes |
|---|---|---|---|
| ps | remote | look at the list of jobs | ... |


### TODOs

* TODO: add SSH support in Docker; then we'll need to run a `develop` job 
  and port-forward it; as inspiration use 
  https://github.com/neuromation/research-models/blob/master/synthetic-reverse/Dockerfile
* TODO: make a proper list of local commands (lint, install, etc).
* TODO: install apt dependencies in `setup`.
* TODO: how to fix this without creating a folder manually?
```
neuro cp -r benchmark storage:benchmark-test/benchmark
Copy 'file:///Users/mariyadavydova/projects/neuromation/platform_benchmark/benchmark' => 
  'storage://mariyadavydova/benchmark-test/benchmark'
ERROR: File not found ([Errno 2] No such directory: 
  'storage://mariyadavydova/benchmark-test')
```
* TODO: add a list of make commands (some kind of help?).
* TODO: make Jupyter notebooks in this benchmark to run.