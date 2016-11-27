#!/bin/bash

DIR=$(mktemp -d)
HUGO_VERSION=0.17

cd $DIR

# Install awscli python lib + deps in buildroot
pip install pyyaml awscli -t .

# Fetch aws cli wrapper from github
wget https://raw.githubusercontent.com/aws/aws-cli/1.11.21/bin/aws \
	-O awscli.py

# Fetch hugo release (statically compile go binary)
wget https://github.com/spf13/hugo/releases/download/v${HUGO_VERSION}/hugo_${HUGO_VERSION}_Linux-64bit.tar.gz
tar -xf hugo_${HUGO_VERSION}_Linux-64bit.tar.gz
rm -f hugo_${HUGO_VERSION}_Linux-64bit.tar.gz
mv hugo_${HUGO_VERSION}_linux_amd64/hugo_${HUGO_VERSION}_linux_amd64 hugo.go
rm -rf hugo_${HUGO_VERSION}_linux_amd64

# cleanup
find . -name "*.pyc" -delete

# Fetch the main script from this repo
wget https://raw.githubusercontent.com/jolexa/hugo-lambda-function/master/main.py

# create zip
zip -r9 /tmp/hugo-lambda-function.zip *
cd ..

# cleanup
rm -rf $DIR
