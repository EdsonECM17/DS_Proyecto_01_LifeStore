from login.user_access import login
from services.lifestore_services import Service
from utils.menu_utils import select_menu, validate_question


# CONTANTES GLOABLES
# MENUS DE INTERFAZ DE USUARIO
# Definir menu principal
main_menu = {1: "Productos más vendidos", 2: "Productos rezagados",
             3: "Productos por valoración", 4: "Ventas anuales",
             5: "Ventas mensuales", 6: "Ventas por categoria",
             7: "Consultas Avanzadas", 8: "Salir"}
# Definir submenu de consulta
menu_sales={1: "Número de ventas", 2: "Ingresos totales"}
# Definir submenu de año
menu_year = {1: "2020"}

# Preguntas de Sí o No utilizadas en el menu
continue_question = "¿Desea realizar otra consulta?"
refunds_question = "¿Desea descartar ventas que terminaron en devolución?"

# Variables auxiliares
month_list = ("Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre")


# EJECUCIÓN PROGRAMA PRINCIPAL
# Crear objeto de la clase Services para las consultas
service = Service()

# Llamar a función que valida inicio de sesion
data_access = login() # If true, continues

# Acceso correcto (data_acess = true)
while data_access:
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
        # Caso: Ventas Anuales
        # Desplegar menú de ventas y obtener opción seleccionada
        menu_sales_option = select_menu(menu_sales)
        # Desplegar menu para seleccionar año y obtener año como int
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
            print(f"En promedio, se tuvieron {round(sales_number/12)} ventas al mes.")
        elif menu_sales_option == 2:
            # Se obtienen ingresos y se muestran resultados
            income = service.year_income(year, refund_status=refunds_case)
            print(f"En {year}, los ingresos totales son ${income:,.2f}.")
    elif main_menu_option == 5:
        # Caso: Ventas Mensuales
        # Desplegar menú de ventas y obtener opción seleccionada
        menu_sales_option = select_menu(menu_sales)
        # Desplegar menu para seleccionar año y obtener año como int
        year = int(menu_year[select_menu(menu_year)])
        # Validar si se consideran o descartan devoluciones
        if validate_question(refunds_question):
            refunds_case = False
        else:
            refunds_case = None
        if menu_sales_option == 1:
            # Se obtiene numero de ventas de cada mes
            sales_month = service.month_sales(year, refund_status=refunds_case)
            # Se muestran los resultados de cada mes
            print(f"Ventas mensuales del año {year}:")
            for month in sales_month.keys():
                print(f"{month}.- {month_list[month-1]}: {sales_month[month]}")
            print('\n')
            # Se ordenan los meses en una lista de mayor a menor numero de ventas
            month_most_sales = sorted(sales_month, key=sales_month.get, reverse=True)
            # Se presentan los meses con mayor número de ventas
            print("Meses con más ventas:")
            for i in range(0,6):
                month = month_most_sales[i]
                print(f"{i+1}.- {month_list[month-1]}")
            print('\n')
            # Se presentan los meses con menor número de ventas
            print("Meses con menos ventas:")
            for i in range(0,6):
                month = month_most_sales[11-i] # Del ultimo al primero
                print(f"{i+1}.- {month_list[month-1]}")
        elif menu_sales_option == 2:
            # Se obtienen ingresos y se muestran resultados
            income_month = service.month_income(year, refund_status=refunds_case)
            # Se muestran los resultados de cada mes
            print(f"Ingresos mensuales del año {year}:")
            for month in income_month.keys():
                print(f"{month}.- {month_list[month-1]}: ${income_month[month]:,.2f}")
            print('\n')
            # Se ordenan los meses en una lista de más a menos ingresos
            month_most_income = sorted(income_month, key=income_month.get, reverse=True)
            # Se presentan los meses con mayor número de ingresos
            print("Meses con más ingresos:")
            for i in range(0,6):
                month = month_most_income[i]
                print(f"{i+1}.- {month_list[month-1]}")
            print('\n')
            # Se presentan los meses con menor número de ingresos
            print("Meses con menos ingresos:")
            for i in range(0,6):
                month = month_most_income[11-i] # Del ultimo al primero
                print(f"{i+1}.- {month_list[month-1]}")
    elif main_menu_option == 6:
        print("1")
    elif main_menu_option == 7:
        print("Opción no disponible.")
    elif main_menu_option == 8:
        break
    # Despues de la consulta de un caso, validar si se desea continuar o salir.
    print('')
    data_access = validate_question(continue_question)

print("\n¡Hasta la proxima!")
