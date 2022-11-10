from typing import List, Optional, Union

from entity_api import EntityAPI
from entity_bc import EntityBC
from entity_ping import EntityPing

# from entity_test import EntityTest, EntityTestStatusBM

from utils import singleton

from pydantic import BaseModel

from log import log

from utils import run_parallel




class ProbeBM(BaseModel):
    resource: str
    random: str
    uptime: int


class FoldWrapAPIBM(BaseModel):
    resource: str
    datetime: str
    uptime: str

class EnergramAPIBM(BaseModel):
    resource: str
    datetime: str

# class RessBackupManagerBM(BaseModel):
#     resource: str
#     datetime: str
#     last_run: str
#     total_size_gb: str


# class TinkerboardBM(BaseModel):
#     resource: str
#     server: str


# class AKNotesBM(BaseModel):
#     resource: str
#     git_revision_hash: str
#     datetime: str


class TorrentDownloaderBM(BaseModel):
    resource: str
    git_revision_hash: str
    datetime: str
    redis_available: bool
    last_run: Optional[str]
    last_count: Optional[int]


@singleton
class ProbeManager:

    entities: List[Union[EntityAPI, EntityPing, EntityBC]] = []
    paused = False

    def __init__(self):

        self.bin = []

        # self.add_entity(Entity('foldwrap, digitalocean', '167.172.164.135', uri='probe', look_for='resource', expected='fold', schema=ProbeBM, interval=5*60))

        # self.add_entity(EntityTest("test_olny", interval=1 * 10, url="/nya/", look_for="status", expected="always true", schema=EntityTestStatusBM))

        self.add_entity(EntityPing("grani_microtic", interval=5 * 60, host="grani.ress.ws", expect_in_output="171.25.165.250"))
        # self.add_entity(EntityPing("ress.ws", interval=60 * 60, host="ress.ws", expect_in_output="167.172.164.135"))
        self.add_entity(EntityAPI("foldwrap_api", interval=15 * 60, url="http://api.foldwrap.com/info", look_for="resource", expected="info", schema=FoldWrapAPIBM))
        self.add_entity(EntityBC("validators", interval=20 * 60))

        self.add_entity(EntityAPI("energram_api", interval=15 * 60, url="http://energram-api.ress.ws/info", look_for="resource", expected="energram_prototype", schema=EnergramAPIBM))

        # ress_backup_manager = EntityAPI("ress_backup_manager", interval=30 * 60, url="http://grani.ress.ws:9003/info", look_for="resource", expected="ress_backup_manager", schema=RessBackupManagerBM)
        # ress_backup_manager.depends_on = ["grani_microtic"]
        # ress_backup_manager.extrafields = ["last_run", "total_size_gb"]
        # self.add_entity(ress_backup_manager)

        # self.add_entity(EntityAPI("eland_tinkerboard", interval=5 * 60, url="http://eland.ress.ws:8999/", look_for="resource", expected="tinkerboard", schema=TinkerboardBM))

        # self.add_entity(EntityAPI("ak_notes", interval=15 * 60, url="https://aknotes.ress.ws/info", look_for="resource", expected="ak_notes, info, CI/CD", schema=AKNotesBM))

        # self.add_entity(EntityAPI("torrent_downloader", interval=380 * 60, url="http://foldwrap.com:8666/info", look_for="resource", expected="torrent-downloader", schema=TorrentDownloaderBM, extrafields=["last_run", "last_count"]))
        self.add_entity(EntityAPI("torrent_downloader", interval=380 * 60, url="http://foldwrap.com:8666/info", look_for="resource", expected="torrent-downloader", schema=TorrentDownloaderBM))

    def add_entity(self, e: Union[EntityAPI, EntityPing]):
        self.entities.append(e)

    def get_entity_by_index(self, index):
        return self.entities[index]

    def is_dependencies_ok(self, entity: Union[EntityAPI, EntityPing]):
        if len(entity.depends_on):
            for name in entity.depends_on:
                for n in self.entities:
                    if name == n.name:
                        if n.status != "ok":
                            log(f"stop at dependency {name} for {entity.name}", level="debug")
                            return False
        return True

    async def check_one(self, e, force=False, get_from_cache=False):
        f, s = 0, 0
        if e.success_count:
            s = int(e.success_count)
        if e.fail_count:
            f = int(e.fail_count)

        ratio = 0.0
        if f + s > 0:
            ratio = s / (s + f)

        dependencies = None
        if e.depends_on:
            dependencies = e.depends_on

        if not get_from_cache:
            if not self.is_dependencies_ok(e):
                e.status = "skip"
                log(f"skip {e.name} because dependencies is not ok", level="debug")
                data = {"name": e.name, "type": e.type, "interval": e.interval, "lastcheck": e.lastcheck_formatted, "status": "skip", "info": "dependency"}
                self.bin.append(data)
                return

            await e.start_routine(force=force)

        data = {
            "name": e.name,
            "type": e.type,
            "interval": e.interval,
            "lastcheck": e.lastcheck_formatted,
            "status": e.status,
            "success_count": e.success_count,
            "fail_count": e.fail_count,
            "success_ratio": round(ratio, 4),
            "dependencies": dependencies,
            "extra": e.extra,
        }
        self.bin.append(data)
        return

    async def check_all(self, force=False):

        self.bin = []

        log(f"sending {len(self.entities)} probes...", level="debug")
        await run_parallel(*[self.check_one(e, force=force) for e in self.entities])
        return self.bin

    async def show_cached(self):

        self.bin = []

        log(f"getting {len(self.entities)} probes from cache...", level="debug")
        await run_parallel(*[self.check_one(e, get_from_cache=True) for e in self.entities])
        return self.bin
