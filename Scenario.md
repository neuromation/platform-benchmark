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


#### 3. Run a training script
```
gcloud ai-platform jobs submit training \
	    $(JOB_NAME) \
	    --scale-tier basic \
	    --package-path ./experiments \
	    --module-name experiments.train \
	    --region $(REGION) \
	    --staging-bucket gs://$(BUCKET) \
	    --python-version 3.5 \
	    --runtime-version 1.14 \
	    -- \
	    --dataset-gs-path "gs://$(BUCKET)/cifar10" \
	    --logs-gs-path "gs://$(BUCKET)/logs"
```
This command both uploads the code and runs it 

#### 4. Look at the training logs
* Authenticate in gcloud in order to give tensorboard an access to gstorage: `gcloud auth application-default login`
* Run TensorBoard: `tensorboard --logdir=gs://$BUCKET/logs/board`


#### 5. Visualize predictions
Google AI JupyterLab

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
* Create demo.ipynb in Google AI Platform JupyterLab Web interface
* Move demo.ipynb to google cloud
* Give public access: `gsutil acl -r ch -u AllUsers:R gs://data-main/for-demo`
* Share via [NBViwer](https://nbviewer.jupyter.org/urls/data-main.storage.googleapis.com/for-demo/demo.ipynb) 
