"""Gestor central: guarda clientes, servicios y reservas en listas internas."""

from functools import singledispatchmethod

from cliente import Cliente
from excepciones import ReservaError, SoftwareFJError
from registro_logs import log
from reserva import Reserva
from servicios import Servicio


class GestorSoftwareFJ:
    def __init__(self) -> None:
        self._clientes: list[Cliente] = []
        self._servicios: list[Servicio] = []
        self._reservas: list[Reserva] = []

    # --- sobrecarga por tipo con singledispatchmethod ---
    @singledispatchmethod
    def registrar(self, objeto):
        raise ReservaError(f"No se puede registrar un objeto de tipo {type(objeto).__name__}.")

    @registrar.register
    def _(self, objeto: Cliente):
        self._clientes.append(objeto)
        log.info("Cliente registrado: %s", objeto.nombre)

    @registrar.register
    def _(self, objeto: Servicio):
        self._servicios.append(objeto)
        log.info("Servicio registrado: %s", objeto.nombre)

    @registrar.register
    def _(self, objeto: Reserva):
        self._reservas.append(objeto)

    def intentar(self, descripcion: str, operacion):
        """Ejecuta una operación; si falla, registra el error y el sistema continúa."""
        print(f"\n>> {descripcion}")
        try:
            resultado = operacion()
        except SoftwareFJError as error:
            log.error("%s -> %s: %s", descripcion, type(error).__name__, error)
            print(f"   [ERROR CONTROLADO] {type(error).__name__}: {error}")
            if error.__cause__:
                print(f"   (causa original: {type(error.__cause__).__name__}: {error.__cause__})")
            return None
        except Exception as error:  # error inesperado: tampoco detiene el sistema
            log.critical("%s -> error inesperado %s: %s", descripcion,
                         type(error).__name__, error)
            print(f"   [ERROR INESPERADO] {type(error).__name__}: {error}")
            return None
        else:
            print(f"   [OK] {resultado if resultado is not None else 'Operación exitosa'}")
            return resultado
        finally:
            log.info("Operación finalizada: %s", descripcion)

    def resumen(self) -> str:
        return (f"Clientes: {len(self._clientes)} | Servicios: {len(self._servicios)} | "
                f"Reservas: {len(self._reservas)}")

    @property
    def reservas(self) -> list[Reserva]:
        return list(self._reservas)
