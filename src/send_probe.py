from datetime import datetime
import os
import platform
# import subprocess

from fastapi import status
from fastapi_utils.cbv import cbv
from fastapi.responses import JSONResponse
from fastapi_utils.inferring_router import InferringRouter

from config import config

from entity import Entity

import requests

router = InferringRouter(tags=['General'])

from pydantic import BaseModel, UUID4, constr


class ProbeBM(BaseModel):
    resource: str
    random: str
    uptime: int

@cbv(router)
class SendProbeCBV:

    """ READ """
    @router.get('/send_probe', summary='Send Probe')
    def read(self):


        e = Entity('foldwrap, digitalocean', '167.172.164.135', expected='fold')

        r = requests.get(e.url)
        probe = ProbeBM.parse_obj(r.json())

        print(probe)
  
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                'client': config.APP_NAME,
                'time_client': datetime.now().strftime(config.DATETIME_FORMAT_HUMAN),
                'resource': probe.resource,
                'random': probe.random,
                'uptime': probe.uptime
            }
        )
