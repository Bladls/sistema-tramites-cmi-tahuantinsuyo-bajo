# Módulo archivo_datos: guarda y lee los trámites en un archivo de texto.
# Cada trámite es una línea y sus datos van separados por el símbolo |
# Formato: codigo|fecha|tipo|dni|nombre|apellido|area|estado

import os
from tramite import Tramite

RUTA = "tramites.txt"
RUTA_CONTADOR = "contador.txt"  # guarda el último código entregado


def guardar_tramites(lista_tramites):
    with open(RUTA, "w", encoding="utf-8") as archivo:
        for t in lista_tramites:
            datos = [str(t.codigo), t.fecha, t.tipo, t.dni, t.nombre, t.apellido, t.area, t.estado]
            archivo.write("|".join(datos) + "\n")


def cargar_tramites():
    lista = []
    if not os.path.exists(RUTA):
        return lista

    with open(RUTA, "r", encoding="utf-8") as archivo:
        for linea in archivo.read().split("\n"):
            partes = linea.split("|")
            if len(partes) == 8 and partes[0].isdigit():
                tramite = Tramite(int(partes[0]), partes[1], partes[2], partes[3], partes[4], partes[5], partes[6], partes[7])
                lista.append(tramite)
    return lista


def guardar_contador(codigo):
    # Guarda el último código entregado, para que no se repita aunque se elimine el trámite
    with open(RUTA_CONTADOR, "w", encoding="utf-8") as archivo:
        archivo.write(str(codigo))


def cargar_contador():
    # Devuelve el último código entregado, o 0 si el archivo todavía no existe
    if not os.path.exists(RUTA_CONTADOR):
        return 0

    with open(RUTA_CONTADOR, "r", encoding="utf-8") as archivo:
        texto = archivo.read().strip()
    if texto.isdigit():
        return int(texto)
    return 0
