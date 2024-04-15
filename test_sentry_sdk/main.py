import os
from flask import Flask

import sentry_sdk
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.propagate import set_global_textmap
from sentry_sdk.integrations.opentelemetry import SentryPropagator
from sentry_sdk.integrations.opentelemetry import SentrySpanProcessor


sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN", ""),
    enable_tracing=True,
    instrumenter="otel"
)

provider = TracerProvider()
provider.add_span_processor(SentrySpanProcessor())
trace.set_tracer_provider(provider)
set_global_textmap(SentryPropagator())
tracer = trace.get_tracer(__name__)


app = Flask(__name__)
@app.route("/")
def home():
    with tracer.start_as_current_span("home"):
        1 / 0
        return "Testing..."


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
