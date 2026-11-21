def limpiar_nombre(texto):
    palabras = texto.split()
    resultado = []
    for p in palabras:
        resultado.append(p.capitalize())
    return " ".join(resultado)


def limpiar_texto(texto):
    return " ".join(texto.replace("|", "").split())

def solo_numeros(texto):
    # Desafío 6: acepta solo los dígitos 0 al 9 del teclado (isdigit también acepta "²")
    if texto == "":
        return False
    for caracter in texto:
        if caracter < "0" or caracter > "9":
            return False
    return True

def es_dni_valido(dni):
    return len(dni) == 8 and solo_numeros(dni)


def es_vacio(texto):
    return texto.strip() == ""


def a_entero(texto):
    texto = texto.strip()
    if solo_numeros(texto):
        return int(texto)
    return None

def clave_orden(texto):
    # Desafío 6: quita las tildes para ordenar; la ñ va después de la n
    texto = texto.lower()
    texto = texto.replace("á", "a").replace("é", "e").replace("í", "i")
    texto = texto.replace("ó", "o").replace("ú", "u").replace("ü", "u")
    texto = texto.replace("ñ", "n~")
    return texto