#Subido por Lino
# Módulo main: flujo principal del programa (roles y menú).
from gestor import GestorTramites
from autenticador import Autenticador


def main():
    gestor = GestorTramites()
    autenticador = Autenticador()

    if len(gestor.lista_tramites) > 0:
        print(f"[i] Se cargaron {len(gestor.lista_tramites)} trámites guardados.")

    activo = True
    while activo:
        print("\n=== SISTEMA DE TRÁMITES ===")
        print(" [1] Ventanilla")
        print(" [2] Jefatura")
        print(" [3] Archivo")
        print(" [4] Salir")

        opcion_rol = input("Elija una opcion: ")

        if opcion_rol == "4":
            print("\nSaliendo del sistema. ¡Hasta luego!")
            break

        elif opcion_rol == "1" or opcion_rol == "2" or opcion_rol == "3":
            rol = autenticador.iniciar_sesion(opcion_rol)

            if rol is None:
                continue

        else:
            print("\n[X] Opción inválida. Elija un número del 1 al 4.")
            continue

        sesion = True
        while sesion:
            print(f"\n--- MENU PRINCIPAL [{rol.upper()}] ---")
            print(" 1. Registrar \n 2. Consultar \n 3. Modificar (Solo Jefatura) \n 4. Eliminar (Solo Jefatura)")
            print(" 5. Reporte Archivo \n 6. Mostrar Trámites \n 7. Cerrar sesion \n 8. Apagar sistema")

            menu = input("Elija (1-8): ")

            if menu == "1": gestor.registrar(rol)
            elif menu == "2": gestor.consultar()
            elif menu == "3": gestor.cambiar_estado(rol)
            elif menu == "4": gestor.eliminar(rol)
            elif menu == "5": gestor.reporte_archivo()
            elif menu == "6":
                gestor.ordenar_por_nombre_burbuja()
                gestor.mostrar_matriz_bidimensional()
            elif menu == "7": sesion = False
            elif menu == "8":
                print("\n[i] Apagando el sistema por completo.")
                sesion = False
                activo = False
            else:
                print("\n[X] Opción inválida. Elija un número del 1 al 8.")


if __name__ == "__main__":
    main()
