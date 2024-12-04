import sqlite3
import tkinter as tk
from tkinter import messagebox

DB_PATH = './database/restaurante.db'

def eliminar_mesero(nombre):
    """Elimina un mesero de la base de datos."""
    if not nombre:
        messagebox.showerror("Error", "Debe ingresar un nombre para eliminar.")
        return

    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM meseros WHERE nombre = ?", (nombre,))
            conn.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo("Éxito", f"Mesero {nombre} eliminado exitosamente.")
            else:
                messagebox.showerror("Error", f"No se encontró al mesero {nombre}.")
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"No se pudo eliminar el mesero: {e}")

def mostrar_ventana_eliminar_mesero():
    """Muestra la ventana para eliminar un mesero."""
    ventana = tk.Tk()
    ventana.title("Eliminar Mesero")
    ventana.geometry("400x300")

    tk.Label(ventana, text="Nombre del Mesero a eliminar:", font=("Arial", 12)).pack(pady=5)
    entrada_nombre = tk.Entry(ventana, font=("Arial", 12))
    entrada_nombre.pack(pady=5)

    def eliminar():
        nombre = entrada_nombre.get()
        eliminar_mesero(nombre)
        entrada_nombre.delete(0, tk.END)

    tk.Button(ventana, text="Eliminar Mesero", command=eliminar, font=("Arial", 12)).pack(pady=10)

    ventana.mainloop()

if __name__ == "__main__":
    mostrar_ventana_eliminar_mesero()
