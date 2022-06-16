package main

import (
	"fmt"
	"os"
	"test_ssl_cert/pkg/cert"
)

func main() {
	if certPath, keyPath, err := cert.MakeCert("./", "localhost"); err != nil {
		fmt.Fprintf(os.Stderr, "Error: %v\n", err)
		os.Exit(1)

	} else {
		fmt.Printf("Cert: %s\nKey: %s\n", certPath, keyPath)
	}
}
