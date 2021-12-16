class Entity:

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
