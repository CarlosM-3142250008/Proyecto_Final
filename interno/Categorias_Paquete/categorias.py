from interno import funciones
from interno.Categorias_Paquete import crud_categorias

AZUL = "\033[1;34m"
VERDE = "\033[1;32m"
CYAN = "\033[1;36m"
AMARILLO = "\033[1;33m"
ROJO = "\033[1;31m"
RESET = "\033[0m"

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

def consultarCategorias():
    try:
        funciones.borrarPantalla()
        print(f"{CYAN}\n\t...:::: LISTA DE CATEGORÍAS ::::...\n{RESET}")
        cats = crud_categorias.consultar()
        if cats:
            print(f"\t{CYAN}{'ID':<5}|{'NOMBRE':<20}{RESET}")
            print(f"\t{AZUL}" + "-" * 30 + f"{RESET}")
            for id_cat, nombre in cats:
                print(f"\t{VERDE}#{id_cat:<4}{RESET}|{nombre:<20}")
        else:
            print(f"\t{AMARILLO}⚠️ No hay categorías registradas.{RESET}")
    except Exception as e:
        print(f"Error al mostrar categorías: {e}")
    funciones.espereTecla()

def agregarCategoria():
    try:
        funciones.borrarPantalla()
        print(f"{CYAN}\n\t...::: AGREGAR CATEGORÍA :::...\n{RESET}")
        nombre = funciones.pedirTextoValidado(
            "Introduce el nombre de la nueva categoría (solo letras): ",
            funciones.validarNombre,
            "El nombre solo debe contener letras y espacios (2 a 40 caracteres)."
        )
        if nombre:
            print(f"\n{AZUL}--- RESUMEN DE CAMBIOS ---{RESET}")
            print(f"Acción: Registro de nueva categoría")
            print(f"Nombre: {nombre}")
            
            def ejecutar_insertar():
                if crud_categorias.insertar(nombre):
                    mostrarExito(f"Se agregó correctamente la categoría '{nombre}'.")
                else:
                    funciones.accionNoExitosa()

            pedirConfirmacion(
                "¿Estás seguro de realizar este cambio?",
                ejecutar_insertar,
                f"El usuario decidió no agregar la categoría '{nombre}'."
            )
        else:
            funciones.opcionInvalida()
    except Exception as e:
        print(f"Error inesperado: {e}")
        funciones.espereTecla()

def editarCategoria():
    try:
        funciones.borrarPantalla()
        print(f"{CYAN}\n\t...::: EDITAR CATEGORÍA :::...\n{RESET}")
        cats = crud_categorias.consultar()
        if not cats:
            funciones.accionNoExitosa()
            funciones.espereTecla()
            return

        print(f"{AZUL}--- Categorías Existentes ---{RESET}")
        ids_validos = []
        for id_cat, nombre in cats:
            print(f"{VERDE}#{id_cat:<4}{RESET}| {nombre}")
            ids_validos.append(str(id_cat))

        id_cat_input = input("\nID de la categoría a editar: ").strip()
        if not id_cat_input.isdigit() or id_cat_input not in ids_validos:
            funciones.opcionInvalida()
            return

        nuevo_nombre = input("Nuevo nombre: ").strip()
        if nuevo_nombre:
            print(f"\n{AZUL}--- RESUMEN DE CAMBIOS ---{RESET}")
            print(f"Acción: Edición de categoría")
            print(f"ID Categoría: {id_cat_input}")
            print(f"Nuevo Nombre: {nuevo_nombre}")
            
            def ejecutar_editar():
                if crud_categorias.editar(int(id_cat_input), nuevo_nombre):
                    mostrarExito(f"Se modificó correctamente la categoría ID {id_cat_input} a '{nuevo_nombre}'.")
                else:
                    funciones.accionNoExitosa()

            pedirConfirmacion(
                "¿Estás seguro de realizar este cambio?",
                ejecutar_editar,
                f"Se descartaron las modificaciones para la categoría ID {id_cat_input}."
            )
        else:
            funciones.opcionInvalida()
    except Exception as e:
        print(f"Error inesperado: {e}")
        funciones.espereTecla()

def eliminarCategoria():
    try:
        funciones.borrarPantalla()
        print(f"{CYAN}\n\t...::: ELIMINAR CATEGORÍA :::...\n{RESET}")
        cats = crud_categorias.consultar()
        if not cats:
            funciones.accionNoExitosa()
            funciones.espereTecla()
            return

        ids_validos = {}
        for id_c, nombre in cats:
            print(f"{VERDE}#{id_c:<4}{RESET}| {nombre}")
            ids_validos[str(id_c)] = nombre

        id_cat_input = input("\nID de la categoría a eliminar: ").strip()
        if not id_cat_input.isdigit() or id_cat_input not in ids_validos:
            funciones.opcionInvalida()
            funciones.espereTecla()
            return

        nombre_cat = ids_validos[id_cat_input]
        prods_asociados = crud_categorias.obtener_productos_por_categoria(int(id_cat_input))

        print(f"\n{AZUL}--- RESUMEN DE CAMBIOS ---{RESET}")
        print(f"Acción: Eliminar categoría '{nombre_cat}' (ID: {id_cat_input})")
        
        if prods_asociados:
            print(f"\n{ROJO}⚠️ ADVERTENCIA: Los siguientes productos pertenecen a esta categoría y serán afectados/eliminados:{RESET}\n")
            
            print(f"  +-------+--------------------------------+")
            print(f"  | {AMARILLO}{'ID':<5}{RESET} | {AMARILLO}{'NOMBRE DEL PRODUCTO':<30}{RESET} |")
            print(f"  +-------+--------------------------------+")
            
            for id_p, nom_p, *resto in prods_asociados:
                print(f"  | {id_p:<5} | {nom_p:<30} |")
            
            print(f"  +-------+--------------------------------+\n")
        else:
            print(f"\n{VERDE}✓ Esta categoría no tiene productos asociados.{RESET}\n")

        def ejecutar_eliminar():
            if crud_categorias.eliminar(int(id_cat_input)):
                mostrarExito(f"Se eliminó correctamente la categoría '{nombre_cat}' (ID: {id_cat_input}).")
            else:
                funciones.accionNoExitosa()

        pedirConfirmacion(
            "¿Estás seguro de realizar este cambio y eliminar esta categoría?",
            ejecutar_eliminar,
            f"No se eliminó la categoría ID {id_cat_input}."
        )
    except Exception as e:
        print(f"Error inesperado: {e}")
        funciones.espereTecla()

def menuCategorias():
    ciclar = True
    while ciclar:
        funciones.borrarPantalla()
        print(f"{AZUL}=============================================================={RESET}")
        print(f"{CYAN}\t\t 📂 GESTIÓN DE CATEGORÍAS{RESET}")
        print(f"{AZUL}=============================================================={RESET}\n")
        print(f"\t{VERDE}1.{RESET} 📜 Ver Categorías")
        print(f"\t{VERDE}2.{RESET} ➕ Agregar Categoría")
        print(f"\t{VERDE}3.{RESET} ✏️  Editar Categoría")
        print(f"\t{VERDE}4.{RESET} 🗑️  Eliminar Categoría")
        print(f"\t{ROJO}5.{RESET} ↩️  Regresar\n")
        print(f"{AZUL}--------------------------------------------------------------{RESET}")
        opc = input(f"{AMARILLO}Seleccione una opción: {RESET}").strip()

        match opc:
            case "1":
                consultarCategorias()
            case "2":
                agregarCategoria()
            case "3":
                editarCategoria()
            case "4":
                eliminarCategoria()
            case "5":
                ciclar = False
            case _:
                funciones.opcionInvalida()
                
                