#!/bin/bash
yum groupinstall "Development Tools"
yum install python3-devel
sudo python3.9 -m ensurepip --upgrade
python3.9 -m pip install virtualenv
sudo virtualenv -p python3.9 venv
source venv/bin/activate
sudo chmod 777 ../applications/data-collector/src/main/database
sudo chmod 777 ../applications/data-collector/src/main/database/database.db
sudo chmod 777 ../applications/data-analyzer/src/main/database
sudo chmod 777 ../applications/data-analyzer/src/main/database/analyzer_database.db
pip3 install -r requirements.txt