#!/bin/bash

# export FLASK_APP=/var/www/webapp/src/app.py
# flask run --host=0.0.0.0 --port=8080

sudo systemctl enable gunicorn
sudo systemctl start gunicorn

