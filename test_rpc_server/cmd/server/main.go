package main

import (
	"flag"
	"log"
	"net/http"
	"net/rpc"

	"test_rpc_server/pkg/types"
)

func main() {
	var listen = flag.String("l", "127.0.0.1:1234", "Set listen address.")
	flag.Parse()

	if err := rpc.Register(new(types.Time)); err != nil {
		log.Fatalf("Error: %v", err)
	}

	rpc.HandleHTTP()
	log.Printf("Start serve %s", *listen)

	if err := http.ListenAndServe(*listen, nil); err != nil {
		log.Fatalf("Error: %v", err)
	}
}
