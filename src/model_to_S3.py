#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import subprocess
import boto3
import glob
import json
import os

###### FUNCTIONS ######
def get_plane_ID(containerPath):
    """
    Get container ID to copy over data from persistent volume
    """
    #static
    fn = "clusterID"

    # Remove old file if exists:
    if os.path.exists(fn):
        os.remove(fn)

    with open(fn, "a") as output:
        subprocess.call('docker inspect --format="{{.Id}}" kind-control-plane', shell=True, stdout=output, stderr=output)

    with open(fn, 'r') as file:
        ID = file.read().replace('\n', '')

    subprocess.call(f'docker cp {ID}:mnt/data {containerPath}', shell=True)


def getURL(s3_bucket, s3_key, s3_region):
    """
    Return a Pre-signed URL to enable Download of your S3 File:
    """
    session = boto3.session.Session(region_name=s3_region)
    s3Client = session.client('s3')
    url = s3Client.generate_presigned_url('get_object', 
                                          Params = {'Bucket': s3_bucket, 
                                                    'Key': s3_key},
                                          ExpiresIn = 100)
    return url

def upload_csv(model_data, s3_bucket, s3_key, s3_accessKey, s3_secretKey, s3_region):
    """
    Spin up S3 session and write model output data to:
    s3_bucket -> s3_Folder -> s3_key (folder path is prepended to s3_key)
    """
    session = boto3.Session(
        aws_access_key_id = s3_accessKey,
        aws_secret_access_key = s3_secretKey,
        region_name = s3_region)
    
    s3 = session.resource('s3')

    with open(model_data, 'rb') as data:
        s3.Object(s3_bucket, s3_key).put(Body=data)
        
    url = getURL(s3_bucket, s3_key, s3_region)
    print(f"{model_data} uploaded to {s3_bucket}: {s3_key} at:\n {url}")

    return

if __name__ == "__main__":

    ###### INITIALIZE ######
    wrkDir = os.getcwd()
    paramFile = f'{wrkDir}/init.json'
    with open(paramFile) as jf:
        init = json.load(jf)
    
    # Get model output into "data" folder 
    containerPath = "/data"
    get_plane_ID(containerPath)

    # Where we copy data from pv to container running this code...
    dataFolder = f"{containerPath}/*"

    s3_accessKey = init["s3_accessKey"]
    s3_secretKey = init["s3_secretKey"]
    s3_bucket = init["s3_bucket"]
    s3_keyFolder = init["s3_keyFolder"]
    s3_region = init["s3_region"]

    # Iterate over all files from model results
    for filepath in glob.iglob(fr'{dataFolder}'):
    
        model_data_file = filepath.split("/")[-1]
        s3_key = f"{s3_keyFolder}/{model_data_file }"
    
        print(f"Uploading {model_data}\n")
        upload_csv(model_data, s3_bucket, s3_key, s3_accessKey, s3_secretKey, s3_region)
