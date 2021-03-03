#!/bin/bash


# chmod +x cluster.sh 
# sh cluster.sh

kind create cluster

kubectl apply -f yaml/pv-volume.yaml

kubectl apply -f yaml/pv-claim.yaml

n=0; until ((n >= 60)); do kubectl -n default get serviceaccount default -o name && break; n=$((n + 1)); sleep 1; done; ((n < 60))

kubectl apply -f yaml/pod.yaml

echo "Creating Container"

#n=0; until ((n >= 60)); do kubectl -n default get serviceaccount default -o name && break; n=$((n + 1)); sleep 1; done; ((n < 60))
#sleep 80
#echo "Complete: Verify with $ kubectl get pods"


