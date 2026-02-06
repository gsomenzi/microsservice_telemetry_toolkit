from abc import ABC, abstractmethod
from contextlib import AbstractContextManager
from typing import Optional, TypedDict, Any
from .generic_histogram import GenericHistogram
from .generic_gauge import GenericGauge
from .generic_counter import GenericCounter
from .generic_up_down_counter import GenericUpDownCounter
from .generic_span import GenericSpan


class GenericSpanContext(TypedDict):
    trace_id: str
    span_id: str
    trace_flags: int


class GenericTracer(ABC):
    @abstractmethod
    def start_root_span(
        self, name: str, context: Optional[GenericSpanContext] = None
    ) -> AbstractContextManager[GenericSpan]: ...

    @abstractmethod
    def start_span_action(self, name: str) -> AbstractContextManager[GenericSpan]: ...

    @abstractmethod
    def extract_context_from(
        self, carrier: dict[str, Any]
    ) -> Optional[GenericSpanContext]: ...

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
