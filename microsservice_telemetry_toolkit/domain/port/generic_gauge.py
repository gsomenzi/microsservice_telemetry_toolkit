from abc import ABC, abstractmethod
from typing import Optional, Union, Any, Callable


class GenericGauge(ABC):
    @abstractmethod
    def set(
        self,
        amount: Union[int, float],
        attributes: Optional[Any] = None,
        context: Optional[Any] = None,
    ) -> None:
        """Define o valor atual do gauge."""
        pass
