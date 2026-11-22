# Módulo gestor: administra la lista de trámites y todas las operaciones del sistema.
from datetime import datetime
from tramite import Tramite
from archivo_datos import cargar_tramites, guardar_tramites, cargar_contador, guardar_contador
from texto import clave_orden

TIPOS = ["Referencia", "SIS", "Certificado_Salud", "Descanso_Medico"]
ESTADOS = ["Registrado", "En evaluacion", "Denegado", "Aprobado"]
AREAS = ["Jefatura", "Archivo", "Medico Jefe", "Diris Lima norte", "Hospital Referencia"]

# 2. Definición del Gestor
class GestorTramites:
    def __init__(self):
        self.lista_tramites = cargar_tramites()

    def siguiente_codigo(self):
        mayor = cargar_contador()
        for t in self.lista_tramites:
            if t.codigo > mayor:
                mayor = t.codigo
        return mayor + 1

    def agregar(self, dni, nombre, apellido, tipo):
        fecha = datetime.now().strftime("%d/%m/%Y")
        nuevo = Tramite(self.siguiente_codigo(), fecha, tipo, dni, nombre, apellido, "Jefatura", "Registrado")
        self.lista_tramites.append(nuevo)
        guardar_tramites(self.lista_tramites)
        guardar_contador(nuevo.codigo)  
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
                apellido_a = clave_orden(a.apellido)
                apellido_b = clave_orden(b.apellido)
                if apellido_a > apellido_b or (apellido_a == apellido_b and clave_orden(a.nombre) > clave_orden(b.nombre)):
                    lista[j] = b
                    lista[j + 1] = a


    def ordenar_por_codigo(self):
        # Ordena por código de menor a mayor (orden de llegada a mesa de partes)
        lista = self.lista_tramites
        n = len(lista)
        for i in range(n - 1):
            for j in range(n - 1 - i):
                a = lista[j]
                b = lista[j + 1]
                if a.codigo > b.codigo:
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

    def ordenar_seleccion(self):
        # Método selección: en cada vuelta busca el menor apellido (y nombre) y lo pone en su lugar
        lista = self.lista_tramites
        n = len(lista)
        for i in range(n - 1):
            menor = i
            for j in range(i + 1, n):
                a = lista[j]
                b = lista[menor]
                apellido_a = clave_orden(a.apellido)
                apellido_b = clave_orden(b.apellido)
                if apellido_a < apellido_b or (apellido_a == apellido_b and clave_orden(a.nombre) < clave_orden(b.nombre)):
                    menor = j
            if menor != i:
                temporal = lista[i]
                lista[i] = lista[menor]
                lista[menor] = temporal

    def buscar_por_apellido(self, texto):
        # Búsqueda por apellido: sin tildes ni mayúsculas y por parte del apellido (find = IndexOf)
        texto = clave_orden(texto.strip())
        encontrados = []
        for t in self.lista_tramites:
            if clave_orden(t.apellido).find(texto) != -1:
                encontrados.append(t)
        return encontrados
    
    def como_matriz(self):
        # Matriz (lista de listas): matriz[i][j] es el dato j del trámite i, en el orden de la tabla
        matriz = []
        for t in self.obtener_todos():
            fila = [t.codigo, t.dni, t.nombre, t.apellido, t.tipo, t.area, t.estado, t.fecha]
            matriz.append(fila)
        return matriz
    
    def resumen_estados(self):
        # Arreglos paralelos: estados[i] y cantidades[i] se refieren al mismo estado
        estados = []
        cantidades = []
        for e in ESTADOS:
            estados.append(e)
            cantidades.append(0)
        for t in self.lista_tramites:
            for i in range(len(estados)):
                if t.estado == estados[i]:
                    cantidades[i] = cantidades[i] + 1
        return estados, cantidades

    def buscar_recursivo(self, codigo, i=0):
        # Búsqueda recursiva: revisa la posición i y, si no es, se llama con i + 1
        if i >= len(self.lista_tramites):
            return -1
        if self.lista_tramites[i].codigo == codigo:
            return i
        return self.buscar_recursivo(codigo, i + 1)
    
    def contar_en_area(self, area, i=0):
        # Conteo recursivo de los trámites de un área
        if i >= len(self.lista_tramites):
            return 0
        if self.lista_tramites[i].area == area:
            suma = 1
        else:
            suma = 0
        return suma + self.contar_en_area(area, i + 1)
