#!/bin/bash
gunicorn myblog.wsgi:application -c /data/www/myblog/gunicorn.conf.py --daemon --reload

