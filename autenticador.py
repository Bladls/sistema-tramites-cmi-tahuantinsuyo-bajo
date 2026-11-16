# Módulo autenticador: controla el acceso según el rol (contraseña).

class Autenticador:
    def roles(self):
        return ["Ventanilla", "Jefatura", "Archivo"]

    def validar(self, rol, clave):
        if rol == "Ventanilla":
            return clave == "1234"
        elif rol == "Jefatura":
            return clave == "Jefe2026"
        elif rol == "Archivo":
            return clave == "Admin123"
        else:
            return False
