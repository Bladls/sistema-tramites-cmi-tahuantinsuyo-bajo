# Módulo autenticador: controla el acceso según el rol (contraseña).

class Autenticador:

    def iniciar_sesion(self, opcion):
        if opcion == "1":
            rol = "ventanilla"
            nombre_rol = "Ventanilla"
            clave = "1234"
        elif opcion == "2":
            rol = "jefatura"
            nombre_rol = "Jefatura"
            clave = "Jefe2026"
        elif opcion == "3":
            rol = "archivo"
            nombre_rol = "Archivo"
            clave = "Admin123"
        else:
            return None

        intento = input("Ingrese la contraseña de " + nombre_rol + ": ")

        if intento == clave:
            print("\n[OK] Acceso concedido a " + nombre_rol + ".")
            return rol

        print("\n[X] Contraseña incorrecta. Acceso denegado.")
        return None
