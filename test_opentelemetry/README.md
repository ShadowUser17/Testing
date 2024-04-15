#### Python:
```bash
python3 -m venv --upgrade-deps env && \
./env/bin/pip3 install -r ./python/requirements.txt
```

#### Golang:
```bash
cd golang
```
```bash
go mod tidy
```
```bash
go build -ldflags="-s -w" -o ./server ./golang/main.go
```

#### URLs:
- [python](https://opentelemetry.io/docs/languages/python/getting-started/)
- [golang](https://opentelemetry.io/docs/languages/go/getting-started/)
