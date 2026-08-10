from interno import funciones

# Umbral por defecto para considerar que un producto tiene poco stock
UMBRAL_STOCK_BAJO = 5

def agregar_producto(nombre, precio, stock, categoria_id):
    try:
        cursor = funciones.conexion.cursor()
        cursor.execute("INSERT INTO productos (nombre, precio, stock, categoria_id) VALUES (%s, %s, %s, %s)", (nombre, precio, stock, categoria_id))
        cursor.execute("INSERT INTO historial (movimiento) VALUES (%s)", (f"Se agregó el producto '{nombre}' con stock inicial de {stock}",))
        funciones.conexion.commit()
        cursor.close()
        
        if stock <= UMBRAL_STOCK_BAJO:
            print(f"⚠️ ¡ATENCIÓN! El producto '{nombre}' se agregó con stock bajo ({stock} unidades).")
        return True
    except Exception:
        return False

def editar_producto(id_prod, nuevo_nombre, nuevo_precio, nuevo_categoria_id):
    try:
        cursor = funciones.conexion.cursor()
        cursor.execute("UPDATE productos SET nombre = %s, precio = %s, categoria_id = %s WHERE id = %s", (nuevo_nombre, nuevo_precio, nuevo_categoria_id, id_prod))
        cursor.execute("INSERT INTO historial (movimiento) VALUES (%s)", (f"Se actualizó el producto ID {id_prod} a '{nuevo_nombre}'",))
        funciones.conexion.commit()
        cursor.close()
        return True
    except Exception:
        return False

def eliminar_producto(id_prod):
    try:
        cursor = funciones.conexion.cursor()
        cursor.execute("DELETE FROM productos WHERE id = %s", (id_prod,))
        cursor.execute("INSERT INTO historial (movimiento) VALUES (%s)", (f"Se eliminó el producto ID {id_prod}",))
        funciones.conexion.commit()
        cursor.close()
        return True
    except Exception:
        return False

def reabastecer_stock(id_prod, cantidad):
    try:
        cursor = funciones.conexion.cursor()
        cursor.execute("UPDATE productos SET stock = stock + %s WHERE id = %s", (cantidad, id_prod))
        cursor.execute("INSERT INTO historial (movimiento) VALUES (%s)", (f"Se reabasteció el producto ID {id_prod} con +{cantidad} unidades",))
        funciones.conexion.commit()
        cursor.close()
        return True
    except Exception:
        return False

def vender_producto(id_prod, cantidad):
    try:
        cursor = funciones.conexion.cursor()
        
        # Obtener nombre y stock actual para validar si se puede vender
        cursor.execute("SELECT nombre, stock FROM productos WHERE id = %s", (id_prod,))
        producto = cursor.fetchone()
        
        if not producto:
            cursor.close()
            return False, "El producto no existe."
            
        nombre_prod, stock_actual = producto[0], producto[1]
        
        if stock_actual < cantidad:
            cursor.close()
            return False, f"Stock insuficiente. Solo quedan {stock_actual} unidades disponibles."
            
        nuevo_stock = stock_actual - cantidad
        cursor.execute("UPDATE productos SET stock = %s WHERE id = %s", (nuevo_stock, id_prod))
        cursor.execute("INSERT INTO historial (movimiento) VALUES (%s)", (f"Se vendió el producto '{nombre_prod}' (ID: {id_prod}) x{cantidad} unidad/es",))
        funciones.conexion.commit()
        cursor.close()
        
        # Alerta en consola si el stock entra en nivel crítico
        if nuevo_stock <= UMBRAL_STOCK_BAJO:
            print(f"⚠️ ¡ALERTA DE STOCK BAJO! Quedan solo {nuevo_stock} unidad/es) de '{nombre_prod}'.")
            
        return True, "Venta realizada con éxito."
    except Exception:
        return False, "Error al procesar la venta."

def consultar_stock_bajo(limite=UMBRAL_STOCK_BAJO):
    try:
        cursor = funciones.conexion.cursor()
        cursor.execute("SELECT p.id, p.nombre, p.stock, c.nombre FROM productos p INNER JOIN categorias c ON p.categoria_id = c.id WHERE p.stock <= %s", (limite,))
        resultados = cursor.fetchall()
        cursor.close()
        return resultados
    except Exception:
        return []

def consultar():
    try:
        cursor = funciones.conexion.cursor()
        cursor.execute("SELECT p.id, p.nombre, p.precio, p.stock, c.nombre FROM productos p INNER JOIN categorias c ON p.categoria_id = c.id")
        resultados = cursor.fetchall()
        cursor.close()
        return resultados
    except Exception:
        return []

def buscar(id_prod):
    try:
        cursor = funciones.conexion.cursor()
        cursor.execute("SELECT p.id, p.nombre, p.precio, p.stock, c.nombre FROM productos p INNER JOIN categorias c ON p.categoria_id = c.id WHERE p.id = %s", (id_prod,))
        resultados = cursor.fetchall()
        cursor.close()
        return resultados
    except Exception:
        return []
    
def vaciar_historial_db(conexion):

    #Elimina todos los registros de la tabla 'historial'
    try:
        cursor = conexion.cursor()
        # Consultar total de registros previo al formateo
        cursor.execute("SELECT COUNT(*) FROM historial")
        total_registros = cursor.fetchone()[0]

        if total_registros == 0:
            cursor.close()
            return True, 0
        # Limpieza completa y reinicio de ID
        cursor.execute("TRUNCATE TABLE historial")
        conexion.commit()
        cursor.close()
        return True, total_registros
    except Exception:
        conexion.rollback()
        return False, 0
def vaciar_productos_db(conexion):
    # Elimina todos los registros de la tabla 'productos'
    try:
        cursor = conexion.cursor()
        # Consultar total de registros previo al formateo
        cursor.execute("SELECT COUNT(*) FROM productos")
        total_registros = cursor.fetchone()[0]

        if total_registros == 0:
            cursor.close()
            return True, 0

        # Limpieza completa y reinicio de ID
        cursor.execute("TRUNCATE TABLE productos")
        conexion.commit()
        cursor.close()
        return True, total_registros
    except Exception:
        conexion.rollback()
        return False, 0
    