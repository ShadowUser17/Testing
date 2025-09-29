import os
import sys
import ollama
import traceback


try:
    resp = ollama.chat(
        model=os.environ.get("OLLAMA_MODEL", "gemma3:270m"),
        messages=[{"role": "user", "content": sys.argv[1]}]
    )

    print(resp['message']['content'])

except Exception:
    traceback.print_exc()
    sys.exit(1)
