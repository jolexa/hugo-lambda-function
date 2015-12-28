#!/bin/bash

DIR=$(mktemp -d)
cd $DIR
pip install awscli -t .
wget https://raw.githubusercontent.com/aws/aws-cli/1.9.15/bin/aws \
	-O awscli.py
wget https://github.com/spf13/hugo/releases/download/v0.15/hugo_0.15_linux_amd64.tar.gz
tar -xf hugo_0.15_linux_amd64.tar.gz
rm -f hugo_0.15_linux_amd64.tar.gz
mv hugo_0.15_linux_amd64/hugo_0.15_linux_amd64 hugo_0.15_linux_amd64.go
rm -rf hugo_0.15_linux_amd64
# wget from repo here TODO
zip -9 /tmp/bundle.zip *
cd ..
zip -r9 /tmp/bundle.zip main.py
rm -rf $DIR
