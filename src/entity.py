# from typing import Union

# import requests

from ress_redis import RessRedisAbstraction
from datetime import datetime

from config import config
from log import log
from utils import send_message

from emoji import emojize

import aiohttp

redis = RessRedisAbstraction()


class ProbeRequestError(Exception):
    """Custom error on probe requests"""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)

    """ Usage: raise ProbeRequestError(message="shit happened") """


class Entity:

    type = "general"

    def __init__(self, name, interval=10, important=True) -> None:

        self.name = name
        self.interval = interval
        self.important = important  # immediately send alerts about error if True
        self.lastcheck = None
        self.fired = False
        self.fail_notification_sended = False
        self.failed = False
        self.redis_fields = {
            "success_count": f"{self.name}_success_count",
            "fail_count": f"{self.name}_fail_count",
        }
        self.errors_verbose = []
        self.depends_on = []
        self.status = "unknown"
        self.extra = {}

    @property
    def lastcheck_formatted(self) -> str:
        if not self.lastcheck:
            return ""
        return self.lastcheck.strftime(config.DATETIME_FORMAT_HUMAN)

    """ success increment """

    @property
    def success_count(self) -> str:
        return redis.get(self.redis_fields["success_count"])

    def success_increment(self):
        return redis.incr(self.redis_fields["success_count"])

    def success_reset(self):
        return redis.set(self.redis_fields["success_count"], 0)

    """ fail increment """

    @property
    def fail_count(self) -> str:
        return redis.get(self.redis_fields["fail_count"])

    def fail_increment(self):
        return redis.incr(self.redis_fields["fail_count"])

    def fail_reset(self):
        return redis.set(self.redis_fields["fail_count"], 0)

    def add_error(self, error_description):
        log(error_description, level="error")
        self.failed = True
        self.errors_verbose.append(error_description)

    @property
    def errors(self) -> str:
        return "\n".join(self.errors_verbose)

    @property
    def error_notification_text(self) -> str:
        return f"{emojize(':warning:')} {self.name}\n{self.errors}"

    @property
    def is_too_early(self):
        if config.TURBO:
            return False
        if self.lastcheck:
            delta = datetime.now(config.TZ) - self.lastcheck
            delta_seconds = round(delta.total_seconds())
            if delta_seconds < self.interval:
                return True
        return False

    async def send_probe_request(self):

        # log("making connection...", level="debug")
        # await asyncio.sleep(2.5)

        self.errors_verbose = []
        self.fired = True
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url, timeout=10) as resp:
                    r = await resp.json()
        except aiohttp.ClientConnectionError as err:
            self.add_error(f"aiohttp ClientError with {self.name}")
            return None
        # except aiohttp.HTTPServerError as err:
        #     self.add_error(f"aiohttp HTTPServerError with {self.name}")
        #     return None
        except Exception as err:
            self.add_error(f"Send probe error for {self.name}")
            return None
        return r

    def commit_success(self):
        self.success_increment()
        if self.failed and self.fail_notification_sended:
            msg = f"{emojize(':shamrock:')} {self.name} back to normal"
            send_message(msg)
            self.fail_notification_sended = False
        self.failed = False
        self.status = "ok"

    def commit_fail(self):
        # log('commit fail')
        self.failed = True
        self.fail_increment()
        self.status = "error"
        log(f"Error happened with {self.name}", level="error")
        if self.important and not self.fail_notification_sended:
            send_message(self.error_notification_text)
            self.fail_notification_sended = True

    async def start_routine(self, force=False):

        # skip if interval not reached
        if self.is_too_early and not force:
            log(f"skip {self.name} because interval not reached", level="debug")
            return True

        self.lastcheck = datetime.now(config.TZ)

        data = await self.send_probe_request()
        if not data:
            self.commit_fail()
            return False

        probe = self.process_probe(data)
        if not probe:
            self.commit_fail()
            return False

        valid = self.validate_response(probe)

        log(f"{self.name} valid: {valid}")

        if not valid:
            self.commit_fail()
            return False

        self.commit_success()
        return valid

    @property
    def nomnoml_block(self):
        """returns string in momnoml syntax for represent block on web"""
        """ [<green> grani_microtic5  |   status: ok, 14:35  |  last fail: 27.12.2021, 14:05] """

        color = "<green>"
        if self.failed:
            color = "<red>"
        return f"[{color} {self.name}  |  type: {self.type}  |  status: {self.status}  |  last check: {self.lastcheck_formatted}]\n"

    def __repr__(self):
        return "Entity-obj-%s" % self.name
