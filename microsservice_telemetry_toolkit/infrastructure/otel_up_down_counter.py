from typing import Optional, Union, Any
from opentelemetry.metrics import UpDownCounter

from ..domain.port.generic_up_down_counter import GenericUpDownCounter


class OtelUpDownCounter(GenericUpDownCounter):
    def __init__(self, counter: UpDownCounter):
        self._counter = counter

    def add(
        self,
        amount: Union[int, float],
        attributes: Optional[Any] = None,
        context: Optional[Any] = None,
    ) -> None:
        self._counter.add(amount, attributes=attributes, context=context)
