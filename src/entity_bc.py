import os
from typing import List
from pydantic import BaseModel, RootModel

from entity import Entity


class ValidatorStatusBM(BaseModel):
    validatorindex: int
    status: str


class ValidatorsBM(BaseModel):
    # __root__: List[ValidatorStatusBM]  # __root__
    RootModel: List[ValidatorStatusBM]

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]


class EntityBC(Entity):

    type = "beaconcha"

    def __init__(self, name, interval=10, important=True) -> None:
        super().__init__(name, interval, important)

        self.url = f"https://beaconcha.in/api/v1/validator/{os.environ.get('VALIDATORS')}"

    def process_probe(self, data):
        try:
            if data["status"] == "OK":
                validators = ValidatorsBM.parse_obj(data["data"])
            else:
                self.add_error("validators status received not OK")
                return None
        except Exception as ex:
            self.add_error(f"cannot parse validators for {self.name}")
            return None
        return validators

    def validate_response(self, validators) -> bool:
        try:
            if all(v.status == "active_online" for v in validators):
                return True
            else:
                self.add_error(f"one or more status in not online for {self.name}")
        except Exception as ex:
            self.add_error(f"cannot validate {self.name}")

        self.add_error(f"error with {self.name}")
        return False

    def __repr__(self):
        return "EntityBC-obj-%s" % self.name
