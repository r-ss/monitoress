from datetime import datetime

from fastapi import status
from fastapi.responses import JSONResponse
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter

from config import Config

from log import log

from pydantic import BaseModel

from probe_manager import ProbeManager

pm = ProbeManager()

router = InferringRouter(tags=["General"])


class ProbeBM(BaseModel):
    resource: str
    random: str
    uptime: int


@cbv(router)
class SendProbeCBV:
    @router.get("/api/probe/{probe_id}", summary="Get Probe")
    async def get_probe(self, probe_id: str):

        pid = int(probe_id)
        e = pm.get_entity_by_index(pid)
        # log(str(e))

        # ok = await e.start_routine()

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "client": Config.APP_NAME,
                "time_client": datetime.now(Config.TZ).strftime(Config.DATETIME_FORMAT_HUMAN),
                "entity_name": e.name,
                "status": e.status,
                "success_count": e.success_count,
                "fail_count": e.fail_count,
            },
        )

    @router.get("/api/all", summary="Get All Probes")
    async def get_all_probes(self):

        # probes = await pm.check_all(force=True)
        probes = await pm.show_cached()

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "client": Config.APP_NAME,
                "time_client": datetime.now(Config.TZ).strftime(Config.DATETIME_FORMAT_HUMAN),
                "probes": probes,
            },
        )
