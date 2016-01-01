#!/bin/bash

DIR=$(mktemp -d)
cd $DIR

# Install awscli python lib + deps in buildroot
pip install awscli -t .
# Fetch aws cli wrapper from github
wget https://raw.githubusercontent.com/aws/aws-cli/1.9.15/bin/aws \
	-O awscli.py
# Fetch hugo release (statically compile go binary)
wget https://github.com/spf13/hugo/releases/download/v0.15/hugo_0.15_linux_amd64.tar.gz
tar -xf hugo_0.15_linux_amd64.tar.gz
rm -f hugo_0.15_linux_amd64.tar.gz
mv hugo_0.15_linux_amd64/hugo_0.15_linux_amd64 hugo_0.15_linux_amd64.go
rm -rf hugo_0.15_linux_amd64
# cleanup
find . -name "*.pyc" -delete
# Fetch the main script from this repo
wget https://raw.githubusercontent.com/jolexa/hugo-lambda-function/master/main.py
# create zip
zip -r9 /tmp/hugo-lambda-function.zip *
cd ..
# cleanup
rm -rf $DIR
