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


## Scenario Implementation for **[Floydhub](https://docs.floydhub.com/)**

### Main part

#### 0. User registration
* Instead of registration, you can use your `git` or `google` account
* After `floyd` client installed by `pip install floyd-cli`, you can
login with `floyd login` (this command will redirect you to the browser)


#### 1. Upload a dataset
* `cd $LOCAL_PATH_TO_CIFAR`
* `floyd data init cifar10`, where `cifar10` is the name of project 
* `floyd data upload`
* Now, you also can find your dataset in web version


#### 2. Upload the code
* `cd $PATH_TO_CODE`
* `floyd init benchmark`, where `benchmark` is the name of project 


#### 3. Run a training script
* To install requirements you just need to rename `requirements.txt` to `floyd_requirements.txt`
* `floyd run \
    --data bender/datasets/cifar10/1:/cifar10 \
    --env pytorch-1.0 \
    --follow \
    "python experiments/train.py --data_root /cifar10 --log_dir logs"`
* Now, you also can find your job in web version


#### 4. Look at the training logs
* `Tensorboard` runs automatically. Just open job's URL and click to tensorboard's link.
Note, that tensorboard is available only while training.


#### 5. Visualize predictions
You can run `jupyter` using UI, without command line:
* First of all, you need to create workspace in web UI
* Then open it and upload your code and model's checkpoint
* Also, you need to mount `cifar` dataset via UI
* Finally, after correcting paths in the `experiments/analyse_predict.ipynb` you can run it


#### 6. Run training again with increased weight for the worst class
* Since the code is stored locally, it can be easily changed
(in any editor or IDE) and added to git
* Then, you can run the code in the same way as in step 3


### Share and pick up results:

#### 1. Download a checkpoint
* Command `floyd output bender/projects/benchmark/10` open browser for you,
where you can download output data such as checkpoint.


#### 2. Share a checkpoint with other platform users
* You can share your checkpont with other users only if you upload it as `dataset`
* Thus, you firstly need to download the checkpoint as in step 1
* And upload it as dataset as in step 1 from main part


#### 3. Present a demo to non-engineers using Jupyter
* Unfortunately, you can't share your running notebook.
