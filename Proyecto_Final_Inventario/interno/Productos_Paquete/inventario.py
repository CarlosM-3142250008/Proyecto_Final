import json
import re
from datetime import datetime
from interno import funciones
from interno.Categorias_Paquete import crud_categorias
from interno.Productos_Paquete import crud

# --- CONSTANTES DE COLOR ---
AZUL = "\033[1;34m"
VERDE = "\033[1;32m"
CYAN = "\033[1;36m"
AMARILLO = "\033[1;33m"
ROJO = "\033[1;31m"
RESET = "\033[0m"

# --- MENÚS Y FUNCIONES PRINCIPALES ---
def MenuPrincipal():
    print(f"{AZUL}=============================================================={RESET}")
    print(f"{CYAN}\t\t 📦 SISTEMA DE GESTIÓN E INVENTARIO{RESET}")
    print(f"{AZUL}=============================================================={RESET}\n")
    print(f"\t{VERDE}1.{RESET} 📂 Categorías")
    print(f"\t{VERDE}2.{RESET} 🏷️  Productos")
    print(f"\t{VERDE}3.{RESET} 💲 Ventas y Stock")
    print(f"\t{VERDE}4.{RESET} 📜 Ver Historial")
    print(f"\t{ROJO}5.{RESET} 🚪 Salir\n")
    print(f"{AZUL}--------------------------------------------------------------{RESET}")
    return input(f"{AMARILLO}Seleccione una opcion: {RESET}").strip()

def pedirConfirmacion(mensaje, funcion_exito, mensaje_cancelacion):
    resp = input(f"\n{AMARILLO}{mensaje}{RESET} ({VERDE}s{RESET}/{ROJO}n{RESET}): ").strip().lower()
    if resp == 's':
        funcion_exito()
    elif resp == 'n':
        print(f"\n{ROJO}✖ Operación cancelada:{RESET} {mensaje_cancelacion}")
        funciones.espereTecla()
    else:
        print(f"\n{ROJO}⚠️  Opción no válida.{RESET} Ingrese únicamente [{VERDE}s{RESET}] para Sí o [{ROJO}n{RESET}] para No.")
        pedirConfirmacion(mensaje, funcion_exito, mensaje_cancelacion)

def mostrarExito(mensaje_detalle=""):
    print(f"\n{VERDE}✓ Acción realizada con éxito.{RESET}")
    if mensaje_detalle:
        print(f"{CYAN}➜ {mensaje_detalle}{RESET}")
    funciones.espereTecla()

def mostrarTablaProductos(productos):
    print(f"{CYAN}{'ID':<5}|{'NOMBRE':<20}|{'PRECIO':<10}|{'STOCK':<10}|{'CATEGORIA':<10}{RESET}")
    print(f"{AZUL}" + "-" * 60 + f"{RESET}")
    for i, nombre, precio, stock, cat_nombre in productos:
        print(f"{VERDE}{i:<5}{RESET}|{nombre:<20}|${precio:<9.2f}|{stock:<10}|{cat_nombre:<10}")

def consultarInventario():
    try:
        funciones.borrarPantalla()
        print(f"{CYAN}\n\t...::: LISTA DE PRODUCTOS :::...\n{RESET}")
        productos = crud.consultar()
        if productos:
            mostrarTablaProductos(productos)
        else:
            print(f"\t{AMARILLO}⚠️ No hay productos registrados en la base de datos.{RESET}")
    except Exception as e:
        print(f"Error al mostrar inventario: {e}")
    funciones.espereTecla()

def buscarProducto():
    try:
        funciones.borrarPantalla()
        print(f"{CYAN}\n\t...:::: BUSCAR PRODUCTOS ::::...\n{RESET}")
        
        id_prod = funciones.pedirTextoValidado(
            "Escribir el ID del producto: ",
            funciones.validarEnteroPositivo,
            "El ID debe ser un número entero positivo válido."
        )

        prod = crud.buscar(id_prod)
        if prod:
            mostrarTablaProductos(prod)
        else:
            print(f"\t{AMARILLO}⚠️ No se encontró el producto solicitado.{RESET}")
    except Exception as e:
        print(f"Error al buscar producto: {e}")
    funciones.espereTecla()

def agregarProducto():
    try:
        funciones.borrarPantalla()
        print(f"{CYAN}\n\t...::: AGREGAR PRODUCTO :::...\n{RESET}")

        nombre = funciones.pedirTextoValidado(
            "Nombre (solo letras y espacios): ",
            funciones.validarNombre,
            "El nombre solo debe contener letras y espacios (2 a 40 caracteres)."
        )
        precio_txt = funciones.pedirTextoValidado(
            "Precio (ej. 12.50): ",
            funciones.validarPrecio,
            "El precio debe ser un número válido, con máximo 2 decimales."
        )
        stock_txt = funciones.pedirTextoValidado(
            "Stock inicial (entero positivo): ",
            funciones.validarEnteroPositivo,
            "El stock debe ser un número entero positivo."
        )
        precio = float(precio_txt)
        stock = int(stock_txt)

        cats = crud_categorias.consultar()
        if not cats:
            print(f"\n\t{AMARILLO}⚠️ Primero debes registrar al menos una categoría.{RESET}")
            funciones.espereTecla()
            return

        print(f"\n{AZUL}--- Categorías Disponibles ---{RESET}")
        ids_validos = []
        for c in cats:
            print(f"{VERDE}ID: {c[0]:<3}{RESET} | Categoría: {c[1]}")
            ids_validos.append(str(c[0]))

        cat_id_input = funciones.pedirTextoValidado(
            "\nID de la Categoría seleccionada: ",
            funciones.validarEnteroPositivo,
            "El ID de categoría debe ser un número entero positivo."
        )

        if cat_id_input not in ids_validos:
            print(f"\t{ROJO}⚠️ El ID ingresado no pertenece a ninguna categoría disponible.{RESET}")
            funciones.espereTecla()
            return

        cat_id = int(cat_id_input)

        print(f"\n{AZUL}--- RESUMEN DE CAMBIOS ---{RESET}")
        print(f"Acción: Registro de nuevo producto")
        print(f"Nombre: {nombre}")
        print(f"Precio: ${precio:.2f}")
        print(f"Stock inicial: {stock}")
        print(f"ID Categoría: {cat_id}")

        def ejecutar_agregar():
            if crud.agregar_producto(nombre, precio, stock, cat_id):
                mostrarExito(f"Se agregó correctamente el producto '{nombre}'.")
            else:
                funciones.accionNoExitosa()

        pedirConfirmacion(
            "¿Estás seguro de agregar este producto?",
            ejecutar_agregar,
            f"El usuario canceló la inserción del producto '{nombre}'."
        )
    except ValueError:
        funciones.opcionInvalida()
    except Exception as e:
        print(f"Error inesperado: {e}")
        funciones.espereTecla()

def editarProducto():
    try:
        funciones.borrarPantalla()
        print(f"{CYAN}\n\t...::: EDITAR PRODUCTO :::...\n{RESET}")
        prods = crud.consultar()
        if not prods:
            print(f"\t{AMARILLO}⚠️ No hay productos disponibles para editar.{RESET}")
            funciones.espereTecla()
            return

        mostrarTablaProductos(prods)
        
        id_prod = funciones.pedirTextoValidado(
            "\nID del producto a editar: ",
            funciones.validarEnteroPositivo,
            "El ID debe ser un número entero positivo válido."
        )

        prod = crud.buscar(id_prod)
        if not prod:
            print(f"\t{AMARILLO}⚠️ No se encontró el producto especificado.{RESET}")
            funciones.espereTecla()
            return

        nombre = funciones.pedirTextoValidado(
            "Nuevo nombre (solo letras y espacios): ",
            funciones.validarNombre,
            "El nombre solo debe contener letras y espacios (2 a 40 caracteres)."
        )
        
        precio_txt = funciones.pedirTextoValidado(
            "Nuevo precio (ej. 12.50): ",
            funciones.validarPrecio,
            "El precio debe ser un número válido, con máximo 2 decimales."
        )
        precio = float(precio_txt)

        cats = crud_categorias.consultar()
        if not cats:
            print(f"\n\t{AMARILLO}⚠️ No hay categorías registradas.{RESET}")
            funciones.espereTecla()
            return

        print(f"\n{AZUL}--- Categorías Disponibles ---{RESET}")
        ids_validos = []
        for c in cats:
            print(f"{VERDE}ID: {c[0]:<3}{RESET} | Categoría: {c[1]}")
            ids_validos.append(str(c[0]))

        cat_id_input = funciones.pedirTextoValidado(
            "\nSeleccione el nuevo ID de Categoría: ",
            funciones.validarEnteroPositivo,
            "El ID de categoría debe ser un entero positivo."
        )

        if cat_id_input not in ids_validos:
            print(f"\t{ROJO}⚠️ El ID ingresado no pertenece a ninguna categoría disponible.{RESET}")
            funciones.espereTecla()
            return

        cat_id = int(cat_id_input)

        print(f"\n{AZUL}--- RESUMEN DE CAMBIOS ---{RESET}")
        print(f"Acción: Modificación de producto ID {id_prod}")
        print(f"Nuevo Nombre: {nombre}")
        print(f"Nuevo Precio: ${precio:.2f}")
        print(f"Nuevo ID Categoría: {cat_id}")

        def ejecutar_editar():
            if crud.editar_producto(id_prod, nombre, precio, cat_id):
                mostrarExito(f"Se modificó correctamente el producto '{nombre}' (ID: {id_prod}).")
            else:
                funciones.accionNoExitosa()

        pedirConfirmacion(
            "¿Estás seguro de guardar estos cambios?",
            ejecutar_editar,
            f"Se descartaron los cambios para el producto ID {id_prod}."
        )
    except ValueError:
        funciones.opcionInvalida()
    except Exception as e:
        print(f"Error inesperado: {e}")
        funciones.espereTecla()

def eliminarProducto():
    try:
        funciones.borrarPantalla()
        print(f"{CYAN}\n\t...::: ELIMINAR PRODUCTO :::...\n{RESET}")
        prods = crud.consultar()
        if not prods:
            print(f"\t{AMARILLO}⚠️ No hay productos disponibles para eliminar.{RESET}")
            funciones.espereTecla()
            return

        mostrarTablaProductos(prods)
        
        id_prod = funciones.pedirTextoValidado(
            "\nID del producto a eliminar: ",
            funciones.validarEnteroPositivo,
            "El ID debe ser un número entero positivo válido."
        )

        prod = crud.buscar(id_prod)
        if prod:
            nombre_p = prod[0][1]
            print(f"\n{AZUL}--- RESUMEN DE CAMBIOS ---{RESET}")
            print(f"Acción: Eliminar producto definitivamente")
            print(f"Producto: {nombre_p} (ID: {id_prod})")

            def ejecutar_eliminar():
                if crud.eliminar_producto(id_prod):
                    mostrarExito(f"Se eliminó correctamente el producto '{nombre_p}' (ID: {id_prod}).")
                else:
                    funciones.accionNoExitosa()

            pedirConfirmacion(
                "¿Estás seguro de eliminar este producto?",
                ejecutar_eliminar,
                f"No se eliminó el producto ID {id_prod}."
            )
        else:
            print(f"\t{AMARILLO}⚠️ No se encontró el producto especificado.{RESET}")
            funciones.espereTecla()
    except Exception as e:
        print(f"Error inesperado: {e}")
        funciones.espereTecla()

def registrarVenta():
    try:
        funciones.borrarPantalla()
        print(f"{CYAN}\n\t...::: REGISTRAR VENTA :::...\n{RESET}")
        prods = crud.consultar()
        if not prods:
            print(f"\t{AMARILLO}⚠️ No hay productos disponibles.{RESET}")
            funciones.espereTecla()
            return

        mostrarTablaProductos(prods)
        
        id_p = funciones.pedirTextoValidado(
            "\nID del producto vendido: ",
            funciones.validarEnteroPositivo,
            "El ID debe ser un número entero positivo válido."
        )

        prod = crud.buscar(id_p)
        if prod:
            nombre_p = prod[0][1]
            stock_actual = prod[0][3]

            cant_txt = funciones.pedirTextoValidado(
                "Cantidad vendida: ",
                funciones.validarEnteroPositivo,
                "La cantidad debe ser un número entero positivo mayor a 0."
            )
            cant = int(cant_txt)

            if cant <= stock_actual:
                print(f"\n{AZUL}--- RESUMEN DE CAMBIOS ---{RESET}")
                print(f"Acción: Venta de producto")
                print(f"Producto: {nombre_p}")
                print(f"Stock actual: {stock_actual} -> Nuevo Stock: {stock_actual - cant}")

                def ejecutar_venta():
                    exito, _ = crud.vender_producto(id_p, cant)
                    if exito:
                        mostrarExito(f"Se registraron {cant} unidad(es) vendidas del producto '{nombre_p}'.")
                    else:
                        funciones.accionNoExitosa()

                pedirConfirmacion(
                    "¿Estás seguro de realizar esta venta?",
                    ejecutar_venta,
                    f"Se anuló el registro de venta para el producto '{nombre_p}'."
                )
            else:
                print(f"\t{AMARILLO}⚠️ Stock insuficiente para realizar la venta.{RESET}")
                funciones.espereTecla()
        else:
            print(f"\t{AMARILLO}⚠️ No se encontró el producto con el ID especificado.{RESET}")
            funciones.espereTecla()
    except ValueError:
        funciones.opcionInvalida()
    except Exception as e:
        print(f"Error inesperado: {e}")
        funciones.espereTecla()

def reabastecerMercancia():
    try:
        funciones.borrarPantalla()
        print(f"{CYAN}\n\t...::: REABASTECER MERCANCÍA :::...\n{RESET}")
        prods = crud.consultar()
        if not prods:
            print(f"\t{AMARILLO}⚠️ No hay productos disponibles.{RESET}")
            funciones.espereTecla()
            return

        mostrarTablaProductos(prods)
        
        id_p = funciones.pedirTextoValidado(
            "\nID del producto a reabastecer: ",
            funciones.validarEnteroPositivo,
            "El ID debe ser un número entero positivo válido."
        )

        prod = crud.buscar(id_p)
        if prod:
            nombre_p = prod[0][1]
            stock_actual = prod[0][3]

            cant_txt = funciones.pedirTextoValidado(
                "Cantidad a añadir: ",
                funciones.validarEnteroPositivo,
                "La cantidad debe ser un número entero positivo mayor a 0."
            )
            cant = int(cant_txt)

            print(f"\n{AZUL}--- RESUMEN DE CAMBIOS ---{RESET}")
            print(f"Acción: Reabastecimiento de stock")
            print(f"Producto: {nombre_p}")
            print(f"Stock actual: {stock_actual} -> Nuevo Stock: {stock_actual + cant}")

            def ejecutar_reabastecimiento():
                if crud.reabastecer_stock(id_p, cant):
                    mostrarExito(f"Se agregaron {cant} unidad(es) al stock del producto '{nombre_p}'.")
                else:
                    funciones.accionNoExitosa()

            pedirConfirmacion(
                "¿Estás seguro de realizar este reabastecimiento?",
                ejecutar_reabastecimiento,
                f"Se descartó el reabastecimiento para '{nombre_p}'."
            )
        else:
            print(f"\t{AMARILLO}⚠️ No se encontró el producto especificado.{RESET}")
            funciones.espereTecla()
    except ValueError:
        funciones.opcionInvalida()
    except Exception as e:
        print(f"Error inesperado: {e}")
        funciones.espereTecla()

def vaciarProductos():
    funciones.borrarPantalla()
    print(f"{CYAN}\n\t...::: VACIAR TODOS LOS PRODUCTOS :::...\n{RESET}")
    try:
        productos = crud.consultar()
        if not productos:
            print(f"\t{AMARILLO}⚠️ No hay productos registrados para vaciar.{RESET}")
            funciones.espereTecla()
            return

        print(f"\t{ROJO}⚠️ ADVERTENCIA: Se eliminarán los {len(productos)} producto(s) registrados en el inventario.{RESET}")
        print(f"\t{ROJO}Esta acción no se puede deshacer.{RESET}\n")

        def ejecutar_vaciar():
            exito, eliminados = crud.vaciar_productos_db(funciones.conexion)
            if exito:
                mostrarExito(f"Se vaciaron {eliminados} producto(s) del inventario.")
            else:
                funciones.accionNoExitosa()

        pedirConfirmacion(
            "¿Estás seguro de vaciar todo el inventario de productos?",
            ejecutar_vaciar,
            "Se canceló el vaciado de productos."
        )
    except Exception as e:
        print(f"Error inesperado: {e}")
        funciones.espereTecla()

def verStockBajo():
    funciones.borrarPantalla()
    print(f"{CYAN}\n\t...::: ALERTAS DE STOCK BAJO (<= 5) :::...\n{RESET}")
    productos = crud.consultar_stock_bajo()
    if productos:
        print(f"{CYAN}{'ID':<5}|{'PRODUCTO':<20}|{'STOCK':<10}|{'CATEGORÍA':<10}{RESET}")
        print(f"{AZUL}" + "-" * 50 + f"{RESET}")
        for p in productos:
            print(f"{VERDE}{p[0]:<5}{RESET}|{p[1]:<20}|{ROJO}{p[2]:<10}{RESET}|{p[3]:<10}")
    else:
        print(f"\t{VERDE}Todos los productos cuentan con stock suficiente.{RESET}")
    funciones.espereTecla()

def menuStock():
    ciclar = True
    while ciclar:
        funciones.borrarPantalla()
        print(f"{AZUL}=============================================================={RESET}")
        print(f"{CYAN}\t\t 💲 MOVIMIENTOS DE STOCK{RESET}")
        print(f"{AZUL}=============================================================={RESET}\n")
        print(f"\t{VERDE}1.{RESET} 🛍️  Vender Producto")
        print(f"\t{VERDE}2.{RESET} 📦 Reabastecer Producto")
        print(f"\t{VERDE}3.{RESET} ⚠️  Ver Alertas de Stock Bajo")
        print(f"\t{ROJO}4.{RESET} ↩️  Regresar\n")
        print(f"{AZUL}--------------------------------------------------------------{RESET}")
        opc = input(f"{AMARILLO}Selecciona una opción: {RESET}").strip()

        match opc:
            case "1":
                registrarVenta()
            case "2":
                reabastecerMercancia()
            case "3":
                verStockBajo()
            case "4":
                ciclar = False
            case _:
                funciones.opcionInvalida()

def MenuGestion():
    ciclar = True
    while ciclar:
        funciones.borrarPantalla()
        print(f"{AZUL}=============================================================={RESET}")
        print(f"{CYAN}\t\t 🏷️  STOCK MASTER - CONTROL DE INVENTARIO{RESET}")
        print(f"{AZUL}=============================================================={RESET}\n")
        print(f"\t{VERDE}1.{RESET} 📜 Ver Productos")
        print(f"\t{VERDE}2.{RESET} ➕ Agregar Producto")
        print(f"\t{VERDE}3.{RESET} ✏️  Editar Producto")
        print(f"\t{VERDE}4.{RESET} 🗑️  Eliminar Producto")
        print(f"\t{VERDE}5.{RESET} 💾 Exportar Inventario (elige formato)")
        print(f"\t{VERDE}6.{RESET} 🧹 Vaciar Todos los Productos")
        print(f"\t{ROJO}7.{RESET} ↩️  Regresar\n")
        print(f"{AZUL}--------------------------------------------------------------{RESET}")
        opc = input(f"{AMARILLO}Seleccione una opción: {RESET}").strip()

        match opc:
            case "1":
                consultarInventario()
            case "2":
                agregarProducto()
            case "3":
                editarProducto()
            case "4":
                eliminarProducto()
            case "5":
                exportarInventarioExcel()
            case "6":
                vaciarProductos()
            case "7":
                ciclar = False
            case _:
                funciones.opcionInvalida()

def _exportarTxt(productos):
    nombre_archivo = "reporte_inventario.txt"
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        archivo.write("=" * 60 + "\n")
        archivo.write("REPORTE DE INVENTARIO - STOCKMASTER\n")
        archivo.write("=" * 60 + "\n")
        archivo.write(f"{'ID':<5}{'NOMBRE':<20}{'PRECIO':<10}{'STOCK':<10}{'CATEGORIA':<15}\n")
        archivo.write("-" * 60 + "\n")
        for id_p, nombre, precio, stock, cat_nombre in productos:
            archivo.write(f"{id_p:<5}{nombre:<20}${precio:<9.2f}{stock:<10}{cat_nombre:<15}\n")
        archivo.write("=" * 60 + "\n")
        archivo.write(f"Total de productos: {len(productos)}\n")
    return nombre_archivo

def _exportarJson(productos):
    nombre_archivo = "reporte_inventario.json"
    datos = [
        {"id": id_p, "nombre": nombre, "precio": precio, "stock": stock, "categoria": cat_nombre}
        for id_p, nombre, precio, stock, cat_nombre in productos
    ]
    reporte = {"reporte": "Inventario StockMaster", "total_productos": len(datos), "productos": datos}
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        json.dump(reporte, archivo, indent=4, ensure_ascii=False)
    return nombre_archivo

def _exportarXls(productos):
    nombre_archivo = "reporte_inventario.xls"
    ahora = datetime.now()
    hora_actual = ahora.strftime("%I:%M %p")

    html = ['<html><head><meta charset="UTF-8"></head><body>']
    html.append('<table border="1" cellspacing="0" cellpadding="4" style="border-collapse:collapse; font-family:Calibri;">')

    html.append(
        '<tr><td colspan="5" align="center" bgcolor="#1F4E78">'
        '<b><font color="#FFFFFF" size="4">REPORTE DE INVENTARIO - STOCKMASTER</font></b></td></tr>'
    )

    fecha_str = ahora.strftime("%d/%m/%Y")
    html.append(
        f'<tr><td colspan="3" align="center"><i>{fecha_str}</i></td>'
        f'<td colspan="2" align="center"><i>{hora_actual}</i></td></tr>'
    )

    html.append('<tr>')
    for encabezado in ["ID", "NOMBRE", "PRECIO", "STOCK", "CATEGORIA"]:
        html.append(f'<td align="center" bgcolor="#2E75B6"><b><font color="#FFFFFF">{encabezado}</font></b></td>')
    html.append('</tr>')

    for id_p, nombre, precio, stock, cat_nombre in productos:
        color_fondo = ' bgcolor="#FFC7CE"' if stock <= crud.UMBRAL_STOCK_BAJO else ''
        html.append(
            f'<tr{color_fondo}>'
            f'<td align="center">{id_p}</td>'
            f'<td>{nombre}</td>'
            f'<td align="center">${precio:.2f}</td>'
            f'<td align="center">{stock}</td>'
            f'<td>{cat_nombre}</td>'
            f'</tr>'
        )

    html.append(
        f'<tr><td colspan="4" align="right"><b>Total de productos:</b></td>'
        f'<td align="center"><b>{len(productos)}</b></td></tr>'
    )

    html.append('</table></body></html>')

    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        archivo.write("\n".join(html))
    return nombre_archivo

def exportarInventarioExcel():
    funciones.borrarPantalla()
    print(f"{CYAN}\n\t...::: EXPORTAR INVENTARIO :::...\n{RESET}")
    try:
        productos = crud.consultar()
        if not productos:
            print(f"\t{AMARILLO}⚠️ No hay productos para exportar.{RESET}")
            funciones.espereTecla()
            return

        print(f"{AZUL}--- Elige el formato de exportación ---{RESET}")
        print(f"\t{VERDE}1.{RESET} 📄 Texto plano (.txt)")
        print(f"\t{VERDE}2.{RESET} 📊 Excel con formato (.xls)")
        print(f"\t{VERDE}3.{RESET} 🧩 JSON (.json)")
        print(f"\t{ROJO}4.{RESET} ↩️  Cancelar\n")
        opc = input(f"{AMARILLO}Selecciona una opción: {RESET}").strip()

        exportadores = {"1": _exportarTxt, "2": _exportarXls, "3": _exportarJson}
        if opc == "4":
            return
        if opc not in exportadores:
            funciones.opcionInvalida()
            return

        nombre_archivo = exportadores[opc](productos)
        print(f"\n{VERDE}✓ Archivo generado con éxito: {nombre_archivo}{RESET}")
        funciones.espereTecla()
    except Exception as e:
        print(f"{ROJO}✖ Error al generar el archivo: {e}{RESET}")
        funciones.espereTecla()

def terminarSistema():
    print(f"\n\t{CYAN}...::: Gracias por usar el sistema de inventario :::...{RESET}\n")
    input(f"\t\t{AMARILLO}Presione ENTER para salir del sistema{RESET}")
    exit()
    
    
    