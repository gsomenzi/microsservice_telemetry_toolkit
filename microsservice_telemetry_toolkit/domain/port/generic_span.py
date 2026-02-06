from abc import ABC, abstractmethod
from typing import Any, TypedDict


class SpanContext(TypedDict):
    trace_id: str
    span_id: str
    trace_flags: int


class GenericSpan(ABC):
    @abstractmethod
    def set_status_ok(self) -> None:
        """Define o status do span como OK."""
        ...

    @abstractmethod
    def set_status_error(self, description: str = "") -> None:
        """Define o status do span como ERROR com uma descrição opcional."""
        ...

    @abstractmethod
    def set_attribute(self, key: str, value: Any) -> None:
        """Define um atributo no span."""
        ...

    @abstractmethod
    def set_attributes(self, attributes: dict[str, Any]) -> None:
        """Define múltiplos atributos no span."""
        ...

    @abstractmethod
    def get_context(self) -> SpanContext:
        """Retorna o contexto do span (trace_id, span_id, etc)."""
        ...

    @abstractmethod
    def record_exception(self, exception: Exception) -> None:
        """Registra uma exceção no span."""
        ...

    @abstractmethod
    def record_and_raise_exception(self, exception: Exception) -> None:
        """Registra uma exceção no span e a re-lança."""
        ...
