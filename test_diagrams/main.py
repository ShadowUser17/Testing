#!/usr/bin/env python3
# https://diagrams.mingrammer.com/docs/getting-started/examples
import traceback

from diagrams import Diagram
from diagrams.k8s.compute import Deploy
from diagrams.k8s.compute import Pod


def get_service(name: str) -> Pod:
    return Pod(name)

try:
    with Diagram("Testing", outformat="svg"):
        Deploy("test-service") >> [
            get_service("test-web"),
            get_service("test-api"),

        ] >> get_service("test-back") >> [
            get_service("test-reader"),
            get_service("test-writer"),
            get_service("test-queue"),
            get_service("test-notifier")
        ]

except Exception:
    traceback.print_exc()
