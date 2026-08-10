import mysql.connector
import re
AMARILLO = "\033[1;33m"
ROJO = "\033[1;31m"
RESET = "\033[0m"
VERDE = "\033[1;32m"
NEGRITA = "\033[1m"
def conectar():
    try:
        return mysql.connector.connect(
            host="localhost",      
            user="root",          
            password="",           
            database="stockmaster_db"  
    )
    except:
            print(f"{ROJO}=============================================================={RESET}")
            print(f"{NEGRITA}\t\t 📦 Base de datos apagada\n\t\t    Prende MySQL en Xampp{RESET}")
            print(f"{ROJO}=============================================================={RESET}\n")
            input("\n\t\tPRESIONE ENTER PARA SALIR\n")
            exit()

conexion = conectar()

def borrarPantalla():
    print("\033c")

def opcionInvalida():
    input(f"\n\t\t{ROJO}...¡Opción inválida, por favor verifique!...{RESET}{AMARILLO}\n\t\t    ...¡Oprima ENTER para continuar!...{RESET}")

def espereTecla():
    input(f"\n\t\t{NEGRITA}    ...¡Oprima  ENTER para continuar!...{RESET}")

def accionExitosa():
    input(f"\n\t\t{VERDE}...¡Acción Realizada con Éxito!...{RESET}")

def accionNoExitosa():
    input(f"\n\t\t{AMARILLO}...¡No fue posible realizar esta acción, inténtalo más tarde!...{RESET}")


# VALIDACIÓN DE ENTRADA POR TECLADO CON RegEx

PATRON_NOMBRE = r'^[A-Za-zÁÉÍÓÚáéíóúÑñ]+(?:\s[A-Za-zÁÉÍÓÚáéíóúÑñ]+)*$'
PATRON_PRECIO = r'^\d+(\.\d{1,2})?$'
PATRON_ENTERO_POSITIVO = r'^[1-9]\d*$'

def validarNombre(texto):
    #Valida que el texto contenga solo letras y espacios simples (2 a 40 caracteres)."""
    if not (2 <= len(texto) <= 40):
        return False
    return re.match(PATRON_NOMBRE, texto) is not None

def validarPrecio(texto):
    #Valida que el texto sea un número decimal válido, con hasta 2 decimales (ej. 12 o 12.50)."""
    return re.match(PATRON_PRECIO, texto) is not None

def validarEnteroPositivo(texto):
   #Valida que el texto sea un número entero positivo, sin ceros a la izquierda."""
    return re.match(PATRON_ENTERO_POSITIVO, texto) is not None

def pedirTextoValidado(mensaje, patron_validador, mensaje_error="Entrada no válida, intenta de nuevo."):
    #Pide un dato por teclado y lo repite hasta que cumpla con el validador RegEx indicado."""
    while True:
        valor = input(mensaje).strip()
        if patron_validador(valor):
            return valor
        print(f"{ROJO}⚠️  {mensaje_error}{RESET}")
        
        
        
        
        
