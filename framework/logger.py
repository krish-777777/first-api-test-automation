import logging
import os
from . import config

def _ensure_log_dir():
    os.makedirs(config.LOG_DIR, exist_ok=True)

def get_app_logger():
    _ensure_log_dir()
    logger = logging.getLogger("app")
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(os.path.join(config.LOG_DIR, "app.log"))
    ch = logging.StreamHandler()
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    fh.setFormatter(fmt); ch.setFormatter(fmt)
    logger.addHandler(fh); logger.addHandler(ch)
    return logger

def get_test_logger():
    _ensure_log_dir()
    logger = logging.getLogger("tests")
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(os.path.join(config.LOG_DIR, "tests.log"))
    ch = logging.StreamHandler()
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    fh.setFormatter(fmt); ch.setFormatter(fmt)
    logger.addHandler(fh); logger.addHandler(ch)
    return logger
