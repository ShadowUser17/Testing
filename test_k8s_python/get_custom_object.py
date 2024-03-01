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
    core_api_client = k8s_client.CoreV1Api()
    custom_api_client = k8s_client.CustomObjectsApi()

    ns_list = core_api_client.list_namespace()
    for ns_item in ns_list.items:
        vulns = custom_api_client.list_namespaced_custom_object(
            "aquasecurity.github.io", "v1alpha1",
            ns_item.metadata.name, "vulnerabilityreports"
        )

        for vuln_item in vulns.get("items", []):
            logging.info("{}/{}".format(
                vuln_item["metadata"]["namespace"],
                vuln_item["metadata"]["name"]
            ))

            # logging.info("Report: {}".format(vuln_item["report"]))

except Exception:
    logging.error(traceback.format_exc())
    sys.exit(1)
