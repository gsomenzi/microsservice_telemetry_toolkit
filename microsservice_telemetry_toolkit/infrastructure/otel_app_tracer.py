from contextlib import contextmanager
from contextvars import ContextVar
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from typing import Optional
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    BatchSpanProcessor,
    SimpleSpanProcessor,
)
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

from ..domain.port.generic_tracer import GenericTracer
from ..application.services.span_name_validator import SpanNameValidator
from ..infrastructure.otel_span import OtelSpan
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter


class OtelAppTracer(GenericTracer):
    _span_stack: ContextVar[list[str]] = ContextVar("span_stack", default=[])

    def __init__(
        self,
        service_name: str,
        otlp_endpoint: Optional[str] = None,
        headers: Optional[dict[str, str]] = None,
    ):
        resource = Resource.create(attributes={SERVICE_NAME: service_name})
        provider = TracerProvider(resource=resource)
        processor = (
            BatchSpanProcessor(
                OTLPSpanExporter(endpoint=otlp_endpoint, headers=headers)
            )
            if otlp_endpoint
            else SimpleSpanProcessor(ConsoleSpanExporter())
        )
        provider.add_span_processor(processor)
        trace.set_tracer_provider(provider)
        self._tracer = provider.get_tracer("base-app-tracer")

    @contextmanager
    def start_root_span(self, name: str):
        validator = SpanNameValidator(parts_count=3)
        validator.validate(name)
        stack = self._span_stack.get() or []
        if stack:
            raise RuntimeError(
                "start_root_span must be used as a root span. Use start_span_action for nested spans."
            )
        with self._tracer.start_as_current_span(name) as span:
            new_stack = [name]
            token = self._span_stack.set(new_stack)
            try:
                yield OtelSpan(name, span)
            finally:
                self._span_stack.reset(token)

    @contextmanager
    def start_span_action(self, name: str):
        validator = SpanNameValidator(parts_count=1)
        validator.validate(name)
        stack = self._span_stack.get() or []
        if not stack:
            raise RuntimeError("No active span found to create an action span.")
        parent_name = stack[-1]
        full_name = f"{parent_name}.{name}"
        with self._tracer.start_as_current_span(full_name) as span:
            new_stack = stack + [full_name]
            token = self._span_stack.set(new_stack)
            try:
                yield OtelSpan(full_name, span)
            finally:
                self._span_stack.reset(token)
