import logging
from config import config
from datetime import datetime

logging.basicConfig(format='%(asctime)s %(message)s', datefmt=config.DATETIME_FORMAT_HUMAN, filename=config.LOG_PATH, encoding='utf-8', level=logging.INFO)

def log(message:str) -> None:
    logging.info(message)
    dtf = datetime.now().strftime(config.DATETIME_FORMAT_HUMAN)
    s = f'{dtf} - {message}'
    print(s)