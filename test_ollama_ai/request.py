import os
import sys
import ollama
import traceback


try:
    messages = [{"role": "user", "content": item} for item in sys.argv]
    resp = ollama.chat(os.environ.get("OLLAMA_MODEL", ""), messages)
    print(resp['message']['content'])

except Exception:
    traceback.print_exc()
    sys.exit(1)
