import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler

from config import config

rotating_file_handler = RotatingFileHandler(
    filename=config.LOG_FILE_PATH, 
    mode='a',
    maxBytes=1*1024,
    backupCount=1,
    encoding='utf-8',
    delay=0
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', datefmt=config.DATETIME_FORMAT_TECHNICAL, handlers=[rotating_file_handler])

def log(message:str) -> None:
    logging.info(message)
    dtf = datetime.now().strftime(config.DATETIME_FORMAT_HUMAN)
    s = f'{dtf} - {message}'
    print(s)