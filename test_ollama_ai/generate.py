import os
import sys
import ollama
import traceback


try:
    resp = ollama.generate(os.environ.get("OLLAMA_MODEL", ""), sys.argv[1])
    print(resp['response'])

except Exception:
    traceback.print_exc()
    sys.exit(1)
