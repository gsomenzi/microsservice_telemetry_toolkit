from abc import ABC, abstractmethod
from typing import Optional, Union, Any


class GenericHistogram(ABC):
    @abstractmethod
    def record(
        self,
        amount: Union[int, float],
        attributes: Optional[Any] = None,
        context: Optional[Any] = None,
    ) -> None:
        pass
