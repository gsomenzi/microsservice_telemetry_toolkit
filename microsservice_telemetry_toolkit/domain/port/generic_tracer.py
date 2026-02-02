from abc import ABC, abstractmethod
from contextlib import AbstractContextManager
from typing import Optional
from .generic_histogram import GenericHistogram
from .generic_gauge import GenericGauge
from .generic_counter import GenericCounter
from .generic_up_down_counter import GenericUpDownCounter
from .generic_span import GenericSpan


class GenericTracer(ABC):
    @abstractmethod
    def start_root_span(self, name: str) -> AbstractContextManager[GenericSpan]: ...

    @abstractmethod
    def start_root_span_with_context(
        self,
        name: str,
        trace_id: str,
        span_id: str,
        trace_flags: int = 0x01,
    ) -> AbstractContextManager[GenericSpan]: ...

    @abstractmethod
    def start_span_action(self, name: str) -> AbstractContextManager[GenericSpan]: ...

    @abstractmethod
    def create_histogram(
        self,
        name: str,
        unit: str = "",
        description: str = "",
        breakpoints: Optional[list[float]] = None,
    ) -> GenericHistogram: ...

    @abstractmethod
    def create_gauge(
        self,
        name: str,
        unit: str = "",
        description: str = "",
    ) -> GenericGauge: ...

    @abstractmethod
    def create_counter(
        self,
        name: str,
        unit: str = "",
        description: str = "",
    ) -> GenericCounter: ...

    @abstractmethod
    def create_up_down_counter(
        self,
        name: str,
        unit: str = "",
        description: str = "",
    ) -> GenericUpDownCounter: ...
