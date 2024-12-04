import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from scripts import historial_ordenes  # Importar historial_ordenes correctamente desde scripts
from scripts import agregar_usuario  # Importar agregar_usuario correctamente desde scripts

DB_PATH = "./database/restaurante.db"

def obtener_usuarios():
    """Obtiene la lista de usuarios de la base de datos."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, usuario FROM usuarios")
            return cursor.fetchall()
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"No se pudo obtener la lista de usuarios: {e}")
        return []

def eliminar_usuario(usuario_id):
    """Elimina un usuario de la base de datos dado su ID."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM usuarios WHERE id = ?", (usuario_id,))
            conn.commit()
            messagebox.showinfo("Éxito", "Usuario eliminado exitosamente.")
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"No se pudo eliminar el usuario: {e}")

def mostrar_ventana_admin():
    """Muestra la ventana del administrador."""
    ventana_admin = tk.Tk()
    ventana_admin.title("Administrador")
    ventana_admin.geometry("800x600")

    def mostrar_historial():
        """Accede a la ventana del historial de órdenes."""
        historial_ordenes.mostrar_historial_ordenes(mesero_id=None)  # Llamada correcta para admin

    def mostrar_agregar_usuario():
        """Accede a la ventana de agregar un usuario."""
        agregar_usuario.mostrar_ventana_agregar_usuario()  # Llamada correcta para agregar usuario

    def mostrar_eliminar_usuario():
        """Accede a la ventana para eliminar usuarios."""
        ventana_eliminar_usuario = tk.Toplevel(ventana_admin)
        ventana_eliminar_usuario.title("Eliminar Usuario")
        ventana_eliminar_usuario.geometry("500x400")

        # Mostrar los usuarios en la tabla
        usuarios = obtener_usuarios()

        # Tabla para mostrar los usuarios
        columnas_usuarios = ("ID", "Usuario")
        tabla_usuarios = ttk.Treeview(ventana_eliminar_usuario, columns=columnas_usuarios, show="headings", height=15)
        tabla_usuarios.heading("ID", text="ID")
        tabla_usuarios.heading("Usuario", text="Usuario")
        tabla_usuarios.pack(pady=10)

        # Insertar usuarios en la tabla
        for usuario in usuarios:
            tabla_usuarios.insert("", "end", values=usuario)

        def eliminar_usuario_seleccionado():
            """Elimina el usuario seleccionado."""
            seleccionado = tabla_usuarios.selection()
            if seleccionado:
                usuario_id = tabla_usuarios.item(seleccionado)["values"][0]
                eliminar_usuario(usuario_id)
                tabla_usuarios.delete(seleccionado)  # Eliminar de la tabla después de eliminar de la base de datos
            else:
                messagebox.showerror("Error", "Seleccione un usuario para eliminar.")

        tk.Button(ventana_eliminar_usuario, text="Eliminar Usuario", command=eliminar_usuario_seleccionado, font=("Arial", 12)).pack(pady=10)

    def mostrar_reportes():
        """Genera el reporte gráfico de ventas."""
        # Aquí deberías tener la importación correcta de reportes si es necesario
        # reportes.generar_grafico_ventas()  # Llama a la función de reportes.py para generar el gráfico

    # Botones
    tk.Button(ventana_admin, text="Historial de Órdenes", command=mostrar_historial, font=("Arial", 12)).pack(pady=10)
    tk.Button(ventana_admin, text="Agregar Usuario", command=mostrar_agregar_usuario, font=("Arial", 12)).pack(pady=10)
    tk.Button(ventana_admin, text="Eliminar Usuario", command=mostrar_eliminar_usuario, font=("Arial", 12)).pack(pady=10)
    tk.Button(ventana_admin, text="Generar Reporte de Ventas", command=mostrar_reportes, font=("Arial", 12)).pack(pady=10)

    ventana_admin.mainloop()






