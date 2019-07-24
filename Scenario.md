## Scenario
We will follow a common scenario when working with each platform:
```
Main part:
0. User registration.
1. Upload dataset.
2. Upload code.
3. Run training script.
4. Look at the training logs.
5. Visualize predictions.
6. Run train again with more weight of worst class.

Share and pick up results:
1. Download checkpoint.
2. Share checkpoint with other platform's users.
3. Share trained model with non specialists using jupyter.
```


## Scenario Implementation for **GPU-server on linux**

#### 0. User registration
It assumed, that user's credentials already added to server.


#### 1. Upload dataset
`rsync -rv -e "ssh -p $PORT" $USER@$IP:$PATH_TO_CIFAR $LOCAL_PATH_TO_CIFAR`


#### 2. Upload code
* Connect to server via `ssh -p $PORT $USER@$IP`,
* than change directory `cd $PATH_TO_CODE`
* and `git clone git@github.com:neuromation/platform_benchmark.git`.


#### 3. Run training script
* Install requirements via `pip install -r requirements.txt`,
* than `python train.py --log_dir $PATH_TO_LOGS --data_root $PATH_TO_CIFAR`


#### 4. Look at the training logs
* Run tensorboard using `tensorboard --logdir=$PATH_TO_LOGS --port $TB_PORT`,
* than start listening this port on your macheine `ssh -L $TB_PORT:localhost:$TB_PORT -p $PORT $USER@$IP`.
* Finally, open `http://localhost:$TB_PORT` in your browser and see graphics.


#### 5. Visualize predictions
