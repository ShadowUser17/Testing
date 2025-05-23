import os
import sys
import pprint
import logging
import warnings
import traceback


from urllib3.exceptions import InsecureRequestWarning
warnings.filterwarnings("ignore", category=InsecureRequestWarning)

from python_freeipa import ClientMeta as FreeIpa


try:
    log_level = logging.DEBUG if os.environ.get("DEBUG_MODE", "") else logging.INFO
    logging.basicConfig(
        format=r'%(levelname)s [%(asctime)s]: "%(message)s"',
        datefmt=r'%Y-%m-%d %H:%M:%S', level=log_level
    )

    client = FreeIpa(host=os.environ.get("IPA_SERVER", "ipa.testing.local"), verify_ssl=False)
    client.login(os.environ.get("IPA_ADMIN", "admin"), os.environ.get("IPA_PASSWD", ""))

    items = client.user_find(o_in_group="admins")
    for item in items["result"]:
        pprint.pprint(item)

except Exception:
    logging.error(traceback.format_exc())
    sys.exit(1)
