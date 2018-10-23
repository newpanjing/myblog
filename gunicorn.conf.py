import multiprocessing

bind = "127.0.0.1:8001"
workers = multiprocessing.cpu_count() * 2 + 1  # workers是工作进程数
threads = 2  # 指定每个进程开启的线程数
errorlog = '/data/www/myblog/gunicorn.error.log'
accesslog = './gunicorn.access.log'
loglevel = 'info'
proc_name = 'gunicorn_blog_project'
