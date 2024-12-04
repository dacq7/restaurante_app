import sqlite3
import tkinter as tk
from tkinter import ttk

# Ruta de la base de datos
DB_PATH = "./database/restaurante.db"

def obtener_productos():
    """Consulta los productos desde la base de datos."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM menu")
        return cursor.fetchall()

def mostrar_menu():
    """Crea la ventana para mostrar el menú del restaurante."""
    # Crear ventana principal
    ventana = tk.Tk()
    ventana.title("Menú del Restaurante")
    ventana.geometry("600x400")

    # Etiqueta de título
    titulo = tk.Label(ventana, text="Menú del Restaurante", font=("Arial", 16, "bold"))
    titulo.pack(pady=10)

    # Crear tabla
    columnas = ("ID", "Nombre", "Descripción", "Precio")
    tabla = ttk.Treeview(ventana, columns=columnas, show="headings", height=15)
    tabla.heading("ID", text="ID")
    tabla.heading("Nombre", text="Nombre")
    tabla.heading("Descripción", text="Descripción")
    tabla.heading("Precio", text="Precio")

    # Ajustar tamaño de las columnas
    tabla.column("ID", width=50, anchor=tk.CENTER)
    tabla.column("Nombre", width=150, anchor=tk.W)
    tabla.column("Descripción", width=250, anchor=tk.W)
    tabla.column("Precio", width=100, anchor=tk.E)

    # Insertar datos en la tabla
    productos = obtener_productos()
    for producto in productos:
        id_producto, nombre, descripcion, precio = producto
        tabla.insert("", "end", values=(id_producto, nombre, descripcion, f"${precio:.2f}"))

    tabla.pack(pady=10)

    # Botón para salir
    boton_cerrar = tk.Button(ventana, text="Cerrar", command=ventana.destroy)
    boton_cerrar.pack(pady=10)

    # Ejecutar la ventana
    ventana.mainloop()

if __name__ == "__main__":
    mostrar_menu()
