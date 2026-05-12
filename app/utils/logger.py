import logging
import os

LOG_DIR = "logs"

os.makedirs(LOG_DIR, exist_ok=True)

def setup_logger(name, filename):

    logger = logging.getLogger(name)

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )

    file_handler = logging.FileHandler(
        os.path.join(LOG_DIR, filename)
    )

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger