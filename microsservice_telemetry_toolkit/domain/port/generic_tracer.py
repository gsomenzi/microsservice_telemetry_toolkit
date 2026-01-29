from abc import ABC, abstractmethod
from contextlib import AbstractContextManager
from typing import Any


class GenericTracer(ABC):
    @abstractmethod
    def start_root_span(self, name: str) -> AbstractContextManager[Any]: ...

    @abstractmethod
    def start_span_action(self, name: str) -> AbstractContextManager[Any]: ...
