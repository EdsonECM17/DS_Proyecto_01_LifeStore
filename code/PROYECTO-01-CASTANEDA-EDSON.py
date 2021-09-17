from login.user_access import login
from services.lifestore_services import Service
from utils.menu_utils import select_menu, validate_question


# CONTANTES GLOABLES
# Lista de meses del año (como texto)
month_list = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

# Preguntas de Sí o No utilizadas en el menu
continue_question = "¿Desea realizar otra consulta?"
refunds_question = "¿Desea descartar ventas que terminaron en devolución?"

# Crear objeto de la clase Services para las consultas
service = Service()

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
        # Ventas anuales
        # Definir submenu de cosulta
        menu_sales={1: "Número de ventas", 2: "Ingresos totales"}
        # Desplegar menú de ventas y obtener opción seleccionada
        menu_sales_option = select_menu(menu_sales)
        # Desplegar menu para seleccionar año y obtener año como int
        menu_year = {1: "2020"}
        year = int(menu_year[select_menu(menu_year)])
        # Validar si se consideran o descartan devoluciones
        if validate_question(refunds_question):
            refunds_case = False
        else:
            refunds_case = None
        if menu_sales_option == 1:
            # Se obtiene numero de ventas y se muestra resultado
            sales_number = service.year_sales(year, refund_status=refunds_case)
            print(f"En {year}, se tuvieron un total de {sales_number} ventas.")
        elif menu_sales_option == 2:
            income = service.year_income(year, refund_status=refunds_case)
            # Se obtienen ingresos y se muestran resultados
            print(f"En {year}, los ingresos totales son ${income}.")
    elif main_menu_option == 5:
        print("1")
    elif main_menu_option == 6:
        print("1")
    elif main_menu_option == 7:
        print("Opción no disponible.")
    elif main_menu_option == 8:
        break
    # Despues de la consulta de un caso, validar si se desea continuar o salir.
    data_access = validate_question(continue_question)

print("\n¡Hasta la proxima!")
