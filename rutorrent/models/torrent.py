import dataclasses
import datetime
from pathlib import Path

import pydantic


@pydantic.validate_arguments
@dataclasses.dataclass
class Torrent:
    is_open: bool
    is_hash_checking: bool
    is_hash_checked: bool
    state: bool  # 1 = active 0 = inactive
    name: str
    size_bytes: int
    completed_chunks: int
    size_chunks: int
    bytes_done: int
    up_total: int
    """Total uploaded bytes"""
    ratio: float
    up_rate: int
    down_rate: int
    chunk_size: int
    custom1: str
    peers_accounted: int
    peers_not_connected: int
    peers_connected: int
    peers_complete: int
    left_bytes: int
    priority: int
    state_changed: int
    skip_total: int
    hashing: bool
    chunks_hashed: int
    base_path: str
    creation_date: datetime.datetime
    tracker_focus: str
    is_active: bool
    message: str
    custom2: str
    free_diskspace: int
    is_private: bool
    is_multi_file: bool

    info_hash: str

    def __post_init__(self):
        self.ratio = int(self.ratio) / 1000

    @property
    def is_paused(self):
        return self.is_open and not self.state

    @property
    def path_obj(self) -> Path:
        return Path(self.base_path)

    @property
    def is_complete(self) -> bool:
        return self.left_bytes == 0

    @staticmethod
    def from_list(info_hash, data):
        return Torrent(*data, info_hash)
