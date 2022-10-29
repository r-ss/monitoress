import sys
from loguru import logger
from config import config

# logger.remove(0)
# logger.add(sys.stderr, format="<green>{time:YYYY-MM-DD at HH:mm:ss}</green> | <level>{message}</level>", colorize=True, backtrace=True, diagnose=True)
# logger.add(config.LOG_FILE_PATH, rotation="3 MB", retention="10 days", format="{time} {level} {message}")


logger.remove(0)
logger.add(sys.stderr, level=config.LOG_LEVEL, format="<green>{time:YYYY-MM-DD at HH:mm:ss}</green> | <level>{message}</level>", colorize=True)
logger.add(
    config.LOG_FILE_PATH,
    level="WARNING",
    rotation="1 MB",
    retention="10 days",
    format="{time:YYYY-MM-DD at HH:mm:ss} {level} {message}",
)


def log(message: str, level: str = "info") -> None:

    match level.lower():
        case "debug":
            logger.debug(message)
        case "warn" | "warning":
            logger.warning(message)
        case "error":
            logger.error(message)
        case _:
            logger.info(message)
