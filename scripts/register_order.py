import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from scripts import historial_meseros  # Cambié la importación

DB_PATH = './database/restaurante.db'

def obtener_productos():
    """Consulta los productos desde la base de datos."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM menu")
        return cursor.fetchall()

def obtener_historial_ordenes(mesero_id):
    """Consulta el historial de órdenes del mesero en la base de datos."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT orders.id, orders.mesa, orders.fecha, orders.hora, orders.total
            FROM orders
            WHERE orders.mesero_id = ?
        """, (mesero_id,))
        return cursor.fetchall()

def mostrar_historial_ordenes(mesero_id):
    """Muestra el historial de órdenes del mesero en una nueva ventana."""
    ventana_historial = tk.Tk()
    ventana_historial.title("Historial de Órdenes")
    ventana_historial.geometry("800x600")

    # Obtener historial de órdenes del mesero
    ordenes = obtener_historial_ordenes(mesero_id)

    # Crear tabla de historial de órdenes
    columnas = ("ID", "Mesa", "Fecha", "Hora", "Total")
    tabla_historial = ttk.Treeview(ventana_historial, columns=columnas, show="headings", height=15)
    tabla_historial.heading("ID", text="ID")
    tabla_historial.heading("Mesa", text="Mesa")
    tabla_historial.heading("Fecha", text="Fecha")
    tabla_historial.heading("Hora", text="Hora")
    tabla_historial.heading("Total", text="Total")

    # Insertar las órdenes del mesero
    for orden in ordenes:
        tabla_historial.insert("", "end", values=orden)

    tabla_historial.pack(pady=10)

    ventana_historial.mainloop()

def registrar_orden(mesa, carrito, mesero_id):
    """Registra la orden y sus detalles en la base de datos."""
    if not carrito:
        messagebox.showerror("Error", "El carrito está vacío.")
        return

    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()

            # Registrar orden en la tabla `orders`
            cursor.execute("""
            INSERT INTO orders (mesa, fecha, hora, total, mesero_id)
            VALUES (?, DATE('now'), TIME('now'), ?, ?)
            """, (mesa, sum(item['precio'] * item['cantidad'] for item in carrito), mesero_id))  # mesero_id es el que inicia sesión
            order_id = cursor.lastrowid

            # Registrar detalles en la tabla `order_details`
            for item in carrito:
                cursor.execute("""
                INSERT INTO order_details (order_id, producto_id, cantidad, precio_unitario)
                VALUES (?, ?, ?, ?)
                """, (order_id, item['id'], item['cantidad'], item['precio']))

            conn.commit()
            messagebox.showinfo("Éxito", f"Orden registrada exitosamente con ID {order_id}.")
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"No se pudo registrar la orden: {e}")


def registrar_pantalla(mesero_id):
    """Crea la ventana para registrar órdenes para el mesero."""
    # Crear ventana principal
    ventana = tk.Tk()
    ventana.title("Registrar Orden")
    ventana.geometry("800x600")

    # Campo para ingresar la mesa
    tk.Label(ventana, text="Mesa:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
    entrada_mesa = tk.Entry(ventana, font=("Arial", 12))
    entrada_mesa.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    # Tabla de productos
    tk.Label(ventana, text="Productos disponibles:", font=("Arial", 12, "bold")).grid(row=1, column=0, columnspan=2, pady=5)
    productos = obtener_productos()
    columnas = ("ID", "Nombre", "Precio")
    tabla_productos = ttk.Treeview(ventana, columns=columnas, show="headings", height=10)
    tabla_productos.heading("ID", text="ID")
    tabla_productos.heading("Nombre", text="Nombre")
    tabla_productos.heading("Precio", text="Precio")
    for producto in productos:
        tabla_productos.insert("", "end", values=(producto[0], producto[1], f"${producto[3]:.2f}"))
    tabla_productos.grid(row=2, column=0, columnspan=2, pady=10, padx=10)

    # Carrito
    tk.Label(ventana, text="Carrito:", font=("Arial", 12, "bold")).grid(row=3, column=0, columnspan=2, pady=5)
    carrito = []
    carrito_lista = tk.Listbox(ventana, font=("Arial", 12), height=8)
    carrito_lista.grid(row=4, column=0, columnspan=2, pady=5, padx=10)

    def agregar_al_carrito():
        """Agrega un producto seleccionado al carrito."""
        seleccion = tabla_productos.focus()
        if not seleccion:
            messagebox.showerror("Error", "Seleccione un producto.")
            return
        item = tabla_productos.item(seleccion)['values']
        producto = {"id": item[0], "nombre": item[1], "precio": float(item[2].strip('$')), "cantidad": 1}
        carrito.append(producto)
        carrito_lista.insert(tk.END, f"{producto['nombre']} - ${producto['precio']:.2f} x{producto['cantidad']}")

    def eliminar_del_carrito():
        """Elimina el producto seleccionado del carrito."""
        seleccion = carrito_lista.curselection()
        if not seleccion:
            messagebox.showerror("Error", "Seleccione un producto del carrito para eliminar.")
            return
        indice = seleccion[0]
        carrito.pop(indice)
        carrito_lista.delete(indice)

    def registrar():
        """Registra la orden en la base de datos."""
        mesa = entrada_mesa.get()
        if not mesa.isdigit():
            messagebox.showerror("Error", "Ingrese un número de mesa válido.")
            return
        registrar_orden(int(mesa), carrito, mesero_id)  # Pasamos mesero_id a la función de registro
        carrito.clear()
        carrito_lista.delete(0, tk.END)
        entrada_mesa.delete(0, tk.END)

    def ver_historial():
        """Muestra el historial de órdenes del mesero."""
        historial_meseros.mostrar_historial_ordenes_mesero(mesero_id)  # Cambié a la versión para meseros

    # Botones
    botones_frame = tk.Frame(ventana)
    botones_frame.grid(row=5, column=0, columnspan=2, pady=10)

    tk.Button(botones_frame, text="Agregar al carrito", command=agregar_al_carrito, font=("Arial", 12)).grid(row=0, column=0, padx=10)
    tk.Button(botones_frame, text="Eliminar del carrito", command=eliminar_del_carrito, font=("Arial", 12)).grid(row=0, column=1, padx=10)

    # Botones "Registrar Orden" y "Ver mi Historial de Órdenes"
    tk.Button(ventana, text="Registrar Orden", command=registrar, font=("Arial", 12)).grid(row=6, column=0, pady=10)
    tk.Button(ventana, text="Ver mi Historial de Órdenes", command=ver_historial, font=("Arial", 12)).grid(row=6, column=1, pady=10)

    ventana.mainloop()









