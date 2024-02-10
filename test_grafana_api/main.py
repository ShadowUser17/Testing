#!/usr/bin/env python3
import sys
import ssl
import uuid
import json
import traceback

from urllib import request
from urllib import parse as urllib


class Grafana:
    def __init__(self, url: str, token: str, verify: bool = False) -> None:
        self._url = url
        self._verify = verify
        self._headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(token)
        }

    def _mkurl(self, path: str) -> str:
        return str(urllib.urljoin(self._url, path))

    def _request(self, req: request.Request) -> dict:
        ctx = None if self._verify else ssl._create_unverified_context()

        with request.urlopen(url=req, context=ctx) as client:
            return json.loads(client.read())

    def list_folders(self) -> dict:
        return self._request(request.Request(
            method="GET",
            url=self._mkurl("/api/folders"),
            headers=self._headers
        ))

    def create_folder(self, name: str) -> dict:
        data = json.dumps({
            "uid": str(uuid.uuid1()),
            "title": name
        })

        return self._request(request.Request(
            method="POST",
            url=self._mkurl("/api/folders"),
            data=data.encode(),
            headers=self._headers
        ))

    def delete_folder(self, uid: str) -> dict:
        return self._request(request.Request(
            method="DELETE",
            url=self._mkurl("/api/folders/{}".format(uid)),
            headers=self._headers
        ))


try:
    client = Grafana("https://grafana.k3s/", "glsa_c42xcSSH98ZKol5NMIacGls3Gxlao8ae_cdc6a6b1")
    print(client.list_folders())
    #print(client.create_folder("dmytro_test"))
    #print(client.delete_folder("9890a252-c865-11ee-a045-d8bbc1905606"))
    #print(client.list_folders())

except Exception:
    traceback.print_exc()
    sys.exit(1)
