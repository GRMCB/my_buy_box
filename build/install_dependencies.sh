#!/bin/bash
sudo yum install python-pip -y
pip3 install virtualenv
virtualenv -p python3.10 venv
source venv/bin/activate
pip3 install -r requirements.txt