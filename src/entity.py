import requests
from ress_redis import RessRedisAbstraction
from datetime import datetime

from config import config
from log import log
from utils import send_message

from emoji import emojize


redis = RessRedisAbstraction()


class Entity:
    def __init__(self, name, interval=10, important=False) -> None:

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
        self.depends_on = None

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
        log(error_description)
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
                log(f"skip {self.name} because interval {self.interval} > {delta_seconds}")
                return True
        return False

    def send_probe_request(self):
        self.errors_verbose = []
        self.fired = True
        try:
            r = requests.get(self.url, timeout=10)
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            self.add_error(f"HTTPError with request {self.name}")
            return None
        except requests.exceptions.ConnectionError as err:
            self.add_error(f"ConnectionError with request {self.name}")
            return None
        except requests.exceptions.ReadTimeout as err:
            self.add_error(f"TimeoutError with request {self.name}")
            return None
        except requests.exceptions.RequestException as err:
            self.add_error(f"Сannot probe {self.name}")
            return None
        return r

    def commit_success(self):
        self.success_increment()
        if self.failed:
            msg = f"{emojize(':shamrock:')} {self.name} back to normal"
            send_message(msg)
        self.failed = False
        self.fail_notification_sended = False

    def commit_fail(self):
        self.failed = True
        self.fail_increment()
        log(f"error happened with {self.name}")
        if self.important and not self.fail_notification_sended:
            send_message(self.error_notification_text)
            self.fail_notification_sended = True

    def start_routine(self):

        # skip if interval not reached
        if self.is_too_early:
            return True

        data = self.send_probe_request()
        if not data:
            self.commit_fail()
            return False

        probe = self.process_probe(data)
        if not probe:
            self.commit_fail()
            return False

        valid = self.validate_response(probe)

        self.lastcheck = datetime.now(config.TZ)
        log(f"{self.name} valid: {valid}")

        if not valid:
            self.commit_fail()
            return False

        self.commit_success()
        return valid

    def __repr__(self):
        return "Entity-obj-%s" % self.name
