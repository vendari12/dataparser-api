import multiprocessing

bind = "0.0.0.0:8080"
timeout = 120
worker_class = "gevent"
workers = multiprocessing.cpu_count()
