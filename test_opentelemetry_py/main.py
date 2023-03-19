#!/usr/bin/env python3
# https://opentelemetry.io/docs/instrumentation/python/manual/
import traceback
from datetime import datetime

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.export import ConsoleSpanExporter
# from opentelemetry.exporter.zipkin.json import ZipkinExporter


trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(ConsoleSpanExporter())
)

# trace.get_tracer_provider().add_span_processor(
#     BatchSpanProcessor(
#         ZipkinExporter(endpoint="http://localhost:9411/api/v2/spans")
#     )
# )


try:
    with tracer.start_as_current_span("testing"):
        print(datetime.now())

except Exception:
    with tracer.start_as_current_span("exception"):
        traceback.print_exc()
