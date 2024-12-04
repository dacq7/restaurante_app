import sqlite3

DB_PATH = './database/restaurante.db'


def cambiar_nombre_tabla():
    """Cambia el nombre de la tabla 'meseros' a 'usuarios'."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        # 1. Crear la nueva tabla temporal llamada 'usuarios' con la misma estructura
        cursor.execute("""
            CREATE TABLE usuarios (
                id INTEGER PRIMARY KEY,
                usuario TEXT NOT NULL,
                contrasena TEXT NOT NULL,
                rol TEXT NOT NULL
            );
        """)

        # 2. Copiar los datos de la tabla 'meseros' a la nueva tabla 'usuarios'
        cursor.execute("""
            INSERT INTO usuarios (id, usuario, contrasena, rol)
            SELECT id, usuario, contrasena, rol FROM meseros;
        """)

        # 3. Eliminar la tabla original 'meseros'
        cursor.execute("DROP TABLE meseros;")

        # 4. Renombrar la tabla 'usuarios' para asegurarse de que sea permanente
        cursor.execute("ALTER TABLE usuarios RENAME TO meseros;")

        conn.commit()

        print("La tabla 'meseros' ha sido renombrada a 'usuarios' y los datos han sido actualizados.")


# Ejecuta la función para cambiar el nombre de la tabla
cambiar_nombre_tabla()

