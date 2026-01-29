from opentelemetry import trace
from opentelemetry.trace import Span, types


class OtelSpan:
    name: str
    _span: Span

    def __init__(self, name: str, span: Span):
        self.name = name
        self._span = span

    def set_status_ok(self):
        self._span.set_status(trace.Status(trace.StatusCode.OK))

    def set_status_error(self, description: str = ""):
        self._span.set_status(
            trace.Status(trace.StatusCode.ERROR, description=description)
        )

    def set_attribute(
        self,
        key: str,
        value: types.AttributeValue,
    ):
        self._span.set_attribute(key, value)

    def get_context(self) -> dict[str, str]:
        ctx = self._span.get_span_context()
        ctx_dict = {
            "trace_id": format(ctx.trace_id, "032x"),
            "span_id": format(ctx.span_id, "016x"),
            "trace_flags": int(ctx.trace_flags),
        }
        return ctx_dict

    def record_exception(self, exception: Exception):
        self._span.set_status(
            trace.Status(trace.StatusCode.ERROR, description=str(exception))
        )
        self._span.record_exception(exception)

    def record_and_raise_exception(self, exception: Exception):
        self.record_exception(exception)
        raise exception
