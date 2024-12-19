#!/usr/bin/env python3
import os
import sys
import requests
import traceback

# NEXUS_USERNAME
# NEXUS_PASSWORD
# NEXUS_SCHEMA
# NEXUS_HOSTNAME
# NEXUS_FILENAME
# NEXUS_REPOSITORY


def upload_package() -> tuple[int, str]:
    with open(os.environ.get("NEXUS_FILENAME", ""), "rb") as package_fd:
        response = requests.put(
            url="{}://{}/service/rest/v1/components?repository={}".format(
                os.environ.get("NEXUS_SCHEMA", "http"),
                os.environ.get("NEXUS_HOSTNAME", "localhost"),
                os.environ.get("NEXUS_REPOSITORY", "testing")
            ),
            headers={"Content-Type": "application/octet-stream"},
            auth=(
                os.environ.get("NEXUS_USERNAME", ""),
                os.environ.get("NEXUS_PASSWORD", "")
            ),
            data=package_fd
        )

        return (response.status_code, response.text)


try:
    print("Status: {}, Text: {}".format(upload_package()))

except Exception:
    traceback.print_exc()
    sys.exit(1)
