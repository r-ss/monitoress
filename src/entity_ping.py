from entity import Entity
from utils import subprocess_call


class EntityPing(Entity):

    type = "ping"

    def __init__(self, name, interval=10, important=False, host=None, expect_in_output=None) -> None:
        super().__init__(name, interval, important)

        self.host = host
        self.cmd = f"ping -c 1 {host}"
        self.expect_in_output = expect_in_output

    async def send_probe_request(self):
        self.errors_verbose = []
        self.fired = True
        try:
            stdout, stderr = await subprocess_call(self.cmd)
        except Exception as ex:
            self.add_error(f"error with send_probe_request in EntityPing for {self.name}")
            return None
        return stdout

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
            if not self.expect_in_output:
                return True
            if self.expect_in_output in probe:
                return True
            else:
                self.add_error(f"expected output {self.expect_in_output} missed in EntityPing for {self.name}")
        except Exception as ex:
            self.add_error(f"cannot validate {self.name}")
        return False
