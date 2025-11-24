"""
Gunicorn Production Configuration
Multi-worker setup with Uvicorn worker class
"""

import multiprocessing
import os

# Server socket
bind = f"0.0.0.0:{os.getenv('PORT', '8000')}"
backlog = 2048

# Worker processes
# Formula: (2 x CPU cores) + 1
workers = int(os.getenv('WORKERS', 2 * multiprocessing.cpu_count() + 1))
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
max_requests = 10000  # Restart workers after N requests (prevent memory leaks)
max_requests_jitter = 1000  # Add randomness to prevent thundering herd
timeout = 120  # Worker timeout in seconds
keepalive = 5

# Logging
accesslog = "-"  # Log to stdout
errorlog = "-"  # Log to stderr
loglevel = os.getenv("LOG_LEVEL", "info").lower()
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "ruv-sparc-api"

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL (if needed)
keyfile = os.getenv("SSL_KEYFILE")
certfile = os.getenv("SSL_CERTFILE")

# Development/production settings
reload = os.getenv("ENVIRONMENT", "development") == "development"
reload_extra_files = []

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190


def on_starting(server):
    """
    Called just before the master process is initialized
    """
    server.log.info("🚀 Starting Gunicorn server...")
    server.log.info(f"📦 Workers: {workers}")
    server.log.info(f"🔧 Worker class: {worker_class}")
    server.log.info(f"🌐 Binding to: {bind}")


def on_reload(server):
    """
    Called when a worker is reloaded
    """
    server.log.info("🔄 Reloading workers...")


def when_ready(server):
    """
    Called just after the server is started
    """
    server.log.info("✅ Gunicorn server is ready. Accepting connections.")


def worker_int(worker):
    """
    Called when a worker receives the SIGINT or SIGQUIT signal
    """
    worker.log.info(f"🛑 Worker {worker.pid} received interrupt signal")


def pre_fork(server, worker):
    """
    Called just before a worker is forked
    """
    pass


def post_fork(server, worker):
    """
    Called just after a worker has been forked
    """
    server.log.info(f"👷 Worker spawned (pid: {worker.pid})")


def pre_exec(server):
    """
    Called just before a new master process is forked
    """
    server.log.info("🔄 Forking new master process...")


def when_ready(server):
    """
    Called just after the server is started
    """
    server.log.info(f"✅ Server is ready. Workers: {workers}")


def worker_exit(server, worker):
    """
    Called just after a worker has been exited
    """
    server.log.info(f"👋 Worker exited (pid: {worker.pid})")


def child_exit(server, worker):
    """
    Called just after a worker has been reaped
    """
    pass


def nworkers_changed(server, new_value, old_value):
    """
    Called just after num_workers has been changed
    """
    server.log.info(f"🔢 Workers changed from {old_value} to {new_value}")
