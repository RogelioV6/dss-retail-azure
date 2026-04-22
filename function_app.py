import azure.functions as func
import pyodbc
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# CONFIGURACIÓN DE TU BASE DE DATOS
# Reemplaza [tu-nombre] con el nombre de tu servidor de Azure SQL
DB_SERVER = 'dss-retail-srv-[tu-nombre].database.windows.net'
DB_NAME = 'dss-retail-db'
DB_USER = 'sqladmin'
DB_PASS = 'DssRetail2024!'

def generar_recomendacion(stock, ventas):
    if stock > 30 and ventas < 5:
        return "PROMOCIÓN: Stock alto con baja rotación. Se recomienda descuento del 20%."
    elif stock < 10:
        return "REBASTECIMIENTO: Stock crítico. No aplicar promociones."
    else:
        return "ESTADO NORMAL: El producto mantiene un flujo saludable."

@app.route(route="recomendacion")
def dss_retail_api(req: func.HttpRequest) -> func.HttpResponse:
    # Capturamos el ID del producto desde la URL (ej: ?id=1)
    id_prod = req.params.get('id')
    
    if not id_prod:
        return func.HttpResponse("Por favor indica el ID del producto: ?id=X", status_code=400)

    try:
        # Conexión a la base de datos
        conn_str = f"Driver={{ODBC Driver 18 for SQL Server}};Server={DB_SERVER},1433;Database={DB_NAME};Uid={DB_USER};Pwd={DB_PASS};Encrypt=yes;TrustServerCertificate=no;"
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        # Consulta a la Vista que creamos en SQL
        cursor.execute("SELECT nombre, stock_actual, unidades_vendidas FROM Vista_Analisis_DSS WHERE id_producto = ?", id_prod)
        row = cursor.fetchone()
        conn.close()

        if row:
            # Procesamos la lógica DSS
            rec = generar_recomendacion(row[1], row[2])
            data = {
                "producto": row[0],
                "stock_actual": row[1],
                "ventas_totales": row[2],
                "recomendacion_dss": rec
            }
            return func.HttpResponse(json.dumps(data, ensure_ascii=False), mimetype="application/json")
        
        return func.HttpResponse("Producto no encontrado", status_code=404)

    except Exception as e:
        return func.HttpResponse(f"Error de conexión: {str(e)}", status_code=500)
