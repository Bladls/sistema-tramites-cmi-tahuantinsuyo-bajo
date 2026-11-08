# Módulo archivo_datos: guarda y lee los trámites en un archivo de texto.
# Cada trámite es una línea y sus datos van separados por el símbolo |
# Formato: codigo|fecha|tipo|dni|nombre|apellido|area|estado

from tramite import Tramite


def guardar_tramites(lista_tramites):
    # Se arma un solo texto con una línea por trámite
    texto = ""
    for t in lista_tramites:
        linea = str(t.codigo) + "|" + t.fecha + "|" + t.tipo + "|" + t.dni + "|" + t.nombre + "|" + t.apellido + "|" + t.area + "|" + t.estado
        texto = texto + linea + "\n"

    with open("tramites.txt", "w") as archivo:
        archivo.write(texto)


def cargar_tramites():
    lista = []

    with open("tramites.txt", "r") as archivo:
        contenido = archivo.read()

    lineas = contenido.split("\n")
    for linea in lineas:
        if linea != "":
            partes = linea.split("|")
            if len(partes) == 8:
                tramite = Tramite(int(partes[0]), partes[1], partes[2], partes[3], partes[4], partes[5], partes[6], partes[7])
                lista.append(tramite)
    return lista


def siguiente_codigo(lista_tramites):
    # El nuevo código es el mayor código guardado + 1
    mayor = 0
    for t in lista_tramites:
        if t.codigo > mayor:
            mayor = t.codigo
    return mayor + 1