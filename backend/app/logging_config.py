import logging
import os
from pythonjsonlogger import jsonlogger

def configure_logging():
    logger = logging.getLogger()
    logger.setLevel(os.getenv('LOG_LEVEL', 'INFO'))
    logHandler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s')
    logHandler.setFormatter(formatter)
    logger.handlers = [logHandler]
