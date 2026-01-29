from abc import ABC, abstractmethod
from typing import Any, Optional


class ChainHandler(ABC):
    def __init__(self, next_handler: Optional["ChainHandler"] = None) -> None:
        self._next = next_handler

    def set_next(self, next_handler: "ChainHandler") -> "ChainHandler":
        self._next = next_handler
        return next_handler

    @abstractmethod
    def handle(self, request: Any) -> Any:
        if self._next:
            return self._next.handle(request)
        return None
