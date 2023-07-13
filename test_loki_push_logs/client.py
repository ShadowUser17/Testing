#!/usr/bin/env python3
import sys
import time
import json
import traceback

from urllib import parse as urllib
from urllib import request


class Logger:
    def __init__(self, url: str, labels: dict) -> None:
        self._url = urllib.urljoin(url, '/loki/api/v1/push')
        self._labels = labels.copy()
        self._headers = {"Content-Type": "application/json"}

    def _get_body(self, message: str) -> bytes:
        return json.dumps({
            "streams": [{
                "stream": self._labels,
                "values": [[str(time.time_ns()), message]]
            }]
        }).encode()

    def push(self, message: str) -> int:
        req = request.Request(
            method="POST",
            url=self._url,
            headers=self._headers,
            data=self._get_body(message)
        )

        with request.urlopen(req) as client:
            return client.status


try:
    log = Logger("http://grafana-loki.k3s", {"env": "testing", "service": "logger"})
    log.push("Testing...")

except Exception:
    traceback.print_exc()
    sys.exit(1)
