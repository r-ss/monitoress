import requests
from ress_redis import RessRedisAbstraction
from datetime import datetime

from log import log

redis = RessRedisAbstraction()

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

    """ success increment """
    @property
    def success_count(self) -> str:
        return redis.get(f'{self.name}_success_count')

    def success_increment(self):
        return redis.incr(f'{self.name}_success_count')

    """ fail increment """
    @property
    def fail_count(self) -> str:
        return redis.get(f'{self.name}_fail_count')

    def fail_increment(self):
        return redis.incr(f'{self.name}_fail_count')

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
        try:
            r = requests.get(self.url)
        except Exception as ex:
            self.add_error(f'cannot probe {self.name}')
            return None
        self.fired = True
        return r

    def validate_response(self, probe) -> bool:
        if not self.failed:
            try:
                if probe.resource == self.expected:
                    return True
            except Exception as ex:
                self.add_error(f'cannot validate {self.name}')
        self.add_error(f'invalid probe {self.name}')
        return False


    @property
    def is_too_early(self):
        if self.lastcheck:
            delta = datetime.now() - self.lastcheck
            delta_seconds = round(delta.total_seconds())
            if delta_seconds < self.interval:
                log(f'skip {self.name} because interval {self.interval} > {delta_seconds}')
                return True 
        return False
    
    def process_probe(self, data):
        try:
            probe = self.schema.parse_obj(data.json())
        except Exception as ex:
            self.add_error(f'cannot parse probe for {self.name}')
            return None
        return probe

    def commit_success(self):
        self.success_increment()

    def commit_fail(self):
        self.fail_increment()

    def start_routine(self):

        # skip if interval not reached
        if self.is_too_early:
            return True

        # # skip if previous probe already failed
        # if self.failed:
        #     log(f'skip already failed probe for {self.name}')
        #     return

        data = self.send_probe_request()
        if not data:
            self.commit_fail()
            return False

        probe = self.process_probe(data)
        if not probe:
            self.commit_fail()
            return False

        valid = self.validate_response(probe)

        # if not self.failed and not valid:
        #             self.add_error(f'invalid probe {self.name}')
        

        # if self.failed:
        #     return False

        self.lastcheck = datetime.now()
        log(f'{self.name} valid: {valid}')

        if not valid:
            self.commit_fail()
            return False

        self.commit_success()
        return valid

    def __repr__(self):
        return 'Entity-obj-%s' % self.name
