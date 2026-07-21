"""Gunicorn configuration for production."""
import multiprocessing

bind = '127.0.0.1:8000'
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'
timeout = 120
graceful_timeout = 30
proc_name = 'blogwebsite'

accesslog = '/var/log/gunicorn/access.log'
errorlog = '/var/log/gunicorn/error.log'
loglevel = 'info'

user = 'www-data'
group = 'www-data'
