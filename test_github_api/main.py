#!/usr/bin/env python3
import subprocess
import traceback
import json
import os


def get_forks() -> list:
    git = os.path.join(os.path.expanduser("~"), "gh")
    cmd = subprocess.Popen(
        [git, "repo", "list", "--fork", "--json", "name"],
        shell=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL
    )

    (out, _) = cmd.communicate()
    return list(map(lambda item: item["name"], json.loads(out)))


try:
    print(get_forks())

except Exception:
    traceback.print_exc()
