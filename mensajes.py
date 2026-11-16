# Mensajes emergentes reutilizables (messagebox).
from tkinter import messagebox


def error(mensaje):
    messagebox.showerror("Error", mensaje)


def correcto(mensaje):
    messagebox.showinfo("Correcto", mensaje)


def aviso(mensaje):
    messagebox.showwarning("Aviso", mensaje)


def confirmar(mensaje):
    return messagebox.askyesno("Confirmar", mensaje)