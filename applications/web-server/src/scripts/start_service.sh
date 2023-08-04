#!/bin/bash

sudo systemctl enable gunicorn-web
sudo systemctl start gunicorn-web

