import time
import random


def success() -> int:
    return 1


def failed() -> int:
    return 2 / 0


def waiting() -> float:
    timeout = float(5)
    time.sleep(timeout)
    return timeout


def get_func() -> any:
    return random.choice((
        success,
        failed,
        waiting,
    ))
