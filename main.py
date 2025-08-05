#!python

import logging
import sys

from tiny_space.game import Game  # noqa: I900


class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    message = "%(levelname)s: %(message)s"

    FORMATS = {
        logging.DEBUG: grey + message + reset,
        logging.INFO: grey + message + reset,
        logging.WARNING: yellow + message + reset,
        logging.ERROR: red + message + reset,
        logging.CRITICAL: bold_red + message + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


# If you want to be spammed less choose a different logging level:
LEVELS = {
    "DEBUG": 10,
    "INFO": 20,
    "WARNING": 30,
    "ERROR": 40,
    "CRITICAL": 50,
}


try:
    arg = sys.argv[1]
    # Check for english log level (INFO, ERROR, etc).
    if not (LOG_LEVEL := LEVELS.get(arg.upper())):
        # Otherwise, assume int.
        LOG_LEVEL = int(arg)
except (IndexError, ValueError):
    # Default to INFO.
    LOG_LEVEL = 20

# Setting root logger is bad practice, too bad!
logger = logging.root
logger.setLevel(LOG_LEVEL)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(LOG_LEVEL)
ch.setFormatter(CustomFormatter())
logger.addHandler(ch)

Game()
