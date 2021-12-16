from datetime import datetime
from config import config

from entity import Entity

import requests

from utils import send_message

from pydantic import BaseModel, UUID4, constr

from log import log

class ProbeBM(BaseModel):
    resource: str
    random: str
    uptime: int


class ProbeManager:

    entities = []
    paused = False

    def __init__(self):

        self.add_entity(Entity('foldwrap, digitalocean', '167.172.164.135', expected='fold'))

        pass

    def add_entity(self, e:Entity):
        self.entities.append(e)

    def probe_entity(self, e:Entity) -> ProbeBM:
        r = requests.get(e.url)
        return ProbeBM.parse_obj(r.json())

    def validate_response(self, e:Entity, probe:ProbeBM) -> bool:
        err = False
        if probe.resource != e.expected:
            err = True
        
        return err

    def check_all(self) -> None:

        log('check_all')

        if self.paused:
            return
        
        for index, e in enumerate(self.entities):

            try:
                probe = self.probe_entity(e)
            except Exception as ex:
                e.add_error('cannot probe')

            try:
                err = self.validate_response(e, probe)
            except Exception as ex:
                e.add_error('cannot validate')

            if err:
                e.add_error('invalid probe')

            if e.failed:
                self.paused = True
                send_message(e.errors)