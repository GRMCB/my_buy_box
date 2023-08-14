#!/bin/bash
sudo python3.9 -m ensurepip --upgrade
pip3 install virtualenv
sudo virtualenv -p python3.9 venv
source venv/bin/activate
pip3 install -r requirements.txt