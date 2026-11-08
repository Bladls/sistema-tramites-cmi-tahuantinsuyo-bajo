# Módulo tramite: define los datos de un trámite.

class Tramite:
    def __init__(self, codigo, fecha, tipo, dni, nombre, apellido, area, estado):
        self.codigo = codigo
        self.fecha = fecha
        self.tipo = tipo
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.area = area
        self.estado = estado
