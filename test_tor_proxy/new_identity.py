import sys
import traceback

from stem import Signal
from stem.control import Controller


try:
    with Controller.from_port(port=9051) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)
        print("[*] New Tor identity requested.")

except Exception:
    traceback.print_exc()
    sys.exit(1)
