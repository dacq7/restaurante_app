import sqlite3
import tkinter as tk
from tkinter import messagebox

DB_PATH = './database/restaurante.db'

def agregar_usuario(nombre, contrasena, rol):
    """Agrega un nuevo usuario (mesero o administrador) a la base de datos."""
    if not nombre or not contrasena:
        messagebox.showerror("Error", "El nombre y la contraseña son obligatorios.")
        return

    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO usuarios (usuario, contrasena, rol) 
                VALUES (?, ?, ?)
            """, (nombre, contrasena, rol))
            conn.commit()
            messagebox.showinfo("Éxito", f"Usuario {nombre} agregado exitosamente como {rol}.")
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"No se pudo agregar el usuario: {e}")

def mostrar_ventana_agregar_usuario():
    """Muestra la ventana para agregar un usuario (mesero o administrador)."""
    ventana = tk.Tk()
    ventana.title("Agregar Usuario")
    ventana.geometry("400x300")

    # Crear los campos para el nombre y la contraseña
    tk.Label(ventana, text="Nombre:", font=("Arial", 12)).pack(pady=5)
    entrada_nombre = tk.Entry(ventana, font=("Arial", 12))
    entrada_nombre.pack(pady=5)

    tk.Label(ventana, text="Contraseña:", font=("Arial", 12)).pack(pady=5)
    entrada_contrasena = tk.Entry(ventana, font=("Arial", 12), show="*")
    entrada_contrasena.pack(pady=5)

    # Crear los botones para seleccionar el rol
    tk.Label(ventana, text="Rol:", font=("Arial", 12)).pack(pady=5)
    rol_var = tk.StringVar(value="mesero")
    rol_mesero_rb = tk.Radiobutton(ventana, text="Mesero", variable=rol_var, value="mesero", font=("Arial", 12))
    rol_administrador_rb = tk.Radiobutton(ventana, text="Administrador", variable=rol_var, value="administrador", font=("Arial", 12))
    rol_mesero_rb.pack(pady=5)
    rol_administrador_rb.pack(pady=5)

    # Función que se ejecuta al presionar el botón "Agregar Usuario"
    def agregar():
        nombre = entrada_nombre.get()
        contrasena = entrada_contrasena.get()
        rol = rol_var.get()

        if rol == "administrador":
            rol = "admin"  # Convertir el rol a "admin" para que coincida con la base de datos

        agregar_usuario(nombre, contrasena, rol)  # Llamar a la función para agregar al usuario

        # Limpiar los campos después de agregar el usuario
        entrada_nombre.delete(0, tk.END)
        entrada_contrasena.delete(0, tk.END)

    # Botón para agregar el usuario
    tk.Button(ventana, text="Agregar Usuario", command=agregar, font=("Arial", 12)).pack(pady=10)

    ventana.mainloop()

if __name__ == "__main__":
    mostrar_ventana_agregar_usuario()


