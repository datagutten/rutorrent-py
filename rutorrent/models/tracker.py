import dataclasses
import datetime

import pydantic


@pydantic.validate_arguments
@dataclasses.dataclass
class Tracker:
    url: str
    type: int
    is_enabled: bool
    group: int
    seeds: int
    peers: int
    downloaded: int
    interval_seconds: int
    last_updated_seconds: int

    @property
    def interval(self):
        return datetime.timedelta(seconds=self.interval_seconds)

    @property
    def last_updated(self):
        return datetime.timedelta(seconds=self.last_updated_seconds)

    @property
    def last_updated_time(self):
        return datetime.datetime.now() - self.last_updated
