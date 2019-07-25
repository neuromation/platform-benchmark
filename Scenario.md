## Scenario
We will follow a common scenario when working with each platform:
```
Main part:
0. User registration
1. Upload dataset
2. Upload code
3. Run training script
4. Look at the training logs
5. Visualize predictions
6. Run training again with more weight of worst class

Share and pick up results:
1. Download checkpoint
2. Share checkpoint with other platform's users
3. Present demo to non-engineers using jupyter
```


## Scenario Implementation for **GPU-server on linux**

### Main part

#### 0. User registration
* It assumed, that user's credentials already added to your server.


#### 1. Upload dataset
* `rsync -rv -e "ssh -p $PORT" $USER@$IP:$PATH_TO_CIFAR $LOCAL_PATH_TO_CIFAR`


#### 2. Upload code
* Connect to server via `ssh -p $PORT $USER@$IP`,
* than change directory `cd $PATH_TO_CODE`
* and `git clone git@github.com:neuromation/platform_benchmark.git`.


#### 3. Run training script
* Install requirements via `pip install -r requirements.txt`,
* than `python experiments/train.py --log_dir $PATH_TO_LOGS --data_root $PATH_TO_CIFAR`


#### 4. Look at the training logs
* Run tensorboard using `tensorboard --logdir=$PATH_TO_LOGS --port $TB_PORT`,
* than start listening this port on your macheine `ssh -L $TB_PORT:localhost:$TB_PORT -p $PORT $USER@$IP`.
* Finally, open `http://localhost:$TB_PORT` in your browser and see graphics


#### 5. Visualize predictions
* Go to code directory via `cd $PATH_TO_CODE`,
* run jupyter `jupyter notebook --no-browser --allow-root  --port $JUP_PORT`
* and start listening this port on your machine `ssh -L $JUP_PORT:localhost:$JUP_PORT -p $PORT $USER@$IP`
* Finally, open `http://localhost:$JUP_PORT` in your browser, copy & paste security token,
than go to `experiments/analyse_predict.ipynb`.


#### 6. Run training again with more weight of worst class.
* Change code a little bit (add few strings for weights)
* Add changes to `git` and push them to server
* Run train again `python experiments/train.py --log_dir $PATH_TO_LOGS --data_root $PATH_TO_CIFAR`

### Share and pick up results:

#### 1. Download checkpoint
* `rsync -v -e "ssh -p $PORT" $USER@$IP:$PATH_TO_LOGS/last.ckpt $LOCAL_PATH_TO_CKPT`

#### 2. Share checkpoint with other users.
* `sudo chmod 777 $PATH_TO_LOGS/last.ckpt`


#### 3. Present demo to non-engineers using jupyter
* Go to code directory via `cd $PATH_TO_CODE`,
* run jupyter `jupyter notebook --no-browser --allow-root  --port $JUP_PORT`
* Now you need to add credentials of your non engineer member to your server and 
ask him to start listening port via `ssh -L $JUP_PORT:localhost:$JUP_PORT -p $PORT $NON_ENGINEER_USER@$IP`
* Than, he needs to open browser and go to `http://localhost:$JUP_PORT`
* Finally, he needs to open `experiments/demo.ipynb`
