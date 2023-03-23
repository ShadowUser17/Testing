#!/usr/bin/env python3
# https://github.com/kubernetes-client/python
import sys
from traceback import print_exc
from kubernetes import config as k8s_config
from kubernetes import client as k8s_client


try:
    k8s_config.load_kube_config()
    core_api = k8s_client.CoreV1Api()

    res = core_api.list_pod_for_all_namespaces(watch=False)
    for item in res.items:
        print("{}/{}/{}".format(item.spec.node_name, item.metadata.namespace, item.metadata.name))

except Exception:
    print_exc()
    sys.exit(1)
