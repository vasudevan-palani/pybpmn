"""Logging configuration
"""
config = {
    "version": 1,
    "disable_existing_loggers": False,
    "loggers": {
        "": {
            "handlers": ["streamHandler"],
            "level": "INFO",
            "propagate": True
        }
    },
    "handlers": {
        "streamHandler": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "jsonFormatter",
            "stream": "ext://sys.stdout"
        }
    },
    "formatters": {
        "jsonFormatter": {
            "format": "%(asctime)%(name)s%(levelname)%(filename)s%(lineno)d%(funcName)s%(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter"
        }
    }
}
