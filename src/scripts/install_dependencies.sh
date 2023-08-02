#!/bin/bash
virtualenv -p python3 venv
source venv/bin/activate
sudo yum install python-pip -y
pip3 freeze > requirements.txt
pip3 install -r requirements.txt
