import logging

def setup_logger(name="3DGod", level=logging.DEBUG, logfile="debug_log.txt"):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Formatter mit Zeitstempel und Modul-Info
    formatter = logging.Formatter('[%(asctime)s][%(levelname)s][%(name)s] %(message)s', datefmt='%H:%M:%S')

    # Konsole
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Datei
    file_handler = logging.FileHandler(logfile, encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

# Globale Instanz
log = setup_logger()