from contextlib import contextmanager
from contextvars import ContextVar
from typing import Optional

from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    BatchSpanProcessor,
    SimpleSpanProcessor,
)
from opentelemetry.sdk.resources import DEPLOYMENT_ENVIRONMENT, SERVICE_NAME, Resource
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

from ..domain.port.generic_tracer import GenericTracer
from ..domain.port.generic_histogram import GenericHistogram
from ..domain.port.generic_gauge import GenericGauge
from ..domain.port.generic_counter import GenericCounter
from ..domain.port.generic_up_down_counter import GenericUpDownCounter
from ..application.services.span_name_validator import SpanNameValidator
from .otel_span import OtelSpan
from .otel_histogram import OtelHistogram
from .otel_gauge import OtelGauge
from .otel_counter import OtelCounter
from .otel_up_down_counter import OtelUpDownCounter


class OtelTracer(GenericTracer):
    _span_stack: ContextVar[list[str]] = ContextVar("span_stack", default=[])

    def __init__(
        self,
        service_name: str,
        service_environment: str = "development",
        otlp_endpoint: Optional[str] = None,
        headers: Optional[dict[str, str]] = None,
    ):
        resource = Resource.create(
            attributes={
                SERVICE_NAME: service_name,
                DEPLOYMENT_ENVIRONMENT: service_environment,
            }
        )
        self._tracer = self._define_tracer(resource, otlp_endpoint, headers)
        self._meter = self._define_meter(resource, otlp_endpoint, headers)

    def _define_tracer(
        self,
        resource: Resource,
        otlp_endpoint: Optional[str],
        headers: Optional[dict[str, str]],
    ):
        provider = TracerProvider(resource=resource)
        tracer_processor = (
            BatchSpanProcessor(
                OTLPSpanExporter(endpoint=otlp_endpoint, headers=headers)
            )
            if otlp_endpoint
            else SimpleSpanProcessor(ConsoleSpanExporter())
        )
        provider.add_span_processor(tracer_processor)
        trace.set_tracer_provider(provider)
        return provider.get_tracer(f"{resource.attributes[SERVICE_NAME]}-tracer")

    def _define_meter(
        self,
        resource: Resource,
        otlp_endpoint: Optional[str],
        headers: Optional[dict[str, str]],
    ):
        exporter = OTLPMetricExporter(endpoint=otlp_endpoint, headers=headers)
        reader = PeriodicExportingMetricReader(exporter)
        provider = MeterProvider(metric_readers=[reader], resource=resource)
        metrics.set_meter_provider(provider)
        return provider.get_meter(f"{resource.attributes[SERVICE_NAME]}-meter")

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

    def create_gauge(
        self, name: str, unit: str = "", description: str = ""
    ) -> GenericGauge:
        gauge = self._meter.create_gauge(name, unit, description)
        return OtelGauge(gauge)

    def create_counter(
        self, name: str, unit: str = "", description: str = ""
    ) -> GenericCounter:
        counter = self._meter.create_counter(name, unit, description)
        return OtelCounter(counter)

    def create_histogram(
        self,
        name: str,
        unit: str = "",
        description: str = "",
        breakpoints: Optional[list[float]] = None,
    ) -> GenericHistogram:
        histogram = self._meter.create_histogram(
            name, unit, description, explicit_bucket_boundaries_advisory=breakpoints
        )
        return OtelHistogram(histogram)

    def create_up_down_counter(
        self, name: str, unit: str = "", description: str = ""
    ) -> GenericUpDownCounter:
        counter = self._meter.create_up_down_counter(name, unit, description)
        return OtelUpDownCounter(counter)
