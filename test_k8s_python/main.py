# https://github.com/kubernetes-client/python
import logging

from kubernetes import config as k8s_config
from kubernetes import client as k8s_client


logging.basicConfig(
    format=r'%(levelname)s [%(asctime)s]: "%(message)s"',
    datefmt=r'%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)

k8s_config.load_kube_config()
core_api_client = k8s_client.CoreV1Api()
custom_api_client = k8s_client.CustomObjectsApi()
