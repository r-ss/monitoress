import requests
from datetime import datetime

from entity import Entity

from config import config
from log import log
from utils import send_message

import subprocess  # For executing a shell command


class EntityPing(Entity):

    type = 'ping'

    def __init__(self, name, interval=10, important=False, host=None) -> None:
        super().__init__(name, interval, important)

        self.host = host
        self.cmd = f"ping -c 1 {host}"

    def send_probe_request(self):
        self.errors_verbose = []
        self.fired = True
        try:
            output = subprocess.check_output(self.cmd, shell=True)
        except Exception as ex:
            print("exception")
            print(ex)
            return None
        return output

    def process_probe(self, output):

        try:
            probe = output.decode("utf-8")
        except Exception as ex:
            self.add_error(f"cannot process probe for {self.name}")
            return None
        return probe

    def __repr__(self):
        return "EntityAPI-obj-%s" % self.name

    def validate_response(self, probe) -> bool:
        try:
            # log(probe)
            if "64 bytes from 171.25.165.250" in probe:
                return True
        except Exception as ex:
            self.add_error(f"cannot validate {self.name}")
        self.add_error(f"invalid probe {self.name}")
        return False
