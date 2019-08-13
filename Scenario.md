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


## Scenario Implementation for **GPU-server on linux**

### Main part

#### 0. User registration
```
set REGION "us-east1"
set BUCKET_NAME "data-main"
```

#### 1. Upload a dataset
```
gsutil -m cp -r cifar10/ gs://$BUCKET_NAME/
<...>
[60.0k/60.0k files][129.4 MiB/129.4 MiB] 100% Done 181.1 KiB/s ETA 00:00:00   
Operation completed over 60.0k objects/129.4 MiB.
```


#### 2. Upload the code
* Connect to server: `ssh -p $PORT $USER@$IP`
* Change directory: `cd $PATH_TO_CODE`
* Get code: `git clone git@github.com:neuromation/platform_benchmark.git`


#### 3. Run a training script
* Install requirements: `pip install -r requirements.txt`
* Run training: `python experiments/train.py --log_dir $PATH_TO_LOGS --data_root $PATH_TO_CIFAR`


#### 4. Look at the training logs
* Run TensorBoard: `tensorboard --logdir=$PATH_TO_LOGS --port $TB_PORT`
* Start listening this port on your machine: `ssh -L $TB_PORT:localhost:$TB_PORT -p $PORT $USER@$IP`
* Open `http://localhost:$TB_PORT` in your browser and see the graphics.


#### 5. Visualize predictions
* Go to the code directory: `cd $PATH_TO_CODE`
* Run Jupyter: `jupyter notebook --no-browser --allow-root  --port $JUP_PORT`
* Start listening this port on your machine: `ssh -L $JUP_PORT:localhost:$JUP_PORT -p $PORT $USER@$IP`
* Open `http://localhost:$JUP_PORT` in your browser, copy & paste security token,
then go to `experiments/analyse_predict.ipynb` and check out the confusion matrix.


#### 6. Run training again with increased weight for the worst class
* Change the code a little bit (add a couple of strings to change weights in `experiments/trainer.py`).
* Add changes to `git` and push them to server.
* Run training again: `python experiments/train.py --log_dir $PATH_TO_LOGS --data_root $PATH_TO_CIFAR`

### Share and pick up results:

#### 1. Download a checkpoint
* `rsync -v -e "ssh -p $PORT" $USER@$IP:$PATH_TO_LOGS/last.ckpt $LOCAL_PATH_TO_CKPT`


#### 2. Share a checkpoint with other platform users
* `sudo chmod 777 $PATH_TO_LOGS/last.ckpt`


#### 3. Present a demo to non-engineers using Jupyter
* Go to the code directory: `cd $PATH_TO_CODE`
* Run Jupyter: `jupyter notebook --no-browser --allow-root  --port $JUP_PORT`
* Now you should add credentials of non-engineer members of your team to your server 
and ask them to start listening the corresponding port via 
`ssh -L $JUP_PORT:localhost:$JUP_PORT -p $PORT $NON_ENGINEER_USER@$IP`
* Then, they should open browser and go to `http://localhost:$JUP_PORT`
* Finally, they should run `experiments/demo.ipynb`
