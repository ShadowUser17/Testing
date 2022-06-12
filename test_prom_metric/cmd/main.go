package main

import (
	"fmt"
	"test_prom_metric/pkg/metric"
)

func main() {
	var testMetric = metric.New("test_metric", "Testing...")
	testMetric.Tags["job"] = "testing_job"
	testMetric.Tags["instance"] = "testing_instance"
	testMetric.Set(128)

	fmt.Println(testMetric)
}
