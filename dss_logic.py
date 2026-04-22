def generar_recomendacion(datos_producto):
    stock = datos_producto['stock']
    ventas = datos_producto['ventas']
    
    # Lógica simplificada para el DSS
    if stock > 30 and ventas < 5:
        return "PROMOCIÓN RECOMENDADA: Stock alto con baja rotación. Aplicar 20% de descuento."
    elif stock < 10:
        return "REBASTECIMIENTO: Stock crítico. Priorizar compra y evitar promociones."
    else:
        return "ESTADO NORMAL: El producto fluye correctamente."
