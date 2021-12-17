import os, sys
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from config import config

def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

def send_message(message):
    request = Request(config.NOTIFICATIONS_URL, urlencode({'message':message,'silent':False}).encode())
    response_json = urlopen(request).read().decode()
    return f'sended message "{message}"'

def bytes_to_human_readable_size(num, suffix="b"):
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"