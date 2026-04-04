import re
import urllib.parse
from pathlib import Path

import requests

from . import models


class RuTorrent:
    def __init__(self, url: str):
        self.session = requests.session()
        self.url = url

    def _post_action(self, action, info_hash: str = None) -> dict:
        if action not in [
            "list",
            "recheck",
            "start",
            "stop",
            "pause",
            "unpause",
            "remove",
            "trk",
            "trkstate",
            "trkall",
            "ttl",
            "stg",
        ]:
            raise RuntimeError("Invalid action")

        parameters = {"mode": action}
        if info_hash:
            parameters["hash"] = info_hash.upper()
        url = self.url + "/plugins/httprpc/action.php"
        response = self.session.post(url, data=parameters)
        response.raise_for_status()
        return response.json()

    def get_config(self):
        response = self._post_action("stg")
        return models.Config(*response)

    def get_torrents(self) -> list[models.Torrent]:
        response = self._post_action("list")
        if not response["t"]:
            return []
        return [
            models.Torrent(*data, info_hash)
            for info_hash, data in response["t"].items()
        ]

    def get_trackers(self, info_hash: str) -> list[models.Tracker]:
        response = self._post_action("trk", info_hash)
        return [models.Tracker(*data) for data in response]

    def get_torrent_file(self, info_hash: str):
        response = self.session.post(
            self.url + "/plugins/source/action.php", data={"hash": info_hash}
        )
        response.raise_for_status()
        filename = re.sub(
            r'attachment; filename="(.+)"',
            r"\1",
            response.headers.get("Content-Disposition"),
        )
        filename = filename.encode("latin-1").decode("utf8")
        return response.content, filename

    def delete_torrent(self, info_hash: str):
        return self._post_action("remove", info_hash)

    def add_torrent(self, file: Path, path: str = "", start_stopped=False):
        url = self.url + "/php/addtorrent.php"
        args = {
            "dir_edit": path,
        }
        if start_stopped:
            args["torrents_start_stopped"] = 0

        url_args = urllib.parse.urlencode(args)
        url += "?" + url_args
        files = {"torrent_file[]": file.open("rb")}
        response = self.session.post(url, files=files)

        response.raise_for_status()

    def set_path(self, info_hash: str, path: str, add_path=True, move_files=False, fast_resume=False):
        data = {
            "hash": info_hash,
            "datadir": path,
            "move_addpath": int(add_path),
            "move_datafiles": int(move_files),
            "move_fastresume": int(fast_resume),
        }
        response = self.session.post(
            self.url + "/plugins/datadir/action.php", data=data
        )
        response.raise_for_status()
        return response.json()

    def recheck(self, info_hash: str):
        self._post_action("recheck", info_hash)
