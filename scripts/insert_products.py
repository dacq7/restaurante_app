import sqlite3

# Ruta de la base de datos
DB_PATH = "./database/restaurante.db"

# Lista de productos para insertar
productos = [
    # Cafés
    ("Café Expreso", "Clásico café corto", 3000),
    ("Café Americano", "Café largo", 3500),
    ("Café con Leche", "Café mezclado con leche caliente", 4000),
    ("Capuchino", "Café con leche espumosa", 4500),

    # Repostería
    ("Croissant", "Panecillo de hojaldre", 5000),
    ("Muffin de Chocolate", "Muffin suave con chips de chocolate", 5500),
    ("Torta de Zanahoria", "Torta esponjosa con zanahoria y nueces", 6000),

    # Hamburguesas
    ("Hamburguesa Clásica", "Hamburguesa con carne de res y queso", 12000),
    ("Hamburguesa BBQ", "Hamburguesa con salsa BBQ y tocineta", 15000),

    # Perros y desgranados
    ("Perro Sencillo", "Salchicha, pan y salsas", 8000),
    ("Desgranado Mixto", "Carne desmechada, maíz y queso", 10000),

    # Carnes a la plancha
    ("Pechuga a la Plancha", "Pechuga de pollo con guarnición", 15000),
    ("Churrasco", "Carne de res con guarnición", 20000),

    # Bebidas
    ("Soda Saborizada", "Soda con sabor a frutas", 3000),
    ("Jugo Natural", "Jugo de frutas naturales", 5000),
    ("Gaseosa", "Refresco carbonatado", 2500),
    ("Cerveza", "Bebida alcohólica", 7000),

    # Cocteles
    ("Margarita", "Clásico cóctel con tequila y limón", 15000),
    ("Mojito", "Cóctel con ron, menta y soda", 13000)
]

def insertar_productos():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.executemany("""
        INSERT INTO menu (nombre, descripcion, precio) VALUES (?, ?, ?)
        """, productos)
        conn.commit()
        print(f"{cursor.rowcount} productos insertados en la tabla 'menu'.")

if __name__ == "__main__":
    insertar_productos()
