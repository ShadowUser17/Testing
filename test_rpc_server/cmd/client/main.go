package main

import (
	"flag"
	"log"
	"net/rpc"

	"test_rpc_server/pkg/types"
)

func main() {
	var server = flag.String("s", "127.0.0.1:1234", "Set server address.")
	flag.Parse()

	if client, err := rpc.DialHTTP("tcp", *server); err != nil {
		log.Fatalf("Error: %v", err)

	} else {
		var replay = new(types.Time)
		defer client.Close()

		if err = client.Call("Time.Request", types.REQ_OP_GET, replay); err != nil {
			log.Fatalf("Error: %v", err)

		} else {
			log.Printf("Replay: %s", replay.String())
		}
	}
}
