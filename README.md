### Repository for testing source code

#### Build golang code:
```bash
GOOS="linux" GOARCH="amd64" go build -ldflags="-s -w" -o ./bin_out ./cmd/main.go
```

#### Create python environment:
```bash
python3 -m venv --upgrade-deps env && \
./env/bin/pip3 install -r requirements.txt
```
