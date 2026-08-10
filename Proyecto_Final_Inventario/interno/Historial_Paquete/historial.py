from interno import funciones
from interno.Productos_Paquete import crud,inventario

AZUL = "\033[1;34m"
VERDE = "\033[1;32m"
CYAN = "\033[1;36m"
AMARILLO = "\033[1;33m"
ROJO = "\033[1;31m"
RESET = "\033[0m"

def menuHistorial():
    ciclar = True
    while ciclar:
        funciones.borrarPantalla()
        print(f"{AZUL}=============================================================={RESET}")
        print(f"{CYAN}\t\t 🗑️  OPCIONES DE LIMPIEZA DE HISTORIAL{RESET}")
        print(f"{AZUL}=============================================================={RESET}\n")
        print(f"\t{VERDE}1.{RESET} 📜 Ver Historial Actual")
        print(f"\t{VERDE}2.{RESET} ⚠️  Vaciar Historial Completo (PERMANENTE)")
        print(f"\t{ROJO}3.{RESET} ↩️  Regresar al Menú Principal\n")
        print(f"{AZUL}--------------------------------------------------------------{RESET}")
        opc = input(f"{AMARILLO}Seleccione una opción: {RESET}").strip()

        match opc:
            case "1":
                verHistorial()
            case "2":
                vaciarHistorial()
            case "3":
                ciclar = False
            case _:
                funciones.opcionInvalida()
def verHistorial():
    funciones.borrarPantalla()
    print(f"{AZUL}=============================================================={RESET}")
    print(f"{CYAN}\t\t 📜 HISTORIAL DE MOVIMIENTOS{RESET}")
    print(f"{AZUL}=============================================================={RESET}\n")
    try:
        cursor = funciones.conexion.cursor()
        cursor.execute("SELECT id, movimiento, fecha FROM historial ORDER BY id DESC")
        registros = cursor.fetchall()
        cursor.close()

        if not registros:
            print(f"\t{AMARILLO}⚠️ No hay movimientos registrados en la base de datos.{RESET}\n")
        else:
            print(f"\t{CYAN}{'ID':<6} | {'FECHA Y HORA':<20} | {'DESCRIPCIÓN'}{RESET}")
            print(f"\t{AZUL}" + "-" * 60 + f"{RESET}")
            for reg in registros:
                fecha_str = reg[2].strftime("%Y-%m-%d %H:%M:%S") if reg[2] else "N/A"
                print(f"\t{VERDE}#{reg[0]:<5}{RESET} | {fecha_str:<20} | {reg[1]}")
    except Exception:
        funciones.accionNoExitosa()
        return

    print(f"\n{AZUL}--------------------------------------------------------------{RESET}")
    funciones.espereTecla()
               
def vaciarHistorial():
    funciones.borrarPantalla()
    print(f"{AZUL}=============================================================={RESET}")
    print(f"{CYAN}\t\t 🗑️  VACIAR Y REINICIAR HISTORIAL{RESET}")
    print(f"{AZUL}=============================================================={RESET}\n")

    try:
        cursor = funciones.conexion.cursor()
        cursor.execute("SELECT COUNT(*) FROM historial")
        total = cursor.fetchone()[0]
        cursor.close()

        if total == 0:
            print(f"\t{AMARILLO}⚠️ El historial ya se encuentra totalmente vacío.{RESET}\n")
            funciones.espereTecla()
            return

        print(f"\t{ROJO}⚠️ ADVERTENCIA: Se eliminarán {total} registro(s) y el ID volverá a iniciar en 1.{RESET}")
        print(f"\t{ROJO}Esta acción no se puede deshacer.{RESET}\n")

        def ejecutar_vaciar():
            exito, eliminados = crud.vaciar_historial_db(funciones.conexion)
            if exito:
                inventario.mostrarExito(f"Historial vaciado por completo. Se eliminaron {eliminados} registros y la secuencia de ID se reinició.")
            else:
                funciones.accionNoExitosa()

        inventario.pedirConfirmacion(
            "¿Estás seguro de ejecutar el TRUNCATE al historial?",
            ejecutar_vaciar,
            "Se canceló la limpieza del historial."
        )
    except Exception as e:
        print(f"Error inesperado al intentar vaciar el historial: {e}")
        funciones.espereTecla()
        