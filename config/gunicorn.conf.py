import multiprocessing

# see http://docs.gunicorn.org/en/latest/settings.html
errorlog="gunicorn-error.log"
accesslog="gunicorn-access.log"
worker_class='gevent'
bind='0.0.0.0:5000'
workers = multiprocessing.cpu_count() * 2 + 1
threads = multiprocessing.cpu_count() * 2
debug = False
loglevel = 'DEBUG'
reload = False
daemon = False
