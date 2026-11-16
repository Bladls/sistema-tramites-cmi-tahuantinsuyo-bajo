def limpiar_nombre(texto):
    palabras = texto.split()
    resultado = []
    for p in palabras:
        resultado.append(p.capitalize())
    return " ".join(resultado)


def limpiar_texto(texto):
    return " ".join(texto.replace("|", "").split())


def es_dni_valido(dni):
    return len(dni) == 8 and dni.isdigit()


def es_vacio(texto):
    return texto.strip() == ""


def a_entero(texto):
    texto = texto.strip()
    if texto.isdigit():
        return int(texto)
    return None
