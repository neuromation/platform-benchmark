REGION ?= "us-east1"
BUCKET ?= "data-main"
JOB_NAME ?= "overview_$(shell date +%Y_%m_%d_%H_%M_%S)"
GOOGLE_APPLICATION_CREDENTIALS ?= "/home/george/Downloads/My First Project-77543fdc6ed9.json"


.PHONY: lint
lint:
	flake8 .
	mypy .


.PHONY: run
run:
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


.PHONY: local
local:
	GOOGLE_APPLICATION_CREDENTIALS=$(GOOGLE_APPLICATION_CREDENTIALS) python -m experiments.train \
	    --dataset-gs-path "gs://$(BUCKET)/cifar10" \
	    --logs-gs-path "gs://$(BUCKET)/logs"

# 	    --stream-logs \
