from __future__ import print_function

import json
import logging

import urllib
import zipfile
import subprocess

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    #logger.info("Event: " + str(event))
    message = json.loads(event['Records'][0]['Sns']['Message'])
    #logger.info("Message: " + str(message))

    repourl = message['repository']['url']
    reponame = message['repository']['name']

    logger.info("This is the URL: " + str(repourl))

    urllib.urlretrieve (repourl + "/archive/master.zip", "/tmp/master.zip")
    zfile = zipfile.ZipFile('/tmp/master.zip')
    zfile.extractall("/tmp/unzipped")
    builddir = "/tmp/unzipped/" + reponame + "-master/"

    subprocess.call("/var/task/hugo.go" , shell=True, cwd=builddir)
    pushdir = builddir + "public/"
    bucketuri = "s3://" + reponame + "/"
    subprocess.call("python /var/task/awscli.py s3 sync --size-only --delete --sse AES256 " + pushdir + " " + bucketuri, shell=True)
