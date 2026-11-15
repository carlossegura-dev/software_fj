"""Clase abstracta que representa las entidades generales del sistema."""

from abc import ABC, abstractmethod
from itertools import count


class Entidad(ABC):
    """Base abstracta: toda entidad tiene un identificador único y se describe."""

    _contador = count(1)

    def __init__(self) -> None:
        self._id = next(Entidad._contador)

    @property
    def id(self) -> int:
        """Identificador de solo lectura (encapsulación)."""
        return self._id

    @abstractmethod
    def describir(self) -> str:
        """Texto legible de la entidad; cada subclase lo implementa."""

    def __str__(self) -> str:
        return self.describir()
