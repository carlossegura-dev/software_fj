# Software FJ – Sistema integral de gestión de clientes, servicios y reservas

Proyecto de Programación Orientada a Objetos en Python (UNAD – Programación, cód. 213023).
Sin base de datos: todo se gestiona con objetos y listas internas; el único archivo que se
escribe es el log de eventos y errores.

## Ejecución

```bash
python main.py
```

Requiere Python 3.9 o superior. No usa librerías externas. El log queda en `logs/software_fj.log`.

## Estructura

| Archivo | Contenido |
|---|---|
| `excepciones.py` | Jerarquía de excepciones personalizadas (`SoftwareFJError` y 7 derivadas). |
| `registro_logs.py` | Configuración del archivo de logs. |
| `entidad.py` | Clase abstracta `Entidad` (id único + `describir()` abstracto). |
| `cliente.py` | `Cliente` con atributos privados y validación en cada *setter*. |
| `servicios.py` | `Servicio` (abstracta) y `ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada`. |
| `reserva.py` | `Reserva`: confirmar, cancelar y procesar, con estados. |
| `gestor.py` | `GestorSoftwareFJ`: listas internas, `registrar` sobrecargado y `intentar()` que evita que el sistema se caiga. |
| `main.py` | Simulación de 17 operaciones (válidas e inválidas). |

## Conceptos aplicados

- **Abstracción:** `Entidad` y `Servicio` son clases abstractas (`ABC`).
- **Herencia y polimorfismo:** los tres servicios sobrescriben `describir`, `validar_parametros` y `_tarifa_base`; `AlquilerEquipo` además sobrescribe `calcular_costo`.
- **Encapsulación:** atributos privados con `@property` y validación en los *setters*.
- **Sobrecarga:** `calcular_costo(duracion, impuesto=0, descuento=0)` con tres variantes de llamada, y `GestorSoftwareFJ.registrar` con `singledispatchmethod` según el tipo.
- **Excepciones:** personalizadas, `try/except`, `try/except/else`, `try/except/finally` y encadenamiento con `raise ... from ...` (ver `Reserva.__init__` y `Reserva.procesar`).
- **Logs:** cada error y evento relevante se registra en `logs/software_fj.log`.

## Trabajo en equipo (GitHub)

Cada integrante debe trabajar en su propia rama y hacer *commits* con su nombre, por ejemplo:

```bash
git checkout -b feature/nombre-integrante
git add .
git commit -m "Describe el aporte"
git push origin feature/nombre-integrante
```
