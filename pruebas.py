# Pruebas automáticas (módulo unittest): comprueban la lógica del sistema sin abrir las ventanas.
# Ejecutar en la carpeta del proyecto:  python -m unittest pruebas -v
import os
import tempfile
import unittest

from texto import limpiar_nombre, limpiar_texto, es_dni_valido, a_entero, clave_orden, ocultar_dni
from GestorTramites import GestorTramites


class PruebasTexto(unittest.TestCase):
    def test_limpiar_nombre(self):
        self.assertEqual(limpiar_nombre(limpiar_texto("  juan   CARLOS|  ")), "Juan Carlos")

    def test_dni_valido(self):
        self.assertTrue(es_dni_valido("12345678"))

    def test_dni_invalido(self):
        for dni in ["1234567", "123456789", "1234567a", "²2345678", ""]:
            self.assertFalse(es_dni_valido(dni))

    def test_a_entero(self):
        self.assertEqual(a_entero(" 12 "), 12)
        self.assertIsNone(a_entero("abc"))

    def test_clave_orden_tildes_y_enie(self):
        self.assertEqual(clave_orden("Pérez"), "perez")
        self.assertTrue(clave_orden("Núñez") < clave_orden("Ñañez"))

    def test_ocultar_dni(self):
        self.assertEqual(ocultar_dni("70123456"), "70****56")


class PruebasGestor(unittest.TestCase):
    def setUp(self):
        # Cada prueba trabaja en una carpeta temporal para no tocar tramites.txt ni contador.txt reales
        self.carpeta = tempfile.TemporaryDirectory()
        self.anterior = os.getcwd()
        os.chdir(self.carpeta.name)
        self.gestor = GestorTramites()

    def tearDown(self):
        os.chdir(self.anterior)
        self.carpeta.cleanup()

    def cargar_tres(self):
        self.gestor.agregar("11111111", "Ana", "Torres", "SIS")
        self.gestor.agregar("22222222", "Luis", "Pérez", "Referencia")
        self.gestor.agregar("33333333", "Rosa", "Alva", "SIS")

    def test_codigos_correlativos_y_no_se_repiten(self):
        self.cargar_tramites = self.cargar_tres()
        self.assertEqual([t.codigo for t in self.gestor.lista_tramites], [1, 2, 3])
        self.gestor.eliminar(3)
        nuevo = GestorTramites().agregar("44444444", "Eva", "Núñez", "SIS")
        self.assertEqual(nuevo.codigo, 4)

    def test_ordenar_por_apellido(self):
        self.cargar_tres()
        self.gestor.ordenar_burbuja()
        self.assertEqual([t.apellido for t in self.gestor.lista_tramites], ["Alva", "Pérez", "Torres"])

    def test_ordenar_por_codigo(self):
        self.cargar_tres()
        self.gestor.ordenar_burbuja()
        self.gestor.ordenar_por_codigo()
        self.assertEqual([t.codigo for t in self.gestor.lista_tramites], [1, 2, 3])

    def test_seleccion_da_el_mismo_orden_que_burbuja(self):
        self.cargar_tres()
        self.gestor.ordenar_seleccion()
        por_seleccion = [t.apellido for t in self.gestor.lista_tramites]
        self.gestor.ordenar_burbuja()
        self.assertEqual(por_seleccion, [t.apellido for t in self.gestor.lista_tramites])

    def test_buscar_codigo_existente_e_inexistente(self):
        self.cargar_tres()
        self.assertEqual(self.gestor.buscar(2), 1)
        self.assertEqual(self.gestor.buscar(99), -1)
        self.assertEqual(self.gestor.buscar_recursivo(2), 1)

    def test_buscar_por_apellido(self):
        self.cargar_tres()
        self.assertEqual([t.apellido for t in self.gestor.buscar_por_apellido("per")], ["Pérez"])

    def test_modificar_y_reporte_archivo(self):
        self.cargar_tres()
        self.assertTrue(self.gestor.modificar(1, "Aprobado", "Archivo"))
        self.assertFalse(self.gestor.modificar(99, "Aprobado", "Archivo"))
        self.assertEqual(len(self.gestor.reporte_archivo()), 1)
        self.assertEqual(self.gestor.contar_en_area("Archivo"), 1)

    def test_archivo_guardado_en_ansi_se_lee_sin_error(self):
        # Error corregido: un tramites.txt guardado como ANSI (con ñ) antes hacía caer el programa
        linea = "1|22/11/2026|SIS|11111111|Ana|Ñañez|Jefatura|Registrado\n"
        with open("tramites.txt", "wb") as archivo:
            archivo.write(linea.encode("latin-1"))
        lista = GestorTramites().lista_tramites
        self.assertEqual(len(lista), 1)
        self.assertEqual(lista[0].apellido, "Ñañez")


if __name__ == "__main__":
    unittest.main()
