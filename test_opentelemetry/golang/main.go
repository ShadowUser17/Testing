package main

import (
	_ "github.com/gin-gonic/gin"

	_ "go.opentelemetry.io/otel"
	_ "go.opentelemetry.io/otel/exporters/stdout/stdoutmetric"
	_ "go.opentelemetry.io/otel/exporters/stdout/stdouttrace"
	_ "go.opentelemetry.io/otel/propagation"
	_ "go.opentelemetry.io/otel/sdk/metric"
	_ "go.opentelemetry.io/otel/sdk/trace"
)

func main() {
}
