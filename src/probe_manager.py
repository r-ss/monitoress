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

class FoldWrapAPIBM(BaseModel):
    resource: str
    datetime: str
    uptime: str


class ProbeManager:

    entities = []
    paused = False

    def __init__(self):

        self.add_entity(Entity('foldwrap, digitalocean', '167.172.164.135', uri='probe', look_for='resource', expected='fold', schema=ProbeBM))
        self.add_entity(Entity('foldwrap, api', 'api.foldwrap.com', https=True, uri='info', look_for='resource', expected='info', schema=FoldWrapAPIBM))

        pass

    def add_entity(self, e:Entity):
        self.entities.append(e)

    def probe_entity(self, e:Entity) -> ProbeBM:
        # print(e.url)
        r = requests.get(e.url)
        return r

    def validate_response(self, e:Entity, probe:ProbeBM) -> bool:
        valid = True
        if probe.resource != e.expected:
            valid = False
        return valid

    def check_all(self) -> None:

        log('check_all')

        if self.paused:
            log('paused')
            return
        
        for index, e in enumerate(self.entities):

            # skip if previous probe already failed
            if e.failed:
                log(f'skip already failed probe for {e.name}')
                continue

            try:
                data = self.probe_entity(e)
            except Exception as ex:
                e.add_error(f'cannot probe {e.name}')


            if not e.failed:
                try:
                    probe = e.schema.parse_obj(data.json())
                except Exception as ex:
                    e.add_error(f'cannot parse probe for {e.name}')

            valid = None
            if not e.failed:
                try:
                    valid = self.validate_response(e, probe)
                except Exception as ex:
                    e.add_error(f'cannot validate {e.name}')


            if not e.failed and not valid:
                e.add_error(f'invalid probe {e.name}')

            if e.failed:
                # self.paused = True
                log(f'error happened with {e.name}')
                send_message(e.errors)
                return

            log(f'{e.name} ok')

