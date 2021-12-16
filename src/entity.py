from log import log

class Entity:

    errors_verbose = []
    schema = None

    def __init__(self, name, host, port=8999, uri='probe', look_for='resource', expected='dev-macbook', https=False, schema = None) -> None:
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

