# k8s
Run model in pod and put results on S3

WIP...


### Create Cluster

`kind create cluster`

### Build PV-VOLUME:

`kubectl apply -f yaml/pv-volume.yaml`

### Build Persistent Volume CLAIM

`kubectl apply -f yaml/pv-claim.yaml`

### Build Model Pod

`kubectl apply -f yaml/pod.yaml`

### OR run all:

`sh yaml/cluster.sh`

### Copy to S3:
Call model_to_S3.py container..