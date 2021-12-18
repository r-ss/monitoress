import os
from pathlib import Path
from dotenv import load_dotenv


SECRETS_ENV_PATH = f'{Path.cwd()}/.env.secrets'
load_dotenv(dotenv_path=SECRETS_ENV_PATH)


# STORAGEROOT = '%s/storage/' % os.path.split(BASE_DIR)[0]

# import pytz
# TZ = pytz.timezone('Europe/Moscow')


class config:

    APP_NAME = 'monitoress'
    

    CHECKS_TICK_INTERVAL = 60

    # GENERAL SETTINGS AND HOSTS
    BASE_DIR: str = Path.cwd()
    PRODUCTION: bool = False
    DEBUG: bool = not PRODUCTION
    SECRET_KEY = str(os.environ.get('SECRET_KEY'))

    VALIDATORS = str(os.environ.get('VALIDATORS'))

    HOST = '0.0.0.0'
    PORT = 9004

    LOG_PATH = f'{Path.cwd()}/log.log'

    TELEGRAM_ENABLED = PRODUCTION  # Not send actual telegram messages if False
    NOTIFICATIONS_URL = str(os.environ.get('NOTIFICATIONS_URL'))
    
    
    # TESTS
    TESTING_MODE: bool = False  # Must be set to True only in autotests


    # FORMATTERS
    DATETIME_FORMAT_TECHNICAL: str = '%Y-%m-%d %H:%M:%S'
    DATETIME_FORMAT_HUMAN: str = '%d.%m.%Y %H:%M:%S'
    TIMEZONE_STRING = 'Europe/Moscow'
