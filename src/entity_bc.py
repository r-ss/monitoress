import requests
from datetime import datetime

from log import log

from typing import Optional, List
from pydantic import BaseModel

class ValidatorStatusBM(BaseModel):
    validatorindex: int
    status: str

class ValidatorsBM(BaseModel):
    __root__: List[ValidatorStatusBM]  # __root__

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]


class EntityBC:

    urlbase = 'https://beaconcha.in/api/v1/validator/'
    errors_verbose = []
    # schema = None
    indexes_string = ''

    def __init__(self, name, indexes_string, interval = 10, important = False) -> None:
        self.name = name
        self.indexes_string = indexes_string
        self.fired = False
        self.failed = False
        self.interval = interval
        self.lastcheck = None
        self.important = important

    @property
    def url(self) -> str:
        return f'{self.urlbase}{self.indexes_string}'

    def add_error(self, error_description):
        log(error_description)
        self.failed = True
        self.errors_verbose.append(error_description)
    
    @property
    def errors(self) -> str:
        comb = '\n'.join(self.errors_verbose)
        return f'{self.name} - {comb}'

    def send_probe_request(self):
        # print(self.url)
        r = requests.get(self.url)
        self.fired = True
        return r

    def validate_response(self, validators) -> bool:
        if any(v.status != 'active_online' for v in validators):
            self.add_error(f'one or more status in not online for {self.name}')
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
                if data.json()['status'] == 'OK':
                    validators = ValidatorsBM.parse_obj(data.json()['data'])
                else:
                    self.add_error(f'json status for {self.name} is not ok')
            except Exception as ex:
                self.add_error(f'cannot parse probe for {self.name}')

        valid = None
        if not self.failed:
            try:
                valid = self.validate_response(validators)
            except Exception as ex:
                self.add_error(f'cannot validate {self.name}')


        if not self.failed and not valid:
            self.add_error(f'invalid probe {self.name}')

        if self.failed:
            return False

        self.lastcheck = datetime.now()
        log(f'{self.name} ok')

        return True

