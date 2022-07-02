package main

import (
	"flag"
	"io/ioutil"
	"log"
	"net/http"
)

func main() {
	var listen = flag.String("l", "127.0.0.1:5002", "Set listen address.")
	flag.Parse()

	http.HandleFunc("/", func(rw http.ResponseWriter, req *http.Request) {
		rw.WriteHeader(http.StatusOK)
		defer req.Body.Close()

		if data, err := ioutil.ReadAll(req.Body); err != nil {
			log.Printf("Error: %v", err)

		} else {
			log.Println("Body:", string(data))
		}
	})

	log.Printf("Start listen: http://%s/\n", *listen)
	log.Fatal(http.ListenAndServe(*listen, nil))
	log.Println("Normal exit.")
}
