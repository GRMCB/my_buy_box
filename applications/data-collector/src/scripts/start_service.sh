#!/bin/bash
cd /var/www/webapp/applications/data-collector/src/scripts/
source venv.sh
sudo systemctl enable gunicorn-collector
sudo systemctl start gunicorn-collector
