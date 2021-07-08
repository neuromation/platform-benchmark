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
* You have to create new account via Web UI, you can not use existed `git` or `google` accaunt.
Then you can login via `spell login` with created login and password.


#### 1. Upload a dataset
* `spell upload cifar.zip`
* `spell run -m uploads/cifar:cifar "unzip cifar/cifar.zip"`
* now we can observe our data via `spell ls runs/2/cifar/`

Or we can use new feature, but it took extremely long time for pending (most likely, unarchiving occurred at this time):
* `spell upload --compress cifar`


#### 2. Upload the code
* Code uploading is automatic


#### 3. Run a training script
* You can run training with via command:
```
spell run \
    --pip-req requirements.txt \
    -m uploads/cifar:/data \
    "python experiments/train.py --data_root /data --log_dir logs"
```
* This command will match your run with a special `run_id` (1, 2, 3 ...)


#### 4. Look at the training logs
* Utilization logs, training artefacts, tensorboard and text logs can be observed via Web UI
* For adding tensorboard to your project you must specify `--tensorboard-dir` in run parameters, tensorboard
will be available during the training
* Text logs can be observed using: `spell logs {run_id}`
* Also, artefacts can be found in `runs/{run_id}/logs`
* We try workaround for viewing tensorbord logs of finished job, but unsuccessfully. We tried the following command: 
 ```
spell run \
    --mount runs/10/logs/board:board/ \
    --tensorboard-dir board/ \
    'python -c "import time; time.sleep(3600)"'
```
, but get an error: `cannot mount into TensorBoard directory`.
So, the only one way to see this logs is download it to local machine and run tensorboard locally.


#### 5. Visualize predictions
* Command for running jupyter:
```
spell jupyter \
    --mount runs/10/logs/:data \
    --mount uploads/cifar/:dataset \
    --pip-req requirements.txt \
    cifar_workspace
```

#### 6. Run training again with increased weight for the worst class
* Just change the code locally, your next run will automatically upload last version of code to the server.
* Add changes to local `git` and push them to remote repository, if you want.


### Share and pick up results:

#### 1. Download a checkpoint
* `spell cp runs/{run_id}/logs/last.ckpt last.ckpt`


#### 2. Share a checkpoint with other platform users
* There is special command for sharing:
`spell link cifar_ckpt runs/{run_id}/logs/last.ckpt`, it's output is
`cifar_ckpt → runs/{run_id}/last.ckpt`. 
* Now, the link alias `cifar_ckpt` can be used in other Spell commands.


#### 3. Present a demo to non-engineers using Jupyter
* You can share a view-only version of a Notebook file (`.ipynb`) 
to users within your organization. To do this, navigate to the Files tab of your Workspace, 
find the `.ipynb` file you want to share, click the three dot action item on the right side
 of the row, and select Open as view only. You can now share this page with anyone with
  access to your Spell organization. (From `spell.run/docs.`)