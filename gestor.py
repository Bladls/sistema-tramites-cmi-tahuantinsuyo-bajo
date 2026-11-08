# --- SUBIDO POR JOSUE ---
# Módulo gestor: administra la lista de trámites y todas las operaciones del sistema.
from datetime import datetime
from tramite import Tramite
from archivo_datos import cargar_tramites, guardar_tramites, siguiente_codigo

# 2. Definición del Gestor
class GestorTramites:
    def __init__(self):
        # Al iniciar, se leen los trámites guardados en el archivo
        self.lista_tramites = cargar_tramites()
        self.contador_codigos = siguiente_codigo(self.lista_tramites)

    # FUNCIONALIDAD BASE 
    def registrar(self, rol):
        if rol == "archivo":
            print("\n[X] Acceso denegado: El personal de Archivo no puede registrar trámites.")
            return
            
        codigo_num = self.contador_codigos
        self.contador_codigos += 1
        dni = input("Ingrese DNI (8 dígitos obligatorios): ")
        while len(dni) != 8:
            print("[X] Error: El DNI debe tener exactamente 8 dígitos numéricos.")
            dni = input("Ingrese DNI (8 dígitos obligatorios): ")
        nombre = input("Ingrese Nombres: ")
        while nombre == "":
            print("[X] Error: El campo de nombres es obligatorio y no puede estar vacío.")
            nombre = input("Ingrese Nombres: ")
        apellido = input("Ingrese Apellidos: ")
        while apellido == "":
            print("[X] Error: El campo de apellidos es obligatorio y no puede estar vacío.")
            apellido = input("Ingrese Apellidos: ")
        tipo = ""
        while tipo != "Referencia" and tipo != "SIS" and tipo != "Certificado_Salud" and tipo != "Descanso_Medico":
            print("\nTipos de trámite disponibles:")
            print(f" 1. Referencia")
            print(f" 2. SIS")
            print(f" 3. Certificado_Salud")
            print(f" 4. Descanso_Medico")
            entrada = input("Escriba el tipo de trámite de la lista(1-4): ")
            if entrada == "1":
                tipo = "Referencia"
            elif entrada == "2":
                tipo = "SIS"
            elif entrada == "3":
                tipo = "Certificado_Salud"
            elif entrada == "4":
                tipo = "Descanso_Medico"
            else:
                print("[X] Error: Tipo de trámite inválido o vacío. Intente nuevamente.")
        requisitos = input("\n¿El ciudadano cumple con todos los requisitos? (si/no): ")
        while requisitos != "si" and requisitos != "no":
            print("[X] Error: Responda únicamente 'si' o 'no' (en minúsculas).")
            requisitos = input("¿El ciudadano cumple con todos los requisitos? (si/no): ")
        if requisitos == "no":
            print("\n[!] Registro cancelado: El trámite no puede proceder sin los requisitos completos.")
            self.contador_codigos -= 1 
            return
        fecha_actual = datetime.now().strftime("%d/%m/%Y")
        
        nuevo_tramite = Tramite(codigo_num, fecha_actual, tipo, dni, nombre, apellido, "Jefatura", "Registrado")
        self.lista_tramites.append(nuevo_tramite)
        guardar_tramites(self.lista_tramites)
        print("\n========================================")
        print("          CARGO DE RECEPCION            ")
        print("========================================")
        print(f" Codigo de Tramite : {codigo_num}")
        print(f" Fecha de Ingreso  : {fecha_actual}")
        print(f" Solicitante       : {nombre} {apellido}")
        print(f" DNI Ciudadano     : {dni}")
        print(f" Tipo de Tramite   : {tipo}")
        print(f" Estado Actual     : Registrado")
        print(f" Area Asignada     : Jefatura")
        print(f" Plazo Estimado    : 3 a 7 dias habiles")
        print("========================================")
        print(f" [OK] Tramite {codigo_num} registrado con exito.")

    def buscar_secuencialmente(self, cod_buscado):
        for i in range(len(self.lista_tramites)):
            if self.lista_tramites[i].codigo == cod_buscado:
                return i
        return -1