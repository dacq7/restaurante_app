import sqlite3

DB_PATH = './database/restaurante.db'

def crear_tabla_usuarios():
    """Crea la tabla 'usuarios' con los campos necesarios."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        # Crear la tabla usuarios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT NOT NULL UNIQUE,
                contrasena TEXT NOT NULL,
                rol TEXT NOT NULL CHECK (rol IN ('mesero', 'admin'))
            );
        """)

        conn.commit()
        print("Tabla 'usuarios' creada exitosamente.")

# Ejecuta la función para crear la tabla
crear_tabla_usuarios()
