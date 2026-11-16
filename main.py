"""Simulación de 12 operaciones completas de Software FJ (sin base de datos).

Ejecutar:  python main.py
Los errores y eventos quedan en logs/software_fj.log
"""

from cliente import Cliente
from gestor import GestorSoftwareFJ
from registro_logs import ARCHIVO_LOG, log
from reserva import Reserva
from servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala


def main() -> None:
    g = GestorSoftwareFJ()
    log.info("=== Inicio de la simulación de Software FJ ===")

    # --- Clientes ---
    def registrar_cliente(*args):
        cliente = Cliente(*args)
        g.registrar(cliente)
        return cliente

    ana = g.intentar("1. Registrar cliente válido (Ana Pérez)",
                     lambda: registrar_cliente("ana pérez", "1002345678",
                                               "ana@correo.com", "3001234567"))
    luis = g.intentar("2. Registrar cliente válido (Luis Gómez)",
                      lambda: registrar_cliente("Luis Gómez", "79456123",
                                                "luis.gomez@mail.co", "3109876543"))
    g.intentar("3. Registrar cliente inválido (correo mal formado)",
               lambda: registrar_cliente("Carlos Ruiz", "123456789",
                                         "carlos-sin-arroba", "3001112233"))
    g.intentar("4. Registrar cliente con parámetros faltantes",
               lambda: registrar_cliente("Marta Díaz", "55667788"))

    # --- Servicios ---
    def registrar_servicio(servicio):
        g.registrar(servicio)
        return servicio.describir()

    sala = g.intentar("5. Crear servicio válido: sala de juntas",
                      lambda: ReservaSala("Sala Innovación", 50_000, 25))
    equipo = g.intentar("6. Crear servicio válido: alquiler de portátil",
                        lambda: AlquilerEquipo("Portátil Pro", 8_000, "Portátil"))
    asesoria = g.intentar("7. Crear servicio válido: asesoría senior",
                          lambda: AsesoriaEspecializada("Asesoría Cloud", 90_000, "senior"))
    g.intentar("8. Crear servicio inválido (tarifa negativa)",
               lambda: AlquilerEquipo("Proyector", -500, "Proyector"))
    g.intentar("9. Crear servicio inválido (nivel de asesoría inexistente)",
               lambda: AsesoriaEspecializada("Asesoría Legal", 70_000, "maestro"))

    for s in (sala, equipo, asesoria):
        if s:
            registrar_servicio(s)

    # --- Reservas ---
    def reservar_y_procesar(cliente, servicio, horas, descuento=0.0):
        reserva = Reserva(cliente, servicio, horas)
        g.registrar(reserva)
        reserva.confirmar()
        total = reserva.procesar(descuento)
        return f"{reserva.describir()} -> Total con IVA: ${total:,.2f}"

    g.intentar("10. Reserva exitosa: Ana reserva la sala 3 h",
               lambda: reservar_y_procesar(ana, sala, 3))
    g.intentar("11. Reserva exitosa con 10 % de descuento: Luis, asesoría 2 h",
               lambda: reservar_y_procesar(luis, asesoria, 2, descuento=0.10))
    g.intentar("12. Reserva fallida: duración fuera de rango (sala 12 h)",
               lambda: reservar_y_procesar(ana, sala, 12))

    if equipo:
        equipo.disponible = False
    g.intentar("13. Reserva fallida: servicio no disponible",
               lambda: reservar_y_procesar(luis, equipo, 5))
    if equipo:
        equipo.disponible = True

    def cancelar_y_reconfirmar():
        reserva = Reserva(ana, equipo, 24)
        g.registrar(reserva)
        reserva.cancelar()
        reserva.confirmar()  # operación no permitida

    g.intentar("14. Operación no permitida: confirmar una reserva cancelada",
               cancelar_y_reconfirmar)
    g.intentar("15. Procesar una reserva sin confirmarla",
               lambda: Reserva(luis, sala, 2).procesar())
    g.intentar("16. Cálculo inconsistente (descuento del 150 %)",
               lambda: sala.calcular_costo(2, 0.19, 1.5))
    g.intentar("17. Registrar un objeto que no es entidad del sistema",
               lambda: g.registrar("esto no es un cliente"))

    # --- Demostración de sobrecarga de calcular_costo ---
    print("\n>> Sobrecarga de calcular_costo (sala, 2 h):")
    print(f"   solo base:            ${sala.calcular_costo(2):,.2f}")
    print(f"   con IVA 19 %:         ${sala.calcular_costo(2, 0.19):,.2f}")
    print(f"   con IVA y 10 % desc.: ${sala.calcular_costo(2, 0.19, 0.10):,.2f}")

    print(f"\n{g.resumen()}")
    print("\nEstado final de las reservas:")
    for r in g.reservas:
        print("  -", r)

    log.info("=== Fin de la simulación: el sistema siguió operativo ===")
    print(f"\nEl sistema terminó sin interrupciones. Revise el log en: {ARCHIVO_LOG}")


if __name__ == "__main__":
    main()
