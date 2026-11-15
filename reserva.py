"""Clase Reserva: integra cliente, servicio, duración y estado."""

from cliente import Cliente
from entidad import Entidad
from excepciones import (OperacionNoPermitidaError, ReservaError,
                         ServicioInvalidoError, ServicioNoDisponibleError,
                         SoftwareFJError)
from registro_logs import log
from servicios import IVA, Servicio

PENDIENTE, CONFIRMADA, CANCELADA, PROCESADA = (
    "PENDIENTE", "CONFIRMADA", "CANCELADA", "PROCESADA")


class Reserva(Entidad):
    def __init__(self, cliente: Cliente, servicio: Servicio, duracion: float):
        super().__init__()
        # try/except/else: validamos y encadenamos la causa original con ``from``.
        try:
            if not isinstance(cliente, Cliente):
                raise ReservaError("La reserva requiere un cliente válido.")
            if not isinstance(servicio, Servicio):
                raise ReservaError("La reserva requiere un servicio válido.")
            if not servicio.disponible:
                raise ServicioNoDisponibleError(
                    f"El servicio '{servicio.nombre}' no está disponible.")
            servicio.validar_parametros(duracion)
        except ServicioInvalidoError as causa:
            # Encadenamiento de excepciones: ReservaError <- ServicioInvalidoError
            raise ReservaError(f"No se pudo crear la reserva: {causa}") from causa
        else:
            self._cliente = cliente
            self._servicio = servicio
            self._duracion = duracion
            self._estado = PENDIENTE
            log.info("Reserva #%s creada (cliente=%s, servicio=%s, %sh)",
                     self.id, cliente.nombre, servicio.nombre, duracion)

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @property
    def servicio(self) -> Servicio:
        return self._servicio

    def confirmar(self) -> None:
        if self._estado != PENDIENTE:
            raise OperacionNoPermitidaError(
                f"Solo se confirma una reserva PENDIENTE (actual: {self._estado}).")
        self._estado = CONFIRMADA
        log.info("Reserva #%s confirmada", self.id)

    def cancelar(self) -> None:
        if self._estado in (CANCELADA, PROCESADA):
            raise OperacionNoPermitidaError(
                f"No se puede cancelar una reserva {self._estado}.")
        self._estado = CANCELADA
        log.info("Reserva #%s cancelada", self.id)

    def procesar(self, descuento: float = 0.0) -> float:
        """Calcula el costo final con IVA y marca la reserva como PROCESADA.

        Usa try/except/finally: el ``finally`` deja siempre constancia en el log.
        """
        try:
            if self._estado != CONFIRMADA:
                raise OperacionNoPermitidaError(
                    f"Debe confirmar la reserva antes de procesarla (actual: {self._estado}).")
            costo = self._servicio.calcular_costo(self._duracion, IVA, descuento)
        except SoftwareFJError as error:
            log.error("Reserva #%s no se pudo procesar: %s", self.id, error)
            raise
        else:
            self._estado = PROCESADA
            log.info("Reserva #%s procesada. Total: $%s", self.id, f"{costo:,.2f}")
            return costo
        finally:
            log.info("Fin del intento de procesamiento de la reserva #%s", self.id)

    def describir(self) -> str:
        return (f"Reserva #{self.id} [{self._estado}] {self._cliente.nombre} -> "
                f"{self._servicio.nombre} ({self._duracion} h)")
