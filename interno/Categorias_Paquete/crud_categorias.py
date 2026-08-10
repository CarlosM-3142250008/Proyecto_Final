from interno import funciones

def insertar(nombre):
    try:
        cursor = funciones.conexion.cursor()
        cursor.execute("INSERT INTO categorias (nombre) VALUES (%s)", (nombre,))
        cursor.execute("INSERT INTO historial (movimiento) VALUES (%s)", (f"Se agregó la categoría '{nombre}'",))
        funciones.conexion.commit()
        cursor.close()
        return True
    except Exception:
        return False

def editar(id_cat, nuevo_nombre):
    try:
        cursor = funciones.conexion.cursor()
        cursor.execute("UPDATE categorias SET nombre = %s WHERE id = %s", (nuevo_nombre, id_cat))
        cursor.execute("INSERT INTO historial (movimiento) VALUES (%s)", (f"Se actualizó la categoría ID {id_cat} a '{nuevo_nombre}'",))
        funciones.conexion.commit()
        cursor.close()
        return True
    except Exception:
        return False

def eliminar(id_cat):
    try:
        cursor = funciones.conexion.cursor()
        cursor.execute("DELETE FROM categorias WHERE id = %s", (id_cat,))
        cursor.execute("INSERT INTO historial (movimiento) VALUES (%s)", (f"Se eliminó la categoría ID {id_cat}",))
        funciones.conexion.commit()
        cursor.close()
        return True
    except Exception:
        return False

def consultar():
    try:
        cursor = funciones.conexion.cursor()
        cursor.execute("SELECT id, nombre FROM categorias")
        resultados = cursor.fetchall()
        cursor.close()
        return resultados
    except Exception:
        return []

def obtener_productos_por_categoria(id_cat):
    try:
        cursor = funciones.conexion.cursor()
        cursor.execute("SELECT id, nombre FROM productos WHERE categoria_id = %s", (id_cat,))
        resultados = cursor.fetchall()
        cursor.close()
        return resultados
    except Exception:
        return []