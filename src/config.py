import os
import pytz
import socket

from pathlib import Path

from pydantic_settings import BaseSettings


# from dotenv import load_dotenv

SECRETS_ENV_PATH = f"{Path.cwd()}/.env.secrets"
# load_dotenv(dotenv_path=SECRETS_ENV_PATH)


class AppConfig(BaseSettings):

    APP_NAME: str = "monitoress"
    BASE_DIR: str = str(Path.cwd())
    ENTRYPOINT: Path = Path("src/main.py")

    # mode switch
    PRODUCTION: bool = True
    if socket.gethostname() == "macbookpro":
        PRODUCTION = False

    DEBUG: bool = not PRODUCTION
    TESTING_MODE: bool = False  # Must be set to True only in autotests

    # secrets
    SECRET_KEY: str = None
    REDIS_PASS: str = None
    VALIDATORS: str = None
    NOTIFICATIONS_URL: str = None


    # server and deploy config
    HOST: str = "0.0.0.0"
    PORT: int = 9004
    SERVER_WATCH_FILES: bool = not PRODUCTION  # auto reload on source files change

    # logging setup, more in log.py
    LOG_FILE_PATH: str = f"{Path.cwd()}/logs/log.log"
    LOG_LEVEL: str = "DEBUG"

    # notifications
    TELEGRAM_ENABLED: bool = PRODUCTION  # Not send actual telegram messages if False
    NOTIFICATIONS_URL: str = str(os.environ.get("NOTIFICATIONS_URL"))

    CHECKS_TICK_INTERVAL: int = 10
    if PRODUCTION:
        CHECKS_TICK_INTERVAL = 60

    TURBO: bool = False  # make probes on every tick, ignoring probe interval settings
    if TURBO:
        CHECKS_TICK_INTERVAL = 5
        TELEGRAM_ENABLED = False
        DEBUG = True

    # formats
    DATETIME_FORMAT_TECHNICAL: str = "%Y-%m-%d %H:%M:%S"
    DATETIME_FORMAT_HUMAN: str = "%d.%m.%Y %H:%M:%S"
    # TIMEZONE_STRING = 'Europe/Moscow'
    TZ: pytz.BaseTzInfo = pytz.timezone("Europe/Madrid")

    class Config:
        """Loads the dotenv file."""

        env_file: str = str(SECRETS_ENV_PATH)

Config = AppConfig()