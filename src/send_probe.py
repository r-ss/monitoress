from datetime import datetime
import os
import platform
# import subprocess

from fastapi import status
from fastapi_utils.cbv import cbv
from fastapi.responses import JSONResponse
from fastapi_utils.inferring_router import InferringRouter

from config import config

router = InferringRouter(tags=['General'])


@cbv(router)
class SendProbeCBV:

    """ READ """
    @router.get('/send_probe', summary='Send Probe')
    def read(self):

        


        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                'resource': config.APP_NAME,
                'git_revision_hash': git_revision_hash,
                'datetime': datetime.now().strftime(config.DATETIME_FORMAT_HUMAN),
                'os': os.name,
                'platform': platform.system(),
                'platform_release': platform.release(),
                'python version': platform.python_version(),
                'testing': config.TESTING_MODE,
                'production': config.PRODUCTION,
                'load averages': f'{load1:.2f} {load5:.2f} {load15:.2f}'
            }
        )