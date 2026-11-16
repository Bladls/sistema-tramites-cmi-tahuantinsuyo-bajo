# Módulo archivo_datos: guarda y lee los trámites en un archivo de texto.
# Cada trámite es una línea y sus datos van separados por el símbolo |
# Formato: codigo|fecha|tipo|dni|nombre|apellido|area|estado

import os
from Tramite import Tramite

RUTA = "tramites.txt"


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
