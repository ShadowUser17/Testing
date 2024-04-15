import os
import sys
import traceback

import sentry_sdk
from opentelemetry import trace
from opentelemetry.propagate import set_global_textmap
from opentelemetry.sdk.trace import TracerProvider
from sentry_sdk.integrations.opentelemetry import (
    SentrySpanProcessor,
    SentryPropagator
)


sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN", ""),
    enable_tracing=True,
    instrumenter="otel"
)

provider = TracerProvider()
provider.add_span_processor(SentrySpanProcessor())
trace.set_tracer_provider(provider)
set_global_textmap(SentryPropagator())


try:
    pass

except Exception:
    traceback.print_exc()
    sys.exit(1)
