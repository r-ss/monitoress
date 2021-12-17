import os
from config import config

from entity import Entity
from entity_bc import EntityBC

from utils import send_message

from pydantic import BaseModel

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


        # self.add_entity(Entity('foldwrap, digitalocean', '167.172.164.135', uri='probe', look_for='resource', expected='fold', schema=ProbeBM, interval=5*60, important=True))
        self.add_entity(Entity('foldwrap, api', 'api.foldwrap.com', https=True, uri='info', look_for='resource', expected='info', schema=FoldWrapAPIBM, interval=5*60, important=True))
        self.add_entity(EntityBC('validators', config.VALIDATORS, interval=15*60, important=True))

        pass

    def add_entity(self, e:Entity):
        self.entities.append(e)

    
    def check_all(self) -> None:

        log('- - - - - - - - -')

        if self.paused:
            log('paused')
            return
        
        for index, e in enumerate(self.entities):

            ok = e.start_routine()
            if not ok:
                log(f'error happened with {e.name}')
                if e.important and config.TELEGRAM_ENABLED:
                    send_message(e.errors)
                    pass
                return

            # log(f'{e.name} ok')

