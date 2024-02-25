# https://github.com/ktbyers/netmiko?tab=readme-ov-file#getting-started-1
import sys
import logging
import traceback

from netmiko import ConnectHandler


try:
    logging.basicConfig(
        format=r'%(levelname)s [%(asctime)s]: "%(message)s"',
        datefmt=r'%Y-%m-%d %H:%M:%S',
        level=logging.INFO
    )

    config = {
        "host": "192.168.207.1",
        "port": 1127,
        "username": "netmiko_client",
        "use_keys": True,
        "key_file": "~/.ssh/keys/netmiko_ssh_key",
        "device_type": "mikrotik_routeros"
    }

    with ConnectHandler(**config) as client:
        logging.info(client.send_command("/system/routerboard/print"))
        logging.info(client.send_command("/file/print proplist=name"))

except Exception:
    logging.error(traceback.format_exc())
    sys.exit(1)
