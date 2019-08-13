CODE_PATH?=code/
DATA_PATH?=data/
NOTEBOOKS_PATH?=notebooks/

PROJECT_PATH_STORAGE?=storage:benchmark/
CODE_PATH_STORAGE?=$(PROJECT_PATH_STORAGE)$(CODE_PATH)
DATA_PATH_STORAGE?=$(PROJECT_PATH_STORAGE)$(DATA_PATH)
NOTEBOOKS_PATH_STORAGE?=$(PROJECT_PATH_STORAGE)$(NOTEBOOKS_PATH)
RESULTS_PATH_STORAGE?=$(PROJECT_PATH_STORAGE)$(RESULTS_PATH)

CODE_PATH_ENV?=/project/code/
DATA_PATH_ENV?=/project/data/
NOTEBOOKS_PATH_ENV?=/project/notebooks/
RESULTS_PATH_ENV?=/project/results/

TRAINING_NAME?=training
JUPYTER_NAME?=jupyter
TENSORBOARD_NAME?=tensorboard
FILEBROWSER_NAME?=filebrowser

BASE_ENV_NAME?=image:neuro/base

##### SETUP #####

.PHONY: setup
setup:
	echo "Not implemented!"

##### STORAGE #####

.PHONY: upload_code
upload_code:
	neuro cp -r $(CODE_PATH) $(CODE_PATH_STORAGE)

.PHONY: clean_code
clean_code:
	neuro rm -r $(CODE_PATH_STORAGE)

.PHONY: upload_data
upload_data:
	neuro storage load -pu $(DATA_PATH) $(DATA_PATH_STORAGE)

.PHONY: clean_data
clean_data:
	neuro rm -r $(DATA_PATH_STORAGE)

.PHONY: upload_notebooks
upload_notebooks:
	neuro cp -r $(NOTEBOOKS_PATH) $(NOTEBOOKS_PATH_STORAGE)

.PHONY: clean_notebooks
clean_notebooks:
	neuro rm -r $(NOTEBOOKS_PATH_STORAGE)

.PHONY: upload
upload: upload_code upload_data upload_notebooks

.PHONY: clean
clean: clean_code clean_data clean_notebooks

##### JOBS #####

.PHONY: run_training
run_training:
	echo "Not implemented!"

.PHONY: kill_training
kill_training:
	echo "Not implemented!"

.PHONY: connect_training
connect_training:
	echo "Not implemented!"

.PHONY: run_jupyter
run_jupyter:
	neuro run \
		--name $(JUPYTER_NAME) \
		--preset gpu-small \
		--http 8888 --no-http-auth --detach \
		--volume $(DATA_PATH_STORAGE):$(DATA_PATH_ENV):ro \
		--volume $(CODE_PATH_STORAGE):$(CODE_PATH_ENV):ro \
		--volume $(NOTEBOOKS_PATH_STORAGE):$(NOTEBOOKS_PATH_ENV):rw \
		--volume $(RESULTS_PATH_STORAGE):$(RESULTS_PATH_ENV):rw \
		$(BASE_ENV_NAME) \
		'jupyter notebook --no-browser --ip=0.0.0.0 --allow-root --NotebookApp.token= --notebook-dir=$(NOTEBOOKS_PATH_ENV)'
	neuro job browse $(JUPYTER_NAME)

.PHONY: kill_jupyter
kill_jupyter:
	neuro kill $(JUPYTER_NAME)

.PHONY: run_tensorboard
run_tensorboard:
	echo "Not implemented!"

.PHONY: kill_tensorboard
kill_tensorboard:
	echo "Not implemented!"

.PHONY: run_filebrowser
run_filebrowser:
	neuro run \
		--name $(FILEBROWSER_NAME) \
		--preset cpu-small \
		--http 80 --no-http-auth --detach \
		--volume $(PROJECT_PATH_STORAGE):/srv:rw \
		filebrowser/filebrowser
	neuro job browse $(FILEBROWSER_NAME)

.PHONY: kill_filebrowser
kill_filebrowser:
	neuro kill $(FILEBROWSER_NAME)

.PHONY: kill
kill: kill_training kill_jupyter kill_tensorboard kill_filebrowser

##### MISC #####

.PHONY: lint
lint:
	flake8 .
	mypy .

.PHONY: ps
ps:
	neuro ps
