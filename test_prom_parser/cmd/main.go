package main

import (
	"bytes"
	"flag"
	"fmt"
	"io"
	"net/http"
	"os"
	"strings"

	"github.com/prometheus/common/expfmt"
)

var (
	url  = flag.String("u", "http://127.0.0.1:9090/metrics", "Set metrics URL")
	data []byte
)

func main() {
	var client = new(http.Client)
	var parser = new(expfmt.TextParser)

	flag.Parse()

	if res, err := client.Get(*url); err != nil {
		fmt.Fprintf(os.Stderr, "Error: %v\n", err)

	} else {
		defer res.Body.Close()
		if data, err = io.ReadAll(res.Body); err != nil {
			fmt.Fprintf(os.Stderr, "Error: %v\n", err)
		}
	}

	var reader = bytes.NewReader(data)
	if metrics, err := parser.TextToMetricFamilies(reader); err != nil {
		fmt.Fprintf(os.Stderr, "Error: %v\n", err)

	} else {
		for _, metric_item := range metrics {
			fmt.Fprintf(os.Stdout, "%s:\n", *metric_item.Name)

			for _, metric_value := range metric_item.Metric {
				if metric_value.Counter != nil {
					fmt.Fprintf(os.Stdout, "\t%s: %d\n", strings.ToLower(metric_item.Type.String()), metric_value.Counter.Value)
				}

				if metric_value.Gauge != nil {
					fmt.Fprintf(os.Stdout, "\t%s: %d\n", strings.ToLower(metric_item.Type.String()), metric_value.Gauge.Value)
				}

				if metric_value.Summary != nil {
					fmt.Fprintf(os.Stdout, "\t%s: -\n", strings.ToLower(metric_item.Type.String()))
				}

				if metric_value.Histogram != nil {
					fmt.Fprintf(os.Stdout, "\t%s: -\n", strings.ToLower(metric_item.Type.String()))
				}

				if metric_value.Untyped != nil {
					fmt.Fprintf(os.Stdout, "\t%s: %d\n", strings.ToLower(metric_item.Type.String()), metric_value.Untyped.Value)
				}

				for _, label_item := range metric_value.Label {
					fmt.Fprintf(os.Stdout, "\t%s: %s\n", *label_item.Name, *label_item.Value)
				}
			}
		}
	}
}
