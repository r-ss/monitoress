from datetime import datetime

from fastapi import status
from fastapi_utils.cbv import cbv
from fastapi.responses import JSONResponse
from fastapi_utils.inferring_router import InferringRouter

from config import config

# from ress_redis import RessRedisAbstraction

from entity_test import EntityTest

router = InferringRouter(tags=["Test"])

# redis = RessRedisAbstraction()
from probe_manager import ProbeManager

pm = ProbeManager()

@cbv(router)
class SelftestCBV:

    """READ"""

    @router.get("/api/selftest", summary="Self test helper")
    async def read(self):

        pm.add_entity(EntityTest("test_only"))

        e = pm.get_entity_by_index(0)
        _ = await e.start_routine()

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "client": config.APP_NAME,
                "time_client": datetime.now(config.TZ).strftime(config.DATETIME_FORMAT_HUMAN),
                "entity_name": e.name,
                "status": e.status,
                "success_count": e.success_count,
                "fail_count": e.fail_count,
            },
        )
