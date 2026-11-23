# Módulo bitacora: guarda en un archivo los eventos y los errores del sistema (módulo logging).
import logging
import os

RUTA_BITACORA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bitacora.log")

logging.basicConfig(
    filename=RUTA_BITACORA,
    level=logging.INFO,
    encoding="utf-8",
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
)


def evento(mensaje):
    # Registra una acción normal del sistema (nivel INFO)
    logging.info(mensaje)


def error(mensaje):
    # Registra un problema (nivel ERROR)
    logging.error(mensaje)
