"""
Central logging configuration.

Logs go to the console and to logs/app.log. The level can be changed with the
LOG_LEVEL environment variable (DEBUG, INFO, WARNING, ERROR).
"""

import logging
import logging.config
import os

LOG_DIR = os.getenv("LOG_DIR", "logs")
LOG_FILE = os.path.join(LOG_DIR, "app.log")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()


def setup_logging() -> None:
    """Configure console and rotating-file logging for the whole app."""
    os.makedirs(LOG_DIR, exist_ok=True)

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {
                    "format": "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "standard",
                    "level": LOG_LEVEL,
                },
                "file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "formatter": "standard",
                    "level": "DEBUG",
                    "filename": LOG_FILE,
                    "maxBytes": 1_000_000,
                    "backupCount": 3,
                    "encoding": "utf-8",
                },
            },
            "root": {"handlers": ["console", "file"], "level": "DEBUG"},
        }
    )
