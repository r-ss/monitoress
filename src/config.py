from pathlib import Path
from dotenv import load_dotenv


SECRETS_ENV_PATH = f'{Path.cwd()}/.env.secrets'
load_dotenv(dotenv_path=SECRETS_ENV_PATH)


# STORAGEROOT = '%s/storage/' % os.path.split(BASE_DIR)[0]

# import pytz
# TZ = pytz.timezone('Europe/Moscow')


class config:

    APP_NAME = 'monitoress'

    # GENERAL SETTINGS AND HOSTS
    BASE_DIR: str = Path.cwd()
    PRODUCTION: bool = True
    DEBUG: bool = not PRODUCTION
    SECRET_KEY: str = None

    HOST = '0.0.0.0'
    PORT = 8667
    
    
    # TESTS
    TESTING_MODE: bool = False  # Must be set to True only in autotests


    # FORMATTERS
    DATETIME_FORMAT_TECHNICAL: str = '%Y-%m-%d %H:%M:%S'
    DATETIME_FORMAT_HUMAN: str = '%d.%m.%Y %H:%M'