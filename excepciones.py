"""Excepciones personalizadas del sistema Software FJ.

Todas heredan de SoftwareFJError, de modo que el programa principal puede
capturar cualquier error propio del dominio con un solo ``except`` sin
ocultar errores ajenos (por ejemplo, un fallo de programación).
"""


class SoftwareFJError(Exception):
    """Excepción base de todo el sistema."""


class ClienteInvalidoError(SoftwareFJError):
    """Datos del cliente inválidos (nombre, correo, teléfono, documento)."""


class ParametroFaltanteError(SoftwareFJError):
    """Se omitió un parámetro obligatorio."""


class ServicioInvalidoError(SoftwareFJError):
    """Parámetros de un servicio inválidos al crearlo o configurarlo."""


class ServicioNoDisponibleError(SoftwareFJError):
    """El servicio existe pero no se puede reservar en este momento."""


class ReservaError(SoftwareFJError):
    """Fallo general al crear o procesar una reserva."""


class OperacionNoPermitidaError(SoftwareFJError):
    """Operación inválida para el estado actual (ej. confirmar una cancelada)."""


class CalculoInconsistenteError(SoftwareFJError):
    """El cálculo de un costo produjo un resultado inconsistente."""
