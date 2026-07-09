import os
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler

BASE_DIR = Path(__file__).resolve().parent.parent

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "standard": {
            "format": "[{asctime}] {levelname} {name}: {message}",
            "style": "{",
        },
    },

    "handlers": {

        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },

        "file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": LOG_DIR / "app.log",
            "when": "midnight",
            "interval": 1,
            "backupCount": 30,
            "encoding": "utf-8",
            "formatter": "standard",
        },

        "error_file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": LOG_DIR / "error.log",
            "when": "midnight",
            "interval": 1,
            "backupCount": 30,
            "encoding": "utf-8",
            "formatter": "standard",
            "level": "ERROR",
        },
    },

    "root": {
        "handlers": [
            "console",
            "file",
            "error_file",
        ],
        "level": "INFO",
    },
}