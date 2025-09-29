#### Usage:
```bash
export OLLAMA_HOST="http://ollama.docker:11434"
```
```bash
export OLLAMA_MODEL="gemma3:270m"
```
```bash
./env/bin/python3 main.py "<context>"
```

#### Show installed models:
```bash
curl "http://ollama.docker:11434/api/tags"
```

#### URLs:
- [python](https://github.com/ollama/ollama-python)
- [gemma3](https://ollama.com/library/gemma3)
- [phi3](https://ollama.com/library/phi3)
