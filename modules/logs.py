import logging
import os
from logging.handlers import RotatingFileHandler

formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', datefmt='%H:%M:%S')


def setup_logger(name, level=logging.DEBUG):
    """Function setup as many loggers as you want"""
    if not os.path.exists('logs'):
        os.mkdir('logs')

    file_handler = logging.handlers.RotatingFileHandler('logs/%s.log' % name.split('.')[-1],
                                                        maxBytes=10000000,
                                                        backupCount=2)  # 10 Mb
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
