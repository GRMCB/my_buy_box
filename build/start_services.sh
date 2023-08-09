#!/bin/bash

sudo systemctl enable gunicorn-web
sudo systemctl start gunicorn-web
sudo systemctl enable gunicorn-collector
sudo systemctl start gunicorn-collector