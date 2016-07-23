from __future__ import print_function

import json
import logging
import boto3

import urllib
import zipfile
import tarfile
import subprocess
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    #logger.info("Event: " + str(event))
    message = json.loads(event['Records'][0]['Sns']['Message'])
    #logger.info("Message: " + str(message))

    repourl = message['repository']['url']
    reponame = message['repository']['name']
    logger.info("This is the URL: " + str(repourl))

    # Unzip the github repo
    logger.info("Fetching Repo: " + repourl + "/archive/master.zip" )
    urllib.urlretrieve(repourl + "/archive/master.zip", "/tmp/master.zip")
    zfile = zipfile.ZipFile('/tmp/master.zip')
    zfile.extractall("/tmp/unzipped")
    builddir = "/tmp/unzipped/" + reponame + "-master/"

    # Fetch hugo and call it
    logger.info("Fetching hugo")
    urllib.urlretrieve("https://github.com/spf13/hugo/releases/download/v0.15/hugo_0.15_linux_amd64.tar.gz", "/tmp/hugo.tar.gz")
    tfile = tarfile.open('/tmp/hugo.tar.gz')
    tfile.extractall("/tmp/hugo")
    logger.info("Running hugo")
    subprocess.call("/tmp/hugo/hugo_0.15_linux_amd64/hugo_0.15_linux_amd64" , shell=True, cwd=builddir)

    # push to s3
    logger.info("Pushing to s3")
    pushdir = builddir + "public/"
    bucketuri = "s3://" + reponame + "/"
    # Grr, I cannot believe there is no "sync" in boto3...https://github.com/boto/boto3/issues/358
    client = boto3.client('s3')
    os.chdir(pushdir)
    for root, dirs, files in os.walk('.'):
        for file in files:
            f=os.path.join(root,file)
            logger.info(f)
            logger.info("Pushing file: " + f + " to: " + bucketuri)
            body = open(f).read()


            reponse = client.put_object(
                Bucket=reponame,
                Body=body,
                Key=f.strip("./"),
                StorageClass='REDUCED_REDUNDANCY',
                ServerSideEncryption='AES256',
                #ContentEncoding=
                )
