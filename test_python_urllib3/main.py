import sys
import urllib3
import logging
import traceback


try:
    logging.basicConfig(
        format=r'%(levelname)s [%(asctime)s]: "%(message)s"',
        datefmt=r'%Y-%m-%d %H:%M:%S', level=logging.DEBUG
    )

    resp = urllib3.request(method="GET", url="http://ident.me")
    logging.info("Status: {} Data: {}".format(resp.status, resp.data.decode()))

except Exception:
    logging.error(traceback.format_exc())
    sys.exit(1)
