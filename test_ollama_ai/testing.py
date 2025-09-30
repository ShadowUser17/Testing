import os
import ollama
import pathlib

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "")
print("Host: {}\nModel: {}".format(OLLAMA_HOST, OLLAMA_MODEL))
