#!/usr/bin/env python3
import sys
import json
import pathlib
import argparse
import traceback

from urllib import request


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Set path of the list of URLs.")
    return parser.parse_args()


def get_urls(path: str) -> list:
    data = pathlib.Path(path).read_text()
    return list(filter(None, data.split('\n')))


def check_url(url: str) -> dict:
    try:
        with request.urlopen(url) as client:
            data = client.read()
            data = json.loads(data.decode())
            return {"service": url, "version": data.get("version", "")}

    except Exception as error:
        return {"service": url, "error": str(error)}


try:
    args = get_args()
    urls = get_urls(args.path)

    for item in iter(urls):
        print(check_url(item))

except Exception:
    traceback.print_exc()
    sys.exit(1)
