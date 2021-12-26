# import os
# from config import config

from typing import Union

from entity_api import EntityAPI
from entity_bc import EntityBC
from entity_ping import EntityPing

from utils import singleton

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


class RessBackupManagerBM(BaseModel):
    resource: str
    datetime: str
    latest_full_backup_time: str


class TinkerboardBM(BaseModel):
    resource: str
    server: str


@singleton
class ProbeManager:

    entities = []
    paused = False

    def __init__(self):

        # self.add_entity(Entity('foldwrap, digitalocean', '167.172.164.135', uri='probe', look_for='resource', expected='fold', schema=ProbeBM, interval=5*60, important=True))

        self.add_entity(EntityPing("grani_microtic", interval=2 * 60, important=True, host="grani.ress.ws"))
        self.add_entity(EntityAPI("foldwrap_api", interval=5 * 60, important=True, url="http://api.foldwrap.com/info", look_for="resource", expected="info", schema=FoldWrapAPIBM))
        # self.add_entity(EntityBC("validators", interval=10 * 60, important=True))

        ress_backup_manager = EntityAPI("ress_backup_manager", interval=5 * 60, important=True, url="http://grani.ress.ws:9003/info", look_for="resource", expected="ress_backup_manager", schema=RessBackupManagerBM)
        ress_backup_manager.depends_on = ["grani_microtic"]

        self.add_entity(ress_backup_manager)
        self.add_entity(EntityAPI("eland_tinkerboard", interval=5 * 60, important=True, url="http://eland.ress.ws:8999/", look_for="resource", expected="tinkerboard", schema=TinkerboardBM))

        pass

    def add_entity(self, e: Union[EntityAPI, EntityBC, EntityPing]):
        self.entities.append(e)

    def get_entity_by_index(self, index):
        return self.entities[index]

    def is_dependencies_ok(self, entity: Union[EntityAPI, EntityBC, EntityPing]):
        if not entity.depends_on:
            return True
        if len(entity.depends_on):
            for name in entity.depends_on:

                for n in self.entities:
                    if name == n.name and n.failed:
                        log(f"found failed dependency {name} for {entity.name}")
                        return False
        return True

    def check_all(self) -> None:

        log("- - - - - - - - -")

        if self.paused:
            log("paused")
            return

        for index, e in enumerate(self.entities):

            if self.is_dependencies_ok(e):
                ok = e.start_routine()
            else:
                log(f"skip {e.name} because dependencies is not ok")

            # log(f'{e.name} ok')
