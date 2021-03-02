# k8s
Run model in pod and put results on S3

WIP...


### Create Cluster

`kind create cluster`

### Build PV-VOLUME:

`kubectl apply -f pv-volume.yaml`

### Build Persistent Volume CLAIM

`kubectl apply -f pv-claim.yaml`

### Build Model Pod

`kubectl apply -f pod.yaml`

### Get PVC Docker Container ID:

`HHHMMMM!!!!????`

### Copy to local machine:

`docker cp <docker cont ID>:mnt/data /Users/travishartman/Desktop/test`

### Copy to S3:
Call model_to_S3.py container..
