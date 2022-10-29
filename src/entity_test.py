from entity import Entity
from pydantic import BaseModel



class EntityTestStatusBM(BaseModel):
    name: str = "test response"
    status: str = "always true"


class EntityTest(Entity):
    """ Used in autotests only """

    type = "test"

    def __init__(self, name, interval=10, important=True, expected="always true", schema=EntityTestStatusBM, extrafields=[]) -> None:
        super().__init__(name, interval, important)

        self.expected = expected
        self.schema = schema
        # self.url = url
        # self.extrafields = extrafields

    def validate_response(self, probe) -> bool:
        try:
            if probe.status == self.expected:
                return True
        except Exception as ex:
            self.add_error(f"cannot validate {self.name}")
        self.add_error(f"invalid probe {self.name}")
        return False

    def process_probe(self, data):
        return self.schema.parse_raw(data)

    async def send_probe_request(self):

        self.errors_verbose = []
        self.fired = True

        e = EntityTestStatusBM()
        r = e.json()

        return r

    def __repr__(self):
        return "EntityTest-obj-%s" % self.name
