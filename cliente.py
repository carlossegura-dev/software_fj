"""Clase Cliente con validaciones robustas y datos personales encapsulados."""

import re

from entidad import Entidad
from excepciones import ClienteInvalidoError, ParametroFaltanteError

_PATRON_CORREO = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")


class Cliente(Entidad):
    """Cliente de Software FJ. Los atributos son privados y se validan al asignar."""

    def __init__(self, nombre=None, documento=None, correo=None, telefono=None):
        super().__init__()
        # Parámetros faltantes: se reporta con una excepción propia.
        faltantes = [n for n, v in (("nombre", nombre), ("documento", documento),
                                    ("correo", correo), ("telefono", telefono))
                     if v is None]
        if faltantes:
            raise ParametroFaltanteError(
                f"Faltan parámetros del cliente: {', '.join(faltantes)}")
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono

    # --- nombre ---
    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ClienteInvalidoError("El nombre debe tener al menos 3 caracteres.")
        if any(ch.isdigit() for ch in valor):
            raise ClienteInvalidoError("El nombre no puede contener números.")
        self._nombre = valor.strip().title()

    # --- documento ---
    @property
    def documento(self) -> str:
        return self._documento

    @documento.setter
    def documento(self, valor) -> None:
        valor = str(valor).strip()
        if not valor.isdigit() or not 6 <= len(valor) <= 12:
            raise ClienteInvalidoError(
                "El documento debe tener solo dígitos (entre 6 y 12).")
        self._documento = valor

    # --- correo ---
    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str) -> None:
        if not isinstance(valor, str) or not _PATRON_CORREO.match(valor.strip()):
            raise ClienteInvalidoError(f"Correo inválido: {valor!r}")
        self._correo = valor.strip().lower()

    # --- teléfono ---
    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor) -> None:
        valor = str(valor).strip()
        if not valor.isdigit() or len(valor) != 10:
            raise ClienteInvalidoError(
                "El teléfono debe tener exactamente 10 dígitos.")
        self._telefono = valor

    def describir(self) -> str:
        return (f"Cliente #{self.id}: {self.nombre} | Doc: {self.documento} | "
                f"{self.correo} | Tel: {self.telefono}")
