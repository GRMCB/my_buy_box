#!/bin/bash

sudo systemctl enable gunicorn-web
sudo systemctl restart gunicorn-web
sudo systemctl enable gunicorn-collector
sudo systemctl restart gunicorn-collector
sudo systemctl enable gunicorn-analyzer
sudo systemctl restart gunicorn-analyzer