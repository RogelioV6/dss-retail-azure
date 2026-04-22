from flask import Flask, jsonify
import pyodbc
from dss_logic import generar_recomendacion
import os

app = Flask(__name__)

# Datos de conexión (Asegúrate que coincidan con tu SQL Azure)
DB_SERVER = 'dss-retail-srv-[tu-nombre].database.windows.net'
DB_NAME = 'dss-retail-db'
DB_USER = 'sqladmin'
DB_PASS = 'DssRetail2024!'

def get_db_connection():
    # El Driver 18 es el estándar en Azure App Service
    conn_str = f"Driver={{ODBC Driver 18 for SQL Server}};Server={DB_SERVER},1433;Database={DB_NAME};Uid={DB_USER};Pwd={DB_PASS};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
    return pyodbc.connect(conn_str)

@app.route('/')
def home():
    return "API DSS Funcionando. Prueba /api/recomendacion/1"

@app.route('/api/recomendacion/<int:id_prod>', methods=['GET'])
def recomendacion(id_prod):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Consultamos la vista que ya probamos en el Query Editor
        cursor.execute("SELECT nombre, stock_actual, unidades_vendidas FROM Vista_Analisis_DSS WHERE id_producto = ?", id_prod)
        row = cursor.fetchone()
        conn.close()

        if row:
            p_data = {"stock": row[1], "ventas": row[2]}
            res = generar_recomendacion(p_data)
            return jsonify({
                "producto": row[0],
                "stock": row[1],
                "ventas_acumuladas": row[2],
                "dss_sugerencia": res
            })
        return jsonify({"error": "Producto no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()
