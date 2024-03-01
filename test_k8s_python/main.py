# https://github.com/kubernetes-client/python
import sys
import logging
import traceback

from kubernetes import config as k8s_config
from kubernetes import client as k8s_client


try:
    logging.basicConfig(
        format=r'%(levelname)s [%(asctime)s]: "%(message)s"',
        datefmt=r'%Y-%m-%d %H:%M:%S',
        level=logging.INFO
    )

    k8s_config.load_kube_config()
    core_api = k8s_client.CoreV1Api()

    res = core_api.list_pod_for_all_namespaces(watch=False)
    for item in res.items:
        logging.info("{}/{}/{}".format(item.spec.node_name, item.metadata.namespace, item.metadata.name))

except Exception:
    logging.error(traceback.format_exc())
    sys.exit(1)
