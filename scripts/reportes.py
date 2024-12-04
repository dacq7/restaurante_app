import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

DB_PATH = './database/restaurante.db'


def obtener_ventas_por_fecha(fecha_inicio, fecha_fin):
    """Obtiene las ventas totales entre las fechas dadas."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT SUM(total) 
                FROM orders 
                WHERE fecha BETWEEN ? AND ?
            """, (fecha_inicio, fecha_fin))
            resultado = cursor.fetchone()
            return resultado[0] if resultado[0] else 0
    except sqlite3.Error as e:
        print(f"Error al obtener ventas por fecha: {e}")
        return 0


def ventas_diarias():
    """Genera el reporte de ventas diarias."""
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    ventas = obtener_ventas_por_fecha(fecha_actual, fecha_actual)
    return ventas


def ventas_semanales():
    """Genera el reporte de ventas semanales."""
    fecha_actual = datetime.now()
    fecha_inicio = (fecha_actual - timedelta(days=fecha_actual.weekday())).strftime(
        "%Y-%m-%d")  # Primer día de la semana
    fecha_fin = fecha_actual.strftime("%Y-%m-%d")  # Último día de la semana
    ventas = obtener_ventas_por_fecha(fecha_inicio, fecha_fin)
    return ventas


def ventas_mensuales():
    """Genera el reporte de ventas mensuales."""
    fecha_actual = datetime.now()
    fecha_inicio = datetime(fecha_actual.year, fecha_actual.month, 1).strftime("%Y-%m-%d")
    fecha_fin = fecha_actual.strftime("%Y-%m-%d")
    ventas = obtener_ventas_por_fecha(fecha_inicio, fecha_fin)
    return ventas


def generar_grafico_ventas():
    """Genera un gráfico de barras con las ventas diarias, semanales y mensuales."""
    ventas = [
        ventas_diarias(),
        ventas_semanales(),
        ventas_mensuales()
    ]
    labels = ['Ventas Diarias', 'Ventas Semanales', 'Ventas Mensuales']

    plt.figure(figsize=(8, 6))
    plt.bar(labels, ventas, color=['blue', 'green', 'red'])
    plt.title('Reporte de Ventas')
    plt.xlabel('Periodo')
    plt.ylabel('Ventas Totales ($)')
    plt.show()
