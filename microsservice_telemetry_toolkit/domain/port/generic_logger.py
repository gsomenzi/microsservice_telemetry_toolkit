from abc import ABC, abstractmethod


class GenericLogger(ABC):
    @abstractmethod
    def log(self, message: str) -> None: ...
