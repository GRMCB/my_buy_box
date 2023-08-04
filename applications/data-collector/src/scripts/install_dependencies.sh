#!/bin/bash
sudo yum install python-pip -y
pip3 install virtualenv
virtualenv -p python3 venv
source venv/bin/activate
pip3 install flask
pip3 install gunicorn
pip3 install apscheduler
pip3 freeze > requirements.txt
pip3 install -r requirements.txt
