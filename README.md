## Repository for testing source code
#### Example of build golang code:
```bash
GOOS="linux" GOARCH="amd64" go build -ldflags="-s -w" -o ./bin_out ./cmd/main.go
```
