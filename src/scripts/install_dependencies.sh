#!/bin/bash
sudo yum install python-pip -y

pip freeze > requirements.txt

pip3 install -r src/scripts/requirements.txt
