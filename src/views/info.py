from datetime import datetime
import os
import platform
import subprocess

from fastapi import status
from fastapi_utils.cbv import cbv
from fastapi.responses import JSONResponse
from fastapi_utils.inferring_router import InferringRouter

from config import config

from ress_redis import RessRedisAbstraction

router = InferringRouter(tags=['General'])

redis = RessRedisAbstraction()

@cbv(router)
class InfoCBV:

    """ READ """
    @router.get('/info', summary='Basic system information')
    def read(self):
        """ Return basic system information and variables, like is app runs
            in production mode or not. Might be useful on deployment.
            Can be used for fast status check in production

            access via /info url
        """

        load1, load5, load15 = os.getloadavg()

        def get_git_revision_short_hash() -> str:
            return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('ascii').strip()

        try:
            git_revision_hash = get_git_revision_short_hash()
        except:
            git_revision_hash = 'error'

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                'resource': config.APP_NAME,
                'git_revision_hash': git_revision_hash,
                'datetime': datetime.now(config.TZ).strftime(config.DATETIME_FORMAT_HUMAN),
                'os': os.name,
                'platform': platform.system(),
                'platform_release': platform.release(),
                'python version': platform.python_version(),
                'testing': config.TESTING_MODE,
                'production': config.PRODUCTION,
                'load averages': f'{load1:.2f} {load5:.2f} {load15:.2f}',
                'redis_available': redis.ping()
            }
        )