## Scenario
We follow this scenario while working with each platform:
```
Main part:
0. User registration
1. Upload a dataset
2. Upload the code
3. Run a training script
4. Look at the training logs
5. Visualize predictions
6. Run training again with increased weight for the worst class

Share and pick up results:
1. Download a checkpoint
2. Share a checkpoint with other platform users
3. Present a demo to non-engineers using Jupyter
```


## Scenario Implementation for **Neuro Platform with remote debug**

### Main part

#### 0. User registration
* Sign up at the [platform website](https://neu.ro).
* Install the platform CLI: `pip install -U neuromation`
* Login: `neuro login`


#### 1. Upload a dataset
* `neuro storage load -pr $LOCAL_PATH_TO_CIFAR storage:$PATH_TO_CIFAR`


#### 2. Upload the code
* We use PyCharm Professional for the remote debug, so see next section.


#### 3. Run a training script
* Change a directory: `cd $LOCAL_PATH_TO_CODE`
* Build a Docker image: `docker build -t neuro:latest .`
* Upload this image to the platform: `neuro image push neuro:latest`
* Start a job: 
```
neuro run \
  --name training \
  --preset gpu-small \
  --http 8888 --no-http-auth --detach \
  --volume storage:$PATH_TO_CIFAR:/var/data:ro \
  --volume storage:$PATH_TO_CODE:/var/project:rw \
  --volume storage:$PATH_TO_LOGS:/var/results:rw \
  image:neuro:latest
```
* Expose the job SSH port: `neuro port-forward training 2222:22`
* In PyCharm Professional, add Python SSH Interpreter 
  with the following parameters:
```
Host: localhost
Port: 2222
Username: root
Interpreter: /usr/bin/python3.7
Sync folders: <Project Root>->/var/project
``` 
* Choose this interpreter as a project interpreter.
* In PyCharm Professional, add run Configuration for `experiments/train.py` script with the following 
 parameters: `--log_dir /var/results --data_root /var/data`
* Run this configuration. PyCharm now uploads source code to the Platform 
and runs training.


#### 4. Look at the training logs
* Start another job:
```
neuro run \
  --name tensorboard \
  --preset cpu-small \
  --http 6006 --no-http-auth --detach \
  --volume storage:$PATH_TO_LOGS:/var/results:rw \
  tensorflow/tensorflow \
  'tensorboard --logdir=/var/results'
```
* Open TensorBoard in browser: `neuro job browse tensorboard`, and see the graphics.


#### 5. Visualize predictions
* Jupyter is already started inside the first job, so all you have to do is
 to open it in browser: `neuro job browse training`, 
 go to `experiments/analyse_predict.ipynb`, and check out the confusion matrix.


#### 6. Run training again with increased weight for the worst class
* Change the code a little bit (add a couple of strings to change weights in `experiments/trainer.py`).
* Rerun training in PyCharm.


### Share and pick up results:

#### 1. Download a checkpoint
* `neuro cp storage:$PATH_TO_LOGS/last.ckpt $LOCAL_PATH_TO_CKPT`


#### 2. Share a checkpoint with other platform users
* `neuro share storage:$PATH_TO_LOGS/last.ckpt $OTHER_USER read`


#### 3. Present a demo to non-engineers using Jupyter
* Get a link to the Jupyter which runs inside our first job:
`neuro job status training`, and share it with non-engineers.
* They should open it in browser and run `experiments/demo.ipynb`.
