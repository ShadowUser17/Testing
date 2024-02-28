# https://github.com/kubernetes-client/python
import sys
import json
import gzip
import base64
import logging
import traceback

from kubernetes import config as k8s_config
from kubernetes import client as k8s_client


def get_helm_releases(client: any) -> list:
    res = client.list_secret_for_all_namespaces()
    items = filter(lambda item: item.type == "helm.sh/release.v1", res.items)
    return list(sorted(items, key=lambda item: item.metadata.name, reverse=True))


def filter_helm_releases(items: list) -> list:
    secrets = []

    name = ""
    for item in items:
        if name != item.metadata.labels["name"]:
            name = item.metadata.labels["name"]
            tmp = list(filter(lambda item: item.metadata.labels["name"] == name, items))
            secrets.append(tmp[0])

    return list(secrets)


def extract_helm_release_data(item: dict) -> dict:
    data = base64.b64decode(item.data["release"])
    data = base64.b64decode(data.decode())
    return json.loads(gzip.decompress(data))


try:
    logging.basicConfig(
        format=r'%(levelname)s [%(asctime)s]: "%(message)s"',
        datefmt=r'%Y-%m-%d %H:%M:%S',
        level=logging.INFO
    )

    k8s_config.load_kube_config()
    client = k8s_client.CoreV1Api()

    items = get_helm_releases(client)
    items = filter_helm_releases(items)

    for item in items:
        data = extract_helm_release_data(item)
        chart = data["chart"]["metadata"]
        logging.info("{} {} {}".format(chart.get("name", "?"), chart.get("home", "?"), chart.get("version", "?")))

except:
    logging.error(traceback.format_exc())
    sys.exit(1)
