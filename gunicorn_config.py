# Gunicorn configuration file
# Usage: gunicorn -c gunicorn_config.py myMemory.wsgi:application

import multiprocessing
import os

# Server socket
bind = "unix:/run/memory-slideshow.sock"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Logging
accesslog = "-"  # Log to stdout
errorlog = "-"   # Log to stderr
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "memory-slideshow"

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL (if needed, uncomment and configure)
# keyfile = "/path/to/keyfile"
# certfile = "/path/to/certfile"

