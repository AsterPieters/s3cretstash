#logger.py

import logging

def s3cretstashlogger():
    logging.basicConfig(
        encoding="utf-8",
        level=logging.DEBUG,
        format="{asctime} - {levelname} - {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M",
    )

    # Logger object
    logger = logging.getLogger(__name__)
    
    return logger
