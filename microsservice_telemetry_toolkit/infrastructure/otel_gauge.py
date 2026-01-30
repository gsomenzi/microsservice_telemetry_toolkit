from typing import Optional, Union, Any
from opentelemetry.metrics import _Gauge as Gauge

from ..domain.port.generic_gauge import GenericGauge


class OtelGauge(GenericGauge):
    def __init__(self, gauge: Gauge):
        self._gauge = gauge

    def set(
        self,
        amount: Union[int, float],
        attributes: Optional[Any] = None,
        context: Optional[Any] = None,
    ) -> None:
        self._gauge.set(amount, attributes=attributes, context=context)
