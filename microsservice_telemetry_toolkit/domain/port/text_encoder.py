from abc import ABC, abstractmethod


class TextEncoder(ABC):
    @abstractmethod
    def encode(self, text: str) -> str: ...
