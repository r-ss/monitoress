from datetime import datetime
import os
import platform
# import subprocess

from fastapi import status
from fastapi_utils.cbv import cbv
from fastapi.responses import JSONResponse
from fastapi_utils.inferring_router import InferringRouter

from config import config

from pydantic import BaseModel
import requests

from probe_manager import ProbeManager
pm = ProbeManager()

router = InferringRouter(tags=['General'])



class ProbeBM(BaseModel):
    resource: str
    random: str
    uptime: int

@cbv(router)
class SendProbeCBV:

    """ READ """
    @router.get('/send_probe', summary='Send Probe')
    def send_probe(self):


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

    @router.get('/get_probe/{probe_id}', summary='Get Probe')
    def get_probe(self, probe_id: str):

        pid = int(probe_id)
        e = pm.get_entity_by_index(pid)
        print(e)

        ok = e.start_routine()

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                'client': config.APP_NAME,
                'time_client': datetime.now().strftime(config.DATETIME_FORMAT_HUMAN),
                'entity_name': e.name,
                'status': ok,
                'success_count': e.success_count,
                'fail_count': e.fail_count
            }
        )
