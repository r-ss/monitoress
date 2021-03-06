import asyncio
from typing import Any, Awaitable

# import os, sys
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from config import config


async def run_sequence(*functions: Awaitable[Any]) -> None:
    for function in functions:
        await function


async def run_parallel(*functions: Awaitable[Any]) -> None:
    await asyncio.gather(*functions)


async def subprocess_call(cmd: str):
    proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    return stdout, stderr


# def get_script_path():
#     return os.path.dirname(os.path.realpath(sys.argv[0]))


def send_message(message):
    if not config.TELEGRAM_ENABLED:
        return
    request = Request(
        config.NOTIFICATIONS_URL,
        urlencode({"message": message, "silent": False}).encode(),
    )
    # print(f'sending message{message}')
    response_json = urlopen(request).read().decode()
    return f'sended message "{message}"'


def bytes_to_human_readable_size(num, suffix="b"):
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


# Singleton - https://stackoverflow.com/questions/42237752/single-instance-of-class-in-python
def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton
