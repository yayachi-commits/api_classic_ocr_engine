"""Logging helpers used across the service."""

from __future__ import annotations

import logging
import os
from logging.config import dictConfig

_LOGGING_CONFIGURED = False


def setup_logging(level: str = "INFO") -> None:
    """Configure root logging once."""

    global _LOGGING_CONFIGURED
    if _LOGGING_CONFIGURED:
        return

    effective_level = "DEBUG" if os.getenv("LOGGER_DEBUG") else level.upper()
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "%(asctime)s :: %(name)s :: %(levelname)s :: %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                }
            },
            "root": {"handlers": ["console"], "level": effective_level},
        }
    )
    _LOGGING_CONFIGURED = True


def get_logger(name: str = "app") -> logging.Logger:
    """Return a logger by name."""
    return logging.getLogger(name)
