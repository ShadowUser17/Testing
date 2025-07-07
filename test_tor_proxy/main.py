import os
import sys
import requests
import traceback


TOR_HOST = os.environ.get("TOR_HOST", "192.168.56.10")
TOR_PORT = os.environ.get("TOR_PORT", "9050")


try:
    proxies = {
        "http":  "socks5h://{}:{}".format(TOR_HOST, TOR_PORT),
        "https": "socks5h://{}:{}".format(TOR_HOST, TOR_PORT)
    }

    response = requests.get("https://check.torproject.org/api/ip")
    print("Real:", response.text)

    response = requests.get("https://check.torproject.org/api/ip", proxies=proxies)
    print("TOR:", response.text)

except Exception:
    traceback.print_exc()
    sys.exit(1)
