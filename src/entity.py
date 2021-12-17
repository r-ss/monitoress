import requests
from datetime import datetime

from log import log


class Entity:

    errors_verbose = []
    schema = None

    def __init__(self, name, host, port=8999, uri='probe', look_for='resource', expected='dev-macbook', https=False, schema = None, interval = 10, important = False) -> None:
        self.name = name
        self.host = host
        self.port = port
        self.uri = uri
        self.look_for = look_for
        self.expected = expected
        self.fired = False
        self.failed = False
        self.https = https
        self.schema = schema
        self.interval = interval
        self.lastcheck = None
        self.importand = important # immediately send alerts about error if True

    @property
    def url(self) -> str:
        protocol = 'http'
        port = self.port

        if self.https:
            protocol = 'https'
            port = 443

        return f'{protocol}://{self.host}:{port}/{self.uri}'

    def add_error(self, error_description):
        log(error_description)
        self.failed = True
        self.errors_verbose.append(error_description)
    
    @property
    def errors(self) -> str:
        comb = '\n'.join(self.errors_verbose)
        return f'{self.name} - {comb}'

    def send_probe_request(self):
        r = requests.get(self.url)
        self.fired = True
        return r

    def validate_response(self, probe) -> bool:
        if probe.resource != self.expected:
            return False
        return True

    def start_routine(self):

        # skip if interval not reached
        if self.lastcheck:
            delta = datetime.now() - self.lastcheck
            delta_seconds = round(delta.total_seconds())
            if delta_seconds < self.interval:
                log(f'skip {self.name} because interval {self.interval} > {delta_seconds}')
                return True  # meand no error.. No error yet =)

        # skip if previous probe already failed
        if self.failed:
            log(f'skip already failed probe for {self.name}')
            return

        try:
            data = self.send_probe_request()
        except Exception as ex:
            self.add_error(f'cannot probe {self.name}')


        if not self.failed:
            try:
                probe = self.schema.parse_obj(data.json())
            except Exception as ex:
                self.add_error(f'cannot parse probe for {self.name}')

        valid = None
        if not self.failed:
            try:
                valid = self.validate_response(probe)
            except Exception as ex:
                self.add_error(f'cannot validate {self.name}')


        if not self.failed and not valid:
            self.add_error(f'invalid probe {self.name}')

        if self.failed:
            return False

        self.lastcheck = datetime.now()
        log(f'{self.name} ok')

        return True

