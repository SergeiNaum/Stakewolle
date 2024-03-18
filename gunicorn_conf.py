# import multiprocessing
#
#
# workers = multiprocessing.cpu_count() * 2 + 1
workers = 1
bind = "0.0.0.0:8000"
worker_class = "gthread"
accesslog = "-"  # Disable access to logging (it will be in stdout/stderr)
errorlog = "-"  # Disable logging error (it will also be in stdout/stderr)
capture_output = True  # Grab stdout/stderr

logconfig_dict = {
    "version": 1,
    "formatters": {
        "generic": {
            "format": "%(asctime)s [%(process)d] [%(levelname)s] %(message)s",
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
            "class": "logging.Formatter",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "generic",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "gunicorn.error": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
        "gunicorn.access": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}