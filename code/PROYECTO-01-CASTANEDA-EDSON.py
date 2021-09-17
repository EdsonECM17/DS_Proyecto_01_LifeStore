from login.user_access import login
from utils.menu_utils import select_menu, validate_continue


# CONTANTES GLOABLES
# Lista de meses del año (como texto)
month_list = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

# Llamar a función que valida inicio de sesion
data_access = login() # If true, continues

# Acceso correcto (data_acess = true)
while data_access:
    # Definir opciones de menu prncipal
    main_menu = {1: "Productos más vendidos", 2: "Productos rezagados",
                 3: "Productos por valoración", 4: "Ventas anuales",
                 5: "Ventas mensuales", 6: "Ventas por categoria",
                 7: "Consultas Avanzadas", 8: "Salir"}
    # Desplegar menú principal y obtener opción seleccionada
    main_menu_option = select_menu(main_menu)
    # Caso para cada opción del menu principal
    if main_menu_option == 1:
        print("1")
    elif main_menu_option == 2:
        print("1")
    elif main_menu_option == 3:
        print("1")    
    elif main_menu_option == 4:
        print("1")    
    elif main_menu_option == 5:
        print("1")
    elif main_menu_option == 6:
        print("1")
    elif main_menu_option == 7:
        print("1")
    elif main_menu_option == 8:
        break
    # Despues de la consulta de un caso, validar si se desea continuar o salir.
    data_access = validate_continue()

print("\n¡Hasta la proxima!")
