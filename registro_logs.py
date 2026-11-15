"""Configuración del archivo de logs (errores y eventos relevantes).

Es el único uso de archivos permitido por el enunciado: no hay base de datos.
"""

import logging
from pathlib import Path

RUTA_LOGS = Path(__file__).resolve().parent / "logs"
ARCHIVO_LOG = RUTA_LOGS / "software_fj.log"


def obtener_logger() -> logging.Logger:
    """Devuelve el logger del sistema, configurándolo solo la primera vez."""
    logger = logging.getLogger("software_fj")
    if logger.handlers:  # ya configurado
        return logger

    logger.setLevel(logging.INFO)
    RUTA_LOGS.mkdir(exist_ok=True)

    manejador = logging.FileHandler(ARCHIVO_LOG, mode="w", encoding="utf-8")
    manejador.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s",
                          datefmt="%Y-%m-%d %H:%M:%S")
    )
    logger.addHandler(manejador)
    logger.propagate = False
    return logger


log = obtener_logger()
