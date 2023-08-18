#!/bin/bash
yum groupinstall "Development Tools"
yum install python3-devel
sudo python3.9 -m ensurepip --upgrade
python3.9 -m pip install virtualenv
sudo virtualenv -p python3.9 venv
source venv/bin/activate
pip3 install -r requirements.txt
export $PYTHONPATH=/var/www/webapp/applications/web-server/src/main/:/var/www/webapp/applications/web-server/src/main/:/var/www/webapp/applications/web-server/src/main/:/var/www/webapp/applications/data-collector/src/main/:/var/www/webapp/applications/data-analyzer/src/main/