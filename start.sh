#!/bin/bash
source $PWD/venv/bin/activate
gunicorn myblog.wsgi:application -c $PWD/gunicorn.conf.py --daemon --reload

