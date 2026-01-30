from typing import Optional, Union, Any
from opentelemetry.metrics import Histogram

from ..domain.port.generic_histogram import GenericHistogram


class OtelHistogram(GenericHistogram):
    def __init__(self, histogram: Histogram):
        self._histogram = histogram

    def record(
        self,
        amount: Union[int, float],
        attributes: Optional[Any] = None,
        context: Optional[Any] = None,
    ) -> None:
        self._histogram.record(amount, attributes=attributes, context=context)
