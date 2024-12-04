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


def obtener_historial_ordenes(mesero_id=None, fecha=None, mesero_nombre=None):
    """Consulta el historial de órdenes filtrado por fecha y/o mesero (según el rol)."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            if mesero_id:  # Si es mesero, filtrar por mesero_id y fecha
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
            else:  # Si es administrador, permitir filtrar por fecha y mesero_nombre
                query = """
                    SELECT orders.id, orders.mesa, orders.fecha, orders.hora, orders.total, usuarios.usuario
                    FROM orders
                    JOIN usuarios ON orders.mesero_id = usuarios.id
                """
                params = []

                if fecha:
                    query += " WHERE orders.fecha = ?"
                    params.append(fecha)

                if mesero_nombre:
                    if params:
                        query += " AND usuarios.usuario = ?"
                    else:
                        query += " WHERE usuarios.usuario = ?"
                    params.append(mesero_nombre)

                cursor.execute(query, tuple(params))

            return cursor.fetchall()
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"No se pudo obtener el historial de órdenes: {e}")
        return []


def mostrar_historial_ordenes(mesero_id=None):
    """Muestra el historial de órdenes en una ventana."""
    ventana = tk.Tk()
    ventana.title("Historial de Órdenes")
    ventana.geometry("800x600")

    # Filtros de búsqueda
    tk.Label(ventana, text="Filtrar por fecha (AAAA-MM-DD):", font=("Arial", 12)).pack(pady=5)
    entrada_fecha = tk.Entry(ventana, font=("Arial", 12))
    entrada_fecha.pack(pady=5)

    if mesero_id is None:  # Administrador
        tk.Label(ventana, text="Filtrar por nombre de mesero:", font=("Arial", 12)).pack(pady=5)
        entrada_mesero = tk.Entry(ventana, font=("Arial", 12))
        entrada_mesero.pack(pady=5)
    else:
        entrada_mesero = None  # Mesero no necesita este campo

    def actualizar_historial(fecha=None, mesero_nombre=None):
        """Actualiza el historial mostrando las órdenes filtradas por los criterios dados."""
        ordenes = obtener_historial_ordenes(mesero_id, fecha, mesero_nombre)
        for row in tabla_historial.get_children():
            tabla_historial.delete(row)

        for orden in ordenes:
            tabla_historial.insert("", "end", values=orden)

    def filtrar_por_criterios():
        """Filtra las órdenes según los criterios proporcionados."""
        fecha = entrada_fecha.get()
        mesero_nombre = entrada_mesero.get() if entrada_mesero else None
        if fecha or mesero_nombre:
            actualizar_historial(fecha, mesero_nombre)
        else:
            messagebox.showerror("Error", "Ingrese al menos un criterio de filtro.")

    def ver_todas_las_ordenes():
        """Muestra todas las órdenes sin filtro."""
        entrada_fecha.delete(0, tk.END)
        if entrada_mesero:
            entrada_mesero.delete(0, tk.END)
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

    tk.Button(ventana, text="Filtrar", command=filtrar_por_criterios, font=("Arial", 12)).pack(pady=10)
    tk.Button(ventana, text="Ver Todas las Órdenes", command=ver_todas_las_ordenes, font=("Arial", 12)).pack(pady=10)
    tk.Button(ventana, text="Ver Detalles de la Orden", command=mostrar_detalles_orden, font=("Arial", 12)).pack(pady=10)

    columnas = ("ID", "Mesa", "Fecha", "Hora", "Total")
    if mesero_id is None:  # Administrador
        columnas = ("ID", "Mesa", "Fecha", "Hora", "Total", "Mesero")

    tabla_historial = ttk.Treeview(ventana, columns=columnas, show="headings", height=15)
    for col in columnas:
        tabla_historial.heading(col, text=col)
    tabla_historial.pack(pady=10)

    actualizar_historial()

    ventana.mainloop()





