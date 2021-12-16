import logging
from config import config

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S', filename=config.LOG_PATH, encoding='utf-8', level=logging.INFO)

def log(message:str) -> None:
    logging.info(message)
    print(message)