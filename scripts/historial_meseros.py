import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

DB_PATH = './database/restaurante.db'


def obtener_detalles_orden(order_id):
    """Obtiene los detalles de una orden dada su ID e incluye el total."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT menu.nombre, order_details.cantidad, order_details.precio_unitario
                FROM order_details
                JOIN menu ON order_details.producto_id = menu.id
                WHERE order_details.order_id = ?
            """, (order_id,))
            detalles = cursor.fetchall()

            cursor.execute("""
                SELECT SUM(order_details.cantidad * order_details.precio_unitario)
                FROM order_details
                WHERE order_details.order_id = ?
            """, (order_id,))
            total = cursor.fetchone()[0]

            return detalles, total
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"No se pudo obtener los detalles de la orden: {e}")
        return [], 0


def obtener_historial_ordenes_mesero(mesero_id, fecha=None):
    """Consulta el historial de órdenes filtrado por fecha para meseros."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            if fecha:
                cursor.execute("""
                    SELECT orders.id, orders.mesa, orders.fecha, orders.hora, orders.total
                    FROM orders
                    WHERE orders.mesero_id = ? AND orders.fecha = ?
                """, (mesero_id, fecha))
            else:
                cursor.execute("""
                    SELECT orders.id, orders.mesa, orders.fecha, orders.hora, orders.total
                    FROM orders
                    WHERE orders.mesero_id = ?
                """, (mesero_id,))
            return cursor.fetchall()
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"No se pudo obtener el historial de órdenes: {e}")
        return []


def mostrar_historial_ordenes_mesero(mesero_id):
    """Muestra el historial de órdenes en una ventana para meseros."""
    ventana = tk.Tk()
    ventana.title("Historial de Órdenes")
    ventana.geometry("800x600")

    # Filtro por fecha
    tk.Label(ventana, text="Filtrar por fecha (AAAA-MM-DD):", font=("Arial", 12)).pack(pady=5)
    entrada_fecha = tk.Entry(ventana, font=("Arial", 12))
    entrada_fecha.pack(pady=5)

    def actualizar_historial(fecha=None):
        """Actualiza el historial mostrando las órdenes filtradas por fecha."""
        ordenes = obtener_historial_ordenes_mesero(mesero_id, fecha)
        for row in tabla_historial.get_children():
            tabla_historial.delete(row)

        for orden in ordenes:
            tabla_historial.insert("", "end", values=orden)

    def filtrar_por_fecha():
        """Filtra las órdenes según la fecha ingresada."""
        fecha = entrada_fecha.get()
        if fecha:
            actualizar_historial(fecha)
        else:
            messagebox.showerror("Error", "Ingrese una fecha válida.")

    def ver_todas_las_ordenes():
        """Muestra todas las órdenes del mesero sin filtro."""
        entrada_fecha.delete(0, tk.END)
        actualizar_historial()

    def mostrar_detalles_orden():
        """Muestra los detalles de la orden seleccionada."""
        seleccionado = tabla_historial.selection()
        if seleccionado:
            orden_id = tabla_historial.item(seleccionado)["values"][0]
            detalles, total = obtener_detalles_orden(orden_id)
            if not detalles:
                messagebox.showerror("Error", "No se encontraron detalles para esta orden.")
                return

            ventana_detalles = tk.Toplevel(ventana)
            ventana_detalles.title(f"Detalles de la Orden {orden_id}")
            ventana_detalles.geometry("600x400")

            columnas_detalles = ("Producto", "Cantidad", "Precio_unitario")
            tabla_detalles = ttk.Treeview(ventana_detalles, columns=columnas_detalles, show="headings", height=15)
            tabla_detalles.heading("Producto", text="Producto")
            tabla_detalles.heading("Cantidad", text="Cantidad")
            tabla_detalles.heading("Precio_unitario", text="Precio")
            tabla_detalles.pack(pady=10)

            for detalle in detalles:
                tabla_detalles.insert("", "end", values=detalle)

            tk.Label(ventana_detalles, text=f"Total de la Orden: ${total:.2f}", font=("Arial", 14, "bold")).pack(pady=10)

        else:
            messagebox.showerror("Error", "Seleccione una orden para ver los detalles.")

    # Botones de acciones para los meseros
    tk.Button(ventana, text="Filtrar", command=filtrar_por_fecha, font=("Arial", 12)).pack(pady=10)
    tk.Button(ventana, text="Ver Todas las Órdenes", command=ver_todas_las_ordenes, font=("Arial", 12)).pack(pady=10)
    tk.Button(ventana, text="Ver Detalles de la Orden", command=mostrar_detalles_orden, font=("Arial", 12)).pack(pady=10)

    # Tabla para mostrar el historial de órdenes
    columnas = ("ID", "Mesa", "Fecha", "Hora", "Total")
    tabla_historial = ttk.Treeview(ventana, columns=columnas, show="headings", height=15)
    for col in columnas:
        tabla_historial.heading(col, text=col)
    tabla_historial.pack(pady=10)

    # Inicializar la tabla con todas las órdenes
    actualizar_historial()

    ventana.mainloop()
