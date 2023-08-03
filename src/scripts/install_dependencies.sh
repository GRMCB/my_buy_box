#!/bin/bash
sudo yum install python-pip -y
pip3 install virtualenv
pip3 install flask
pip3 install gunicorn
virtualenv -p python3 venv
source venv/bin/activate
pip3 freeze > requirements.txt
pip3 install -r requirements.txt
