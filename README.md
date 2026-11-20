# Software FJ – Sistema integral de gestión de clientes, servicios y reservas

Proyecto de Programación Orientada a Objetos en Python (UNAD – Programación, cód. 213023).
Sin base de datos: todo se gestiona con objetos y listas internas; el único archivo que se
escribe es el log de eventos y errores.

## Ejecución

```bash
python main.py
```

Requiere Python 3.9 o superior. No usa librerías externas. El log queda en `logs/software_fj.log`.

## Pruebas

```bash
python -m unittest -v
```

Ejecute `python main.py` al final: las pruebas sobrescriben el log.

## Estructura

| Archivo | Contenido |
|---|---|
| `excepciones.py` | Jerarquía de excepciones personalizadas (`SoftwareFJError` y 8 derivadas, incluida `ClienteDuplicadoError`). |
| `registro_logs.py` | Configuración del archivo de logs. |
| `entidad.py` | Clase abstracta `Entidad` (id único + `describir()` abstracto). |
| `cliente.py` | `Cliente` con atributos privados y validación en cada *setter*. |
| `servicios.py` | `Servicio` (abstracta) y `ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada`. |
| `reserva.py` | `Reserva`: confirmar, cancelar y procesar, con estados. |
| `gestor.py` | `GestorSoftwareFJ`: listas internas, `registrar` sobrecargado, `buscar_cliente`, rechazo de duplicados e `intentar()` que evita que el sistema se caiga. |
| `main.py` | Simulación de 18 operaciones (válidas e inválidas). |
| `test_gestor.py` | Pruebas unitarias (`unittest`) del gestor. |
| `.gitignore` | Excluye `__pycache__/` del repositorio. |

## Conceptos aplicados

- **Abstracción:** `Entidad` y `Servicio` son clases abstractas (`ABC`).
- **Herencia y polimorfismo:** los tres servicios sobrescriben `describir`, `validar_parametros` y `_tarifa_base`; `AlquilerEquipo` además sobrescribe `calcular_costo`.
- **Encapsulación:** atributos privados con `@property` y validación en los *setters*.
- **Sobrecarga:** `calcular_costo(duracion, impuesto=0, descuento=0)` con tres variantes de llamada, y `GestorSoftwareFJ.registrar` con `singledispatchmethod` según el tipo.
- **Excepciones:** personalizadas, `try/except`, `try/except/else`, `try/except/finally` y encadenamiento con `raise ... from ...` (ver `Reserva.__init__`).
- **Logs:** cada error y evento relevante se registra en `logs/software_fj.log`.

## Aportes por integrante

| Integrante | Aporte |
|---|---|
| Carlos Segura | Diseño y código base (entidades, cliente, servicios, reservas, gestor, excepciones, logs), simulación de 18 operaciones en `main.py`, revisión de Pull Requests y README |
| Duvan Villalba | Validaciones de nombre, documento, correo y teléfono en `Cliente` |
| Jhoser Ruiz | Validación de tipos de `impuesto` y `descuento` en `Servicio.calcular_costo` (`servicios.py`), que lanza `CalculoInconsistenteError` si no son numéricos |
| Jackelin Arias | `ClienteDuplicadoError`, rechazo de duplicados y `buscar_cliente` en el gestor, `.gitignore` y pruebas unitarias del gestor |

## Trabajo en equipo (GitHub)

Cada integrante trabajó en su propia rama y abrió un Pull Request hacia `main`, con *commits* a su nombre:

```bash
git checkout -b nombre-de-la-rama
git add archivo.py
git commit -m "Describe el aporte"
git push -u origin nombre-de-la-rama
```