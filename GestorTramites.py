# --- SUBIDO POR JOSUE ---
# Módulo gestor: administra la lista de trámites y todas las operaciones del sistema.
from datetime import datetime
from Tramite import Tramite
from archivo_datos import cargar_tramites, guardar_tramites

TIPOS = ["Referencia", "SIS", "Certificado_Salud", "Descanso_Medico"]
ESTADOS = ["Registrado", "En evaluacion", "Denegado", "Aprobado"]
AREAS = ["Jefatura", "Archivo", "Medico Jefe", "Diris Lima norte", "Hospital Referencia"]

# 2. Definición del Gestor
class GestorTramites:
    def __init__(self):
        self.lista_tramites = cargar_tramites()

    def siguiente_codigo(self):
        mayor = 0
        for t in self.lista_tramites:
            if t.codigo > mayor:
                mayor = t.codigo
        return mayor + 1

    def agregar(self, dni, nombre, apellido, tipo):
        fecha = datetime.now().strftime("%d/%m/%Y")
        nuevo = Tramite(self.siguiente_codigo(), fecha, tipo, dni, nombre, apellido, "Jefatura", "Registrado")
        self.lista_tramites.append(nuevo)
        guardar_tramites(self.lista_tramites)
        return nuevo

    def buscar(self, codigo):
        # Búsqueda secuencial: devuelve la posición o -1
        for i in range(len(self.lista_tramites)):
            if self.lista_tramites[i].codigo == codigo:
                return i
        return -1

    def obtener(self, codigo):
        pos = self.buscar(codigo)
        if pos == -1:
            return None
        return self.lista_tramites[pos]

    def modificar(self, codigo, estado, area):
        tramite = self.obtener(codigo)
        if tramite is None:
            return False
        tramite.estado = estado
        tramite.area = area
        guardar_tramites(self.lista_tramites)
        return True

    def eliminar(self, codigo):
        pos = self.buscar(codigo)
        if pos == -1:
            return None
        eliminado = self.lista_tramites.pop(pos)
        guardar_tramites(self.lista_tramites)
        return eliminado

    def ordenar_burbuja(self):
        # Ordena por apellido y, si empata, por nombre
        lista = self.lista_tramites
        n = len(lista)
        for i in range(n - 1):
            for j in range(n - 1 - i):
                a = lista[j]
                b = lista[j + 1]
                if a.apellido > b.apellido or (a.apellido == b.apellido and a.nombre > b.nombre):
                    lista[j] = b
                    lista[j + 1] = a

    def obtener_todos(self):
        self.ordenar_burbuja()
        return self.lista_tramites

    def reporte_archivo(self):
        lista = []
        for t in self.obtener_todos():
            if t.area == "Archivo":
                lista.append(t)
        return lista
