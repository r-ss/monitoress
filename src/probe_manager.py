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

# Singleton - https://stackoverflow.com/questions/42237752/single-instance-of-class-in-python
def singleton(cls, *args, **kw):
    instances = {}
    def _singleton():
       if cls not in instances:
            instances[cls] = cls(*args, **kw)
       return instances[cls]
    return _singleton

@singleton
class ProbeManager:

    entities = []
    paused = False

    def __init__(self):


        # self.add_entity(Entity('foldwrap, digitalocean', '167.172.164.135', uri='probe', look_for='resource', expected='fold', schema=ProbeBM, interval=5*60, important=True))
        self.add_entity(Entity('foldwrap_api', 'api.foldwrap.com', https=True, uri='info', look_for='resource', expected='info', schema=FoldWrapAPIBM, interval=5*60, important=True))
        self.add_entity(EntityBC('validators', config.VALIDATORS, interval=15*60, important=True))

        pass

    def add_entity(self, e:Entity):
        self.entities.append(e)

    def get_entity_by_index(self, index):
        return self.entities[index]

    
    def check_all(self) -> None:

        log('- - - - - - - - -')

        if self.paused:
            log('paused')
            return
        
        for index, e in enumerate(self.entities):

            ok = e.start_routine()
            if not ok:
                log(f'error happened with {e.name}')
                e.fail_increment()
                if e.important and config.TELEGRAM_ENABLED:
                    send_message(e.errors)
                return
            
            e.success_increment()

            # log(f'{e.name} ok')

