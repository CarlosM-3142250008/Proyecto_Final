from interno import funciones
from interno.Productos_Paquete import inventario
from interno.Categorias_Paquete import categorias
from interno.Historial_Paquete import historial
VERDE = "\033[1;32m"
def main():
    opc = ""
    while opc != "5":
        funciones.borrarPantalla()
        opc = inventario.MenuPrincipal()
        
        match opc:
            case "1":
                funciones.borrarPantalla()
                categorias.menuCategorias()
            case "2":
                funciones.borrarPantalla()
                inventario.MenuGestion()
            case "3":
                funciones.borrarPantalla()
                inventario.menuStock()
            case "4":
                funciones.borrarPantalla()
                historial.menuHistorial()
            case "5":
                print(f"\n\t❤️{VERDE}...::: ¡Gracias por usar el sistema! :::...❤️\n")
                exit()
            case _:
                funciones.opcionInvalida()

if __name__ == "__main__":
    main()
    
    
    
    
    
    
    