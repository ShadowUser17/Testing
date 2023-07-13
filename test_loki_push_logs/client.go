package main

import (
	"fmt"
	"net/http"
	"strings"
	"time"
)

type Logger struct {
	Loki   string
	Labels map[string]string
}

func (log *Logger) Push(message string) (*http.Response, error) {
	var rawLabels = make([]string, 0)
	for key, val := range log.Labels {
		rawLabels = append(rawLabels, fmt.Sprintf("\"%s\": \"%s\"", key, val))
	}

	var fmtData = strings.NewReader(fmt.Sprintf(
		"{\"streams\": [{\"stream\": {%s}, \"values\": [[\"%d\", \"%s\"]] }]}",
		strings.Join(rawLabels, ", "), time.Now().UnixNano(), message,
	))

	return http.Post(log.Loki, "application/json", fmtData)
}

func main() {
	var labels = make(map[string]string)
	labels["env"] = "testing"
	labels["service"] = "backend"

	var logger = Logger{
		Loki:   "http://grafana-loki.k3s/loki/api/v1/push",
		Labels: labels,
	}

	var resp, err = logger.Push("Testing...")
	defer resp.Body.Close()

	if err != nil {
		fmt.Printf("Error: %v\n", err)
	}
}
