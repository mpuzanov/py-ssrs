# модуль создания логера

import logging
from logging.handlers import RotatingFileHandler

_log_format = f"%(asctime)s - [%(levelname)s] - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
_log_format_short = f"%(asctime)s - [%(levelname)s] - %(message)s"


def get_file_handler(path, log_level: int = 10):
    file_handler = logging.FileHandler(path, encoding='utf-8', mode='a')  # mode='w'
    file_handler.setLevel(log_level)  # logging.DEBUG
    file_handler.setFormatter(logging.Formatter(_log_format))
    return file_handler


def get_rotating_file_handler(path, log_level: int = 10):
    file_handler = RotatingFileHandler(
        path, maxBytes=20000, backupCount=5, encoding='utf-8', mode='w')
    file_handler.setLevel(log_level)  # logging.DEBUG
    file_handler.setFormatter(logging.Formatter(_log_format))
    return file_handler


def get_stream_handler(log_level: int = 20):
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)  # logging.INFO
    stream_handler.setFormatter(logging.Formatter(_log_format_short))
    return stream_handler


def get_logger(name, log_level='DEBUG', path="app.log"):
    logger = logging.getLogger(name)

    log_levels = {
        'CRITICAL': logging.CRITICAL,
        'FATAL': logging.FATAL,
        'ERROR': logging.ERROR,
        'WARN': logging.WARNING,
        'WARNING': logging.WARNING,
        'INFO': logging.INFO,
        'DEBUG': logging.DEBUG,
    }
    level = log_levels.get(log_level.upper(), logging.DEBUG)
    logger.setLevel(level)
    logger.addHandler(get_file_handler(path, level))
    logger.addHandler(get_stream_handler(level))
    return logger
