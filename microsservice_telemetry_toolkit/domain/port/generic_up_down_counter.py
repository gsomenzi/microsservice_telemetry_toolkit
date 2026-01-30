from abc import ABC, abstractmethod
from typing import Optional, Union, Any


class GenericUpDownCounter(ABC):
    @abstractmethod
    def add(
        self,
        amount: Union[int, float],
        attributes: Optional[Any] = None,
        context: Optional[Any] = None,
    ) -> None:
        """Adiciona um valor (positivo ou negativo) ao contador."""
        pass
