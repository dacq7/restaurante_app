import sqlite3
import tkinter as tk
from tkinter import messagebox
from .register_order import registrar_pantalla # Ventana de mesero
from .admin import mostrar_ventana_admin # Ventana de administrador

DB_PATH = './database/restaurante.db'


def verificar_usuario(usuario, contrasena):
    """Verifica el usuario y la contraseña en la base de datos y devuelve el id y rol"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, rol FROM usuarios WHERE usuario = ? AND contrasena = ?
        """, (usuario, contrasena))
        usuario_data = cursor.fetchone()
        if usuario_data:
            return usuario_data  # Devuelve el id y rol
        else:
            return None  # Usuario no encontrado


def iniciar_sesion():
    """Inicia sesión dependiendo del rol del usuario"""
    usuario = entrada_usuario.get()
    contrasena = entrada_contrasena.get()

    if not usuario or not contrasena:
        messagebox.showerror("Error", "Por favor, ingrese usuario y contraseña.")
        return

    # Verificar usuario y obtener datos (id y rol)
    usuario_data = verificar_usuario(usuario, contrasena)

    if usuario_data:
        usuario_id, rol = usuario_data
        ventana.destroy()  # Cerrar la ventana de login después de iniciar sesión

        if rol == "admin":  # Si es administrador
            mostrar_ventana_admin()  # Abrir ventana de administrador
        else:
            registrar_pantalla(usuario_id)  # Si es mesero, abrir ventana de mesero
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos.")


# Ventana de login
ventana = tk.Tk()
ventana.title("Iniciar Sesión")
ventana.geometry("400x300")

# Etiqueta y campo para usuario
tk.Label(ventana, text="Usuario", font=("Arial", 12)).pack(pady=10)
entrada_usuario = tk.Entry(ventana, font=("Arial", 12))
entrada_usuario.pack(pady=5)

# Etiqueta y campo para contraseña
tk.Label(ventana, text="Contraseña", font=("Arial", 12)).pack(pady=10)
entrada_contrasena = tk.Entry(ventana, font=("Arial", 12), show="*")
entrada_contrasena.pack(pady=5)

# Botón para iniciar sesión
tk.Button(ventana, text="Iniciar Sesión", command=iniciar_sesion, font=("Arial", 12)).pack(pady=10)

ventana.mainloop()

