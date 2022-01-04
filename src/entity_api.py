from entity import Entity


class EntityAPI(Entity):

    type = "api"

    def __init__(self, name, interval=10, important=True, url=None, look_for="status", expected="ok", schema=None, extrafields=[]) -> None:
        super().__init__(name, interval, important)

        self.look_for = look_for
        self.expected = expected
        self.schema = schema
        self.url = url
        self.extrafields = extrafields

    def validate_response(self, probe) -> bool:
        try:
            if probe.resource == self.expected:
                return True
        except Exception as ex:
            self.add_error(f"cannot validate {self.name}")
        self.add_error(f"invalid probe {self.name}")
        return False

    def process_probe(self, data):
        try:
            probe = self.schema.parse_obj(data)
            for item in self.extrafields:
                self.extra[item] = dict(probe)[item]
        except Exception as ex:
            self.add_error(f"cannot parse probe for {self.name}")
            return None
        return probe

    def __repr__(self):
        return "EntityAPI-obj-%s" % self.name
