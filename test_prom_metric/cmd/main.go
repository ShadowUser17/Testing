package main

import (
	"flag"
	"log"
	"math/rand"
	"net/http"
	"strconv"
	"time"

	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promhttp"
)

var (
	listen   = flag.String("l", "127.0.0.1:5002", "Set listen ip:port")
	registry = prometheus.NewRegistry()
)

var (
	testing_counter = prometheus.NewCounterVec(prometheus.CounterOpts{
		Name: "testing_counter",
		Help: "Test of counter",
	}, []string{"id"})

	testing_gauge = prometheus.NewGaugeVec(prometheus.GaugeOpts{
		Name: "testing_gauge",
		Help: "Test of gauge",
	}, []string{"id"})
)

func main() {
	flag.Parse()
	registry.MustRegister(testing_counter)
	registry.MustRegister(testing_gauge)

	http.Handle("/metrics", promhttp.HandlerFor(
		registry,
		promhttp.HandlerOpts{
			EnableOpenMetrics: true,
		},
	))

	go worker()
	log.Printf("Listen: %s\n", *listen)
	log.Fatal(http.ListenAndServe(*listen, nil))
}

func worker() {
	var (
		id_counter = strconv.Itoa(rand.Int())
		id_gauge   = strconv.Itoa(rand.Int())
	)

	for {
		testing_counter.WithLabelValues(id_counter).Inc()
		testing_gauge.WithLabelValues(id_gauge).Inc()
		time.Sleep(time.Second * 10)
	}
}
