
import os
import multiprocessing

#_scale_processes = 0.5
#_scale_threads = 0.5
_scale_processes = 2
_scale_threads = 10

workers = int( os.environ.get( "GUNICORN_PROCESSES" , multiprocessing.cpu_count( ) * _scale_processes + 1 ) )
threads = int( os.environ.get( "GUNICORN_THREADS" , multiprocessing.cpu_count( ) * _scale_threads + 1 ) )

timeout = int( os.environ.get( "GUNICORN_TIMEOUT" , "30" ) )
bind = os.environ.get( "GUNICORN_BIND" , "0.0.0.0:13031" )

loglevel = "info"
accesslog = "/local_data/container/access.log"
acceslogformat ="%(h)s %(l)s %(u)s %(t)s %(r)s %(s)s %(b)s %(f)s %(a)s"
errorlog = "/local_data/container/error.log"

pidfile = "/local_data/container/gunicorn.pid"

preload_app = True
#reload = True

forwarded_allow_ips = '*'

