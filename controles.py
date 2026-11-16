# Creación de controles del formulario que se repiten (Label + Entry, combos, botones).
from tkinter import Label, Entry, Button, END
from tkinter import ttk


def crear_caja(ventana, texto, fila, columna=0, ancho=25, oculto=False):
    Label(ventana, text=texto).grid(row=fila, column=columna, sticky="w", padx=5, pady=3)
    if oculto:
        caja = Entry(ventana, width=ancho, show="*")
    else:
        caja = Entry(ventana, width=ancho)
    caja.grid(row=fila, column=columna + 1, padx=5, pady=3)
    return caja


def crear_combo(ventana, texto, opciones, fila, columna=0, ancho=22):
    Label(ventana, text=texto).grid(row=fila, column=columna, sticky="w", padx=5, pady=3)
    combo = ttk.Combobox(ventana, values=opciones, state="readonly", width=ancho)
    combo.grid(row=fila, column=columna + 1, padx=5, pady=3)
    return combo


def crear_boton(ventana, texto, accion, fila, columna):
    boton = Button(ventana, text=texto, width=14, command=accion)
    boton.grid(row=fila, column=columna, padx=4, pady=4)
    return boton


def poner_texto(caja, texto):
    caja.delete(0, END)
    caja.insert(0, texto)


def limpiar(cajas, combos):
    for caja in cajas:
        caja.delete(0, END)
    for combo in combos:
        combo.set("")
    if len(cajas) > 0:
        cajas[0].focus()
