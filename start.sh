#!/bin/bash
source source venv/bin/activate
gunicorn myblog.wsgi:application -c /data/www/myblog/gunicorn.conf.py --daemon --reload

