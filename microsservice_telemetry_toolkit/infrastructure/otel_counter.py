from typing import Optional, Union, Any
from opentelemetry.metrics import Counter

from ..domain.port.generic_counter import GenericCounter


class OtelCounter(GenericCounter):
    def __init__(self, counter: Counter):
        self._counter = counter

    def add(
        self,
        amount: Union[int, float],
        attributes: Optional[Any] = None,
        context: Optional[Any] = None,
    ) -> None:
        self._counter.add(amount, attributes=attributes, context=context)
