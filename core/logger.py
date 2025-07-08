import logging

def setup_logger(name="3DGod", level=logging.DEBUG, logfile="debug_log.txt"):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # 🛡️ Doppelte Handler verhindern
    if logger.hasHandlers():
        logger.handlers.clear()

    formatter = logging.Formatter('[%(asctime)s][%(levelname)s][%(name)s] %(message)s', datefmt='%H:%M:%S')

    # 📤 Konsole
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # 📁 Datei-Log
    fh = logging.FileHandler(logfile, encoding='utf-8')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger

# 📦 Globale Log-Instanz
log = setup_logger()

# ✅ Zusätzliche Methode: Erfolgsausgabe mit Emoji
def success(msg):
    log.info("✅ " + msg)

log.success = success