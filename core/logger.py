# core/logger.py

import logging

def setup_logger(name="3DGod", level=logging.DEBUG, logfile="debug_log.txt"):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter('[%(asctime)s][%(levelname)s][%(name)s] %(message)s', datefmt='%H:%M:%S')

    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    fh = logging.FileHandler(logfile, encoding='utf-8')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger

log = setup_logger()
