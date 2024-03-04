import sys
import logging
import traceback

from http import client as http
from urllib import request
from urllib import parse as urllib


try:
    logging.basicConfig(
        format=r'%(levelname)s [%(asctime)s]: "%(message)s"',
        datefmt=r'%Y-%m-%d %H:%M:%S',
        level=logging.DEBUG
    )

    url = urllib.urljoin("https://prometheus-community.github.io/helm-charts", "index.yaml")
    req = request.Request(url=url, method="GET")

    http.HTTPConnection.debuglevel = 1
    http.HTTPSConnection.debuglevel = 1

    with request.urlopen(req) as client:
        client.read()

except Exception:
    logging.error(traceback.format_exc())
    sys.exit(1)
