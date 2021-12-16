import logging
from utils import get_script_path

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S', filename=f'{get_script_path()}/log.log', encoding='utf-8', level=logging.DEBUG)

def log(message:str) -> None:
    logging.info(message)
    print(message)