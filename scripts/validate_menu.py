import sqlite3

# Ruta de la base de datos
DB_PATH = "./database/restaurante.db"

def listar_productos():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM menu")
        productos = cursor.fetchall()

        if productos:
            print(f"Productos en la tabla 'menu':\n")
            for producto in productos:
                id_producto, nombre, descripcion, precio = producto
                print(f"ID: {id_producto}, Nombre: {nombre}, Descripción: {descripcion}, Precio: ${precio:.2f}")
        else:
            print("No hay productos en la tabla 'menu'.")

if __name__ == "__main__":
    listar_productos()
