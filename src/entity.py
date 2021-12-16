class Entity:

    errors_verbose = []

    def __init__(self, name, host, port=8999, uri='probe', look_for='resource', expected='dev-macbook') -> None:
        self.name = name
        self.host = host
        self.port = port
        self.uri = uri
        self.look_for = look_for
        self.expected = expected
        self.fired = False
        self.failed = False
    

    @property
    def url(self) -> str:
        return f'http://{self.host}:{self.port}/{self.uri}'

    def add_error(self, error_description):
        self.failed = True
        self.errors_verbose.append(error_description)
    
    @property
    def errors(self) -> str:
        return '\n'.join(self.errors_verbose)

