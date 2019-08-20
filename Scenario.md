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
* `make upload_data`


#### 2. Upload the code
* `make upload_code`


#### 3. Run a training script 
* `make setup`
* `make run_training`


#### 4. Look at the training logs 
* `make run_tensorboard`


#### 5. Visualize predictions 
* `make upload_notebooks`
* `make run_jupyter`
* Go to `experiments/analyse_predict.ipynb` and check out the confusion matrix.


#### 6. Run training again with increased weight for the worst class 
* Change the code a little bit (add a couple of strings to change weights in `experiments/trainer.py`).
* `make upload_code`
* `make run_training`


### Share and pick up results:

#### 1. Download a checkpoint
* `neuro cp $(RESULTS_PATH_STORAGE)/last.ckpt $(LOCAL_PATH_TO_CKPT)`


#### 2. Share a checkpoint with other platform users 
* `neuro share $(RESULTS_PATH_STORAGE)/last.ckpt $(OTHER_USER) read`


#### 3. Present a demo to non-engineers using Jupyter
* Get a link to the Jupyter which runs inside our `jupyter` job:
`neuro job status jupyter`, and share it with non-engineers.
* They should open it in browser and run `experiments/demo.ipynb`.
