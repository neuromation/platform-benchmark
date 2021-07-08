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


## Scenario Implementation for **Neuro Platform**

### Main part

#### 0. User registration
* Sign up at the [platform website](https://neu.ro).
* Install the platform CLI: `pip install -U neuromation`
* Login: `neuro login`


#### 1. Upload a dataset
* `neuro storage load -pr $LOCAL_PATH_TO_CIFAR storage:$PATH_TO_CIFAR`


#### 2. Upload the code
* `neuro cp -r $LOCAL_PATH_TO_CODE storage:$PATH_TO_CODE`


#### 3. Run a training script 
Here we will run a job based on a public Docker image, install our dependencies there, 
save it as a custom image, and use it for training and running Jupyter. 
* Run a job:
```
neuro run \
  --name setup \
  --preset cpu-small \
  --detach \
  --volume storage:$PATH_TO_CODE:/var/project:ro \
  ufoym/deepo:all-jupyter \
  'tail -f /dev/null'
```
* Enter this job: `neuro exec -t setup bash`
* Install our project requirements:
```
cd /var/project
pip install -r requirements.txt
exit
```
* Save the environment as a custom image: `neuro job save setup image:neuro:latest`
* Kill this job: `neuro kill setup`
* Run training script: 
```
neuro run \
  --name training \
  --preset gpu-small \
  --volume storage:$PATH_TO_CIFAR:/var/data:ro \
  --volume storage:$PATH_TO_CODE:/var/project:ro \
  --volume storage:$PATH_TO_LOGS:/var/results:rw \
  image:neuro:latest \
  'python /var/project/experiments/train.py --log_dir /var/results --data_root /var/data'
```
Note that this job will terminate automatically as soon as the training process is over.

#### 4. Look at the training logs 
* Run another job:
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
* Run a new job:
```
neuro run \
  --name jupyter \
  --preset gpu-small \
  --http 8888 --no-http-auth --detach \
  --volume storage:$PATH_TO_CIFAR:/var/data:ro \
  --volume storage:$PATH_TO_CODE:/var/project:ro \
  --volume storage:$PATH_TO_LOGS:/var/results:ro \
  image:neuro:latest \
  'jupyter notebook --no-browser --ip=0.0.0.0 --allow-root --NotebookApp.token= --notebook-dir=/var/project'
```
* Open Jupyter in browser: `neuro job browse training`, 
  go to `experiments/analyse_predict.ipynb`, and check out the confusion matrix.


#### 6. Run training again with increased weight for the worst class 
* Change the code a little bit (add a couple of strings to change weights in `experiments/trainer.py`).
* Re-upload the code: `neuro cp -r $LOCAL_PATH_TO_CODE storage:$PATH_TO_CODE`
* Re-run the training script:
```
neuro run \
  --name training \
  --preset gpu-large \
  --volume storage:$PATH_TO_CIFAR:/var/data:ro \
  --volume storage:$PATH_TO_CODE:/var/project:ro \
  --volume storage:$PATH_TO_LOGS:/var/results:rw \
  image:neuro:latest \
  'python /var/project/experiments/train.py --log_dir /var/results --data_root /var/data'
```


### Share and pick up results:

#### 1. Download a checkpoint
* `neuro cp storage:$PATH_TO_LOGS/last.ckpt $LOCAL_PATH_TO_CKPT`


#### 2. Share a checkpoint with other platform users 
* `neuro share storage:$PATH_TO_LOGS/last.ckpt $OTHER_USER read`


#### 3. Present a demo to non-engineers using Jupyter
* Get a link to the Jupyter which runs inside our `jupyter` job:
`neuro job status jupyter`, and share it with non-engineers.
* They should open it in browser and run `experiments/demo.ipynb`.
