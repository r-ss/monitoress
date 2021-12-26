import os
import pytz
import socket

from pathlib import Path
from dotenv import load_dotenv

SECRETS_ENV_PATH = f"{Path.cwd()}/.env.secrets"
load_dotenv(dotenv_path=SECRETS_ENV_PATH)


class config:

    APP_NAME = "monitoress"
    BASE_DIR: str = Path.cwd()
    ENTRYPOINT = Path("src/main.py")

    # mode switch
    PRODUCTION: bool = True
    if socket.gethostname() == "ress-mpb.local":
        PRODUCTION = False

    DEBUG: bool = not PRODUCTION
    TESTING_MODE: bool = False  # Must be set to True only in autotests

    # secrets
    SECRET_KEY = str(os.environ.get("SECRET_KEY"))

    # server and deploy config
    HOST = "0.0.0.0"
    PORT = 9004
    SERVER_WATCH_FILES = not PRODUCTION  # auto reload on source files change

    # logging setup, more in log.py
    LOG_FILE_PATH = f"{Path.cwd()}/logs/log.log"

    # notifications
    TELEGRAM_ENABLED = PRODUCTION  # Not send actual telegram messages if False
    NOTIFICATIONS_URL = str(os.environ.get("NOTIFICATIONS_URL"))

    CHECKS_TICK_INTERVAL = 10
    if PRODUCTION:
        CHECKS_TICK_INTERVAL = 60

    TURBO = False  # make probes on every tick, ignoring probe interval settings
    if TURBO:
        CHECKS_TICK_INTERVAL = 5
        # TELEGRAM_ENABLED = False
        DEBUG = True

    # formats
    DATETIME_FORMAT_TECHNICAL: str = "%Y-%m-%d %H:%M:%S"
    DATETIME_FORMAT_HUMAN: str = "%d.%m.%Y %H:%M:%S"
    # TIMEZONE_STRING = 'Europe/Moscow'
    TZ = pytz.timezone("Europe/Moscow")
