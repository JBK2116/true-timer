"""
This module stores the global logging configuration dictionary
"""

import os
from typing import Any

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(BASE_DIR, "logs")

LOGGING_CONFIG: dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(name)s %(levelname)s %(message)s",
        }
    },
    "handlers": {
        "standard_timer": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOGS_DIR, "standard.log"),
            "maxBytes": 10485760, # 10MB
            "formatter": "json",
            "backupCount": 5,
        },
        "pomodoro_timer": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOGS_DIR, "pomodoro.log"),
            "maxBytes": 10485760,
            "formatter": "json",
            "backupCount": 5,
        },
        "interval_timer": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOGS_DIR, "interval.log"),
            "maxBytes": 10485760,
            "formatter": "json",
            "backupCount": 5,
        },
        "deep_timer": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOGS_DIR, "deep.log"),
            "maxBytes": 10485760,
            "backupCount": 5,
            "formatter": "json",
        },
        "console": {"class": "logging.StreamHandler", "formatter": "json"},
    },
    "loggers": {
        "standard": {
            "handlers": ["standard_timer", "console"],
            "level": "INFO",
            "propagate": False,
        },
        "pomodoro": {
            "handlers": ["pomodoro_timer", "console"],
            "level": "INFO",
            "propagate": False,
        },
        "interval": {
            "handlers": ["interval_timer", "console"],
            "level": "INFO",
            "propagate": False,
        },
        "deep": {
            "handlers": ["deep_timer", "console"],
            "level": "INFO",
            "propagate": False,
        }
    },
}