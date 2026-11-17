# Módulo principal: une todas las clases y controla el formulario (Tkinter).
from tkinter import Tk, Frame, Label, LabelFrame
from tkinter import ttk

from GestorTramites import GestorTramites, TIPOS, ESTADOS, AREAS
from autenticador import Autenticador
import mensajes
from texto import limpiar_nombre, limpiar_texto, es_dni_valido, es_vacio, a_entero
from controles import crear_caja, crear_combo, crear_boton, poner_texto, limpiar

COLUMNAS = ("Código", "DNI", "Nombres", "Apellidos", "Tipo", "Área", "Estado", "Fecha")


class VentanaAcceso:
    def __init__(self, ventana, al_ingresar):
        self.ventana = ventana
        self.al_ingresar = al_ingresar
        self.autenticador = Autenticador()

        self.marco = Frame(ventana, padx=20, pady=20)
        self.marco.pack()
        Label(self.marco, text="Acceso al sistema de trámites", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=8)
        self.cboRol = crear_combo(self.marco, "Rol:", self.autenticador.roles(), 1)
        self.txtClave = crear_caja(self.marco, "Contraseña:", 2, oculto=True)
        crear_boton(self.marco, "Ingresar", self.ingresar, 3, 1)
        self.txtClave.bind("<Return>", lambda e: self.ingresar())

    def ingresar(self):
        rol = self.cboRol.get()
        if rol == "":
            mensajes.error("Seleccione un rol.")
            return
        if not self.autenticador.validar(rol, self.txtClave.get()):
            mensajes.error("Contraseña incorrecta.")
            self.txtClave.delete(0, "end")
            return
        self.marco.destroy()
        self.al_ingresar(rol)


class VentanaTramites:
    def __init__(self, ventana, rol):
        self.ventana = ventana
        self.rol = rol
        self.gestor = GestorTramites()
        ventana.title("Sistema de Trámites - CMI Tahuantinsuyo Bajo [" + rol + "]")

        # Datos del trámite
        datos = LabelFrame(ventana, text="Datos del trámite", padx=10, pady=5)
        datos.pack(fill="x", padx=10, pady=5)
        self.txtCodigo = crear_caja(datos, "Código:", 0)
        self.txtDni = crear_caja(datos, "DNI:", 1)
        self.txtNombre = crear_caja(datos, "Nombres:", 2)
        self.txtApellido = crear_caja(datos, "Apellidos:", 3)
        self.cboTipo = crear_combo(datos, "Tipo de trámite:", TIPOS, 0, 2)
        self.cboArea = crear_combo(datos, "Área:", AREAS, 1, 2)
        self.cboEstado = crear_combo(datos, "Estado:", ESTADOS, 2, 2)

        # Botones
        acciones = Frame(ventana)
        acciones.pack(padx=10)
        self.btnRegistrar = crear_boton(acciones, "Registrar", self.registrar, 0, 0)
        crear_boton(acciones, "Buscar", self.buscar, 0, 1)
        self.btnModificar = crear_boton(acciones, "Modificar", self.modificar, 0, 2)
        self.btnEliminar = crear_boton(acciones, "Eliminar", self.eliminar, 0, 3)
        crear_boton(acciones, "Mostrar", self.mostrar, 1, 0)
        crear_boton(acciones, "Reporte Archivo", self.reporte_archivo, 1, 1)
        crear_boton(acciones, "Limpiar", self.limpiar, 1, 2)
        crear_boton(acciones, "Salir", ventana.destroy, 1, 3)
        self.aplicar_permisos()

        # Tabla de datos (Treeview)
        tabla_marco = Frame(ventana)
        tabla_marco.pack(fill="both", expand=True, padx=10, pady=5)
        self.tabla = ttk.Treeview(tabla_marco, columns=COLUMNAS, show="headings", height=10)
        for col in COLUMNAS:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=110, anchor="w")
        barra = ttk.Scrollbar(tabla_marco, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=barra.set)
        self.tabla.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_fila)

        self.lblTotal = Label(ventana, text="")
        self.lblTotal.pack(pady=3)
        self.mostrar()

    # ---------- utilidades del formulario ----------
    def aplicar_permisos(self):
        if self.rol == "Archivo":
            self.btnRegistrar.config(state="disabled")
        if self.rol != "Jefatura":
            self.btnModificar.config(state="disabled")
            self.btnEliminar.config(state="disabled")

    def limpiar(self):
        limpiar([self.txtCodigo, self.txtDni, self.txtNombre, self.txtApellido],
                [self.cboTipo, self.cboArea, self.cboEstado])

    def llenar_campos(self, t):
        poner_texto(self.txtCodigo, str(t.codigo))
        poner_texto(self.txtDni, t.dni)
        poner_texto(self.txtNombre, t.nombre)
        poner_texto(self.txtApellido, t.apellido)
        self.cboTipo.set(t.tipo)
        self.cboArea.set(t.area)
        self.cboEstado.set(t.estado)

    def leer_codigo(self):
        codigo = a_entero(self.txtCodigo.get())
        if codigo is None:
            mensajes.error("Ingrese un código numérico.")
        return codigo

    def llenar_tabla(self, lista):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        for t in lista:
            self.tabla.insert("", "end", values=(t.codigo, t.dni, t.nombre, t.apellido, t.tipo, t.area, t.estado, t.fecha))
        self.lblTotal.config(text="Trámites mostrados: " + str(len(lista)))

    def seleccionar_fila(self, evento):
        seleccion = self.tabla.selection()
        if seleccion:
            codigo = int(self.tabla.item(seleccion[0], "values")[0])
            tramite = self.gestor.obtener(codigo)
            if tramite is not None:
                self.llenar_campos(tramite)

    # ---------- acciones de los botones ----------
    def registrar(self):
        dni = self.txtDni.get().strip()
        nombre = limpiar_nombre(limpiar_texto(self.txtNombre.get()))
        apellido = limpiar_nombre(limpiar_texto(self.txtApellido.get()))
        tipo = self.cboTipo.get()

        if es_vacio(dni):
            mensajes.error("Ingrese el DNI.")
        elif not es_dni_valido(dni):
            mensajes.error("El DNI debe tener exactamente 8 dígitos numéricos.")
        elif es_vacio(nombre):
            mensajes.error("Ingrese los nombres.")
        elif es_vacio(apellido):
            mensajes.error("Ingrese los apellidos.")
        elif tipo == "":
            mensajes.error("Seleccione el tipo de trámite.")
        elif not mensajes.confirmar("¿El ciudadano cumple con todos los requisitos?"):
            mensajes.aviso("Registro cancelado: faltan requisitos.")
        else:
            t = self.gestor.agregar(dni, nombre, apellido, tipo)
            mensajes.correcto("CARGO DE RECEPCIÓN\n\n"
                              "Código: " + str(t.codigo) + "\n"
                              "Fecha: " + t.fecha + "\n"
                              "Solicitante: " + t.nombre + " " + t.apellido + "\n"
                              "DNI: " + t.dni + "\n"
                              "Tipo: " + t.tipo + "\n"
                              "Área: " + t.area + "\n"
                              "Plazo estimado: 3 a 7 días hábiles")
            self.limpiar()
            self.mostrar()

    def buscar(self):
        codigo = self.leer_codigo()
        if codigo is None:
            return
        tramite = self.gestor.obtener(codigo)
        if tramite is None:
            mensajes.error("Trámite no encontrado.")
        else:
            self.llenar_campos(tramite)

    def modificar(self):
        codigo = self.leer_codigo()
        if codigo is None:
            return
        estado = self.cboEstado.get()
        area = self.cboArea.get()
        if estado == "" or area == "":
            mensajes.error("Seleccione el estado y el área.")
        elif self.gestor.modificar(codigo, estado, area):
            mensajes.correcto("Trámite " + str(codigo) + " actualizado y derivado a " + area + ".")
            self.limpiar()
            self.mostrar()
        else:
            mensajes.error("Trámite no encontrado.")

    def eliminar(self):
        codigo = self.leer_codigo()
        if codigo is None:
            return
        if self.gestor.obtener(codigo) is None:
            mensajes.error("Trámite no encontrado.")
            return
        if not mensajes.confirmar("¿Eliminar el trámite " + str(codigo) + "?"):
            return
        eliminado = self.gestor.eliminar(codigo)
        mensajes.correcto("Trámite " + str(eliminado.codigo) + " de " + eliminado.nombre + " eliminado.")
        self.limpiar()
        self.mostrar()

    def mostrar(self):
        self.llenar_tabla(self.gestor.obtener_todos())

    def reporte_archivo(self):
        lista = self.gestor.reporte_archivo()
        self.llenar_tabla(lista)
        if len(lista) == 0:
            mensajes.aviso("No hay trámites en el área de Archivo.")


def main():
    ventana = Tk()
    ventana.title("Sistema de Trámites - CMI Tahuantinsuyo Bajo")
    VentanaAcceso(ventana, lambda rol: VentanaTramites(ventana, rol))
    ventana.mainloop()


if __name__ == "__main__":
    main()
