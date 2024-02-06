from datetime import datetime
import os
import platform
# import subprocess

from fastapi import status
from fastapi.responses import JSONResponse
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter

from config import Config

from ress_redis import RessRedisAbstraction

router = InferringRouter(tags=["General"])

redis = RessRedisAbstraction()


@cbv(router)
class InfoCBV:

    """READ"""

    @router.get("/api/info", summary="Basic system information")
    def read(self):
        """Return basic system information and variables, like is app runs
        in production mode or not. Might be useful on deployment.
        Can be used for fast status check in production

        access via /info url
        """

        # load1, load5, load15 = os.getloadavg()

        # def get_git_revision_short_hash() -> str:
        #     return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).decode("ascii").strip()

        # try:
        #     git_revision_hash = get_git_revision_short_hash()
        # except:
        #     git_revision_hash = "error"

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "resource": Config.APP_NAME,
                # "git_revision_hash": git_revision_hash,
                "datetime": datetime.now(Config.TZ).strftime(Config.DATETIME_FORMAT_HUMAN),
                "os": os.name,
                "platform": platform.system(),
                "platform_release": platform.release(),
                "python version": platform.python_version(),
                "testing": Config.TESTING_MODE,
                "production": Config.PRODUCTION,
                # "load averages": f"{load1:.2f} {load5:.2f} {load15:.2f}",
                # "redis_available": redis.ping(),
            },
        )
