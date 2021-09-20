from services.lifestore_services import Service
from utils.graph_utils import Summary_Chart
from login.user_access import login
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
plot_path = "output" # Carpeta para gráficas

# EJECUCIÓN PROGRAMA PRINCIPAL
# Crear objeto de la clase Services para las consultas
service = Service()
# Crear objeto de la clase Grafica
plot = Summary_Chart(plot_path)

# Llamar a función que valida inicio de sesion
data_access = login() # If true, continues

# Acceso correcto (data_acess = true)
while data_access:
    # Desplegar menú principal y obtener opción seleccionada
    main_menu_option = select_menu(main_menu)
    # Caso para cada opción del menu principal
    if main_menu_option == 1:
        # Caso producto más vendidos
        # Consulta las ventas de cada producto
        product_sales = service.get_products_sales()
        # Ordenar lista de productos organizados de mayor a menor número de ventas
        most_sold_products = sorted(product_sales, key=product_sales.get, reverse=True)
        # Filtrar y presentar los 50 productos más vendidos
        print("Productos más vendidos de la tienda:")
        for i in range(0, 50):
            # Si no existieran tantos elementos en la lista, salir de bucle
            if i>=len(most_sold_products):
                break
            # Obtiene el id del producto en posición i
            product_id = most_sold_products[i]
            # Obtiene el nombre del producto
            product_name = service.get_product_name(product_id)
            # Obtiene la cantidad de unidades en inventario del producto
            product_stock = service.get_product_stock(product_id)
            # Muestra nombre del producto junto a ventas y unidades en inventario.
            print(f"{i+1}.- {product_name} (ID: {product_id:02d}). Ventas: {product_sales[product_id]}.")
            print(f"Unidades en inventario: {product_stock}.")
        print('\n')
        # Consulta las busquedas de cada producto
        product_searches = service.get_products_searches()
        # Ordenar lista de productos organizados de mayor a menor número de busquedas
        most_searched_products = sorted(product_searches, key=product_searches.get, reverse=True)
        # Filtrar y presentar los 50 productos más buscados
        print("Productos más buscados de la tienda:")
        for i in range(0, 50):
            # Si no existieran tantos elementos en la lista, salir de bucle
            if i>=len(most_searched_products):
                break
            # Obtiene el id del producto en posición i
            product_id = most_searched_products[i]
            # Obtiene el nombre del producto
            product_name = service.get_product_name(product_id)
            # Despliega nombre del producto y busquedas al usuario.
            print(f"{i+1}.- {product_name} (ID: {product_id: 02d}). Busquedas: {product_searches[product_id]}")
    
    elif main_menu_option == 2:
        # Caso productos rezagados
        # Consulta las ventas de cada producto
        product_sales = service.get_products_sales()
        # Ordenar lista de productos organizados de menor a mayor número de ventas
        less_sold_products = sorted(product_sales, key=product_sales.get, reverse=True)
        # Filtrar y presentar los 50 productos menos vendidos
        print("Productos menos vendidos de la tienda:")
        for i in range(0, 50):
            # Si no existieran tantos elementos en la lista, salir de bucle
            if i>=len(less_sold_products):
                break
            # Obtiene el id del producto en posición i
            product_id = less_sold_products[i]
            # Obtiene el nombre del producto
            product_name = service.get_product_name(product_id)
            # Obtiene la cantidad de unidades en inventario del producto
            product_stock = service.get_product_stock(product_id)
            # Muestra nombre del producto junto a ventas y unidades en inventario
            print(f"{i+1}.- {product_name} (ID: {product_id:02d}). Ventas: {product_sales[product_id]}.")
            print(f"Unidades en inventario: {product_stock}.")
        print('\n')
        # Consulta las busquedas de cada producto
        product_searches = service.get_products_searches()
        # Ordenar lista de productos organizados de menor a mayor número de busquedas
        less_searched_products = sorted(product_searches, key=product_searches.get)
        # Filtrar y presentar los 50 productos menos buscados
        print("Productos menos buscados de la tienda:")
        for i in range(0, 50):
            # Si no existieran tantos elementos en la lista, salir de bucle
            if i>=len(less_searched_products):
                break
            # Obtiene el id del producto en posición i
            product_id = less_searched_products[i]
            # Obtiene el nombre del producto
            product_name = service.get_product_name(product_id)
            # Despliega nombre del producto y busquedas al usuario
            print(f"{i+1}.- {product_name} (ID: {product_id: 02d}). Busquedas: {product_searches[product_id]}")
    
    elif main_menu_option == 3:
        # Caso de valoración de productos
        product_grades = service.get_product_grades()
        # Separar productos con calificación (ventas>0) de los productos no calificados ('N.D.')
        non_graded_products = {id_product:grade for (id_product,grade) in product_grades.items() if isinstance(grade, str)}
        graded_products = {id_product:grade for (id_product,grade) in product_grades.items() if isinstance(grade, float)}
        # Filtrar productos por calificacion de mayor a menor
        most_valued_products = sorted(graded_products, key=graded_products.get, reverse=True)
        # Productos con mejor valoración
        print("Los productos mejor valorados son:")
        for i in range(0, 20):
            # Si no existieran tantos elementos en la lista, salir de bucle
            if i>=len(most_valued_products):
                break
            # Obtiene el id del producto en posición i
            product_id = most_valued_products[i]
            # Obtiene el nombre del producto
            product_name = service.get_product_name(product_id)
            # Muestra nombre del producto junto a su valoración
            print(f"{i+1}.- {product_name} (ID: {product_id:02d}). Valoración: {product_grades[product_id]}.")
        print("\n")
        # Productos con menor valoración
        print("Los productos peor valorados son:")
        for i in range(0, 20):
            # Si no existieran tantos elementos en la lista, salir de bucle
            if i>=len(most_valued_products):
                break
            # Obtiene el id del producto en posición [-(1+i)]
            product_id = most_valued_products[-(1+i)]
            # Obtiene el nombre del producto
            product_name = service.get_product_name(product_id)
            # Muestra nombre del producto junto a su valoración
            print(f"{i+1}.- {product_name} (ID: {product_id:02d}). Valoración:: {product_grades[product_id]}.")
        print("\n")
        print(f"Por otro lado, hay {len(non_graded_products)} equipos sin ventas, y en consecuencia, sin valoración.")
        print("Los productos que no tienen valoración son:")
        for product_id in non_graded_products.keys():
                # Obten nombre del producto
                product_name = service.get_product_name(product_id)
                # Imprime datos del producto
                print(f"ID:{product_id:02d} - {product_name}.")
    
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
            sales_number = service.get_year_sales(year, refund_status=refunds_case)
            print(f"En {year}, se tuvieron un total de {sales_number} ventas.")
            print(f"En promedio, se tuvieron {round(sales_number/12)} ventas al mes.")
        elif menu_sales_option == 2:
            # Se obtienen ingresos y se muestran resultados
            income = service.get_year_income(year, refund_status=refunds_case)
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
            sales_month = service.get_monthly_sales(year, refund_status=refunds_case)
            # Se muestran los resultados de cada mes
            print(f"Ventas mensuales del año {year}:")
            for month in sales_month.keys():
                print(f"{month}.- {month_list[month-1]}: {sales_month[month]}")
            # Se ordenan los meses en una lista de mayor a menor numero de ventas
            month_most_sales = sorted(sales_month, key=sales_month.get, reverse=True)
            # Se presentan los meses con mayor número de ventas
            print("\nMeses con más ventas:")
            for i in range(0,6):
                month = month_most_sales[i]
                print(f"{i+1}.- {month_list[month-1]}")
            # Se presentan los meses con menor número de ventas
            print("\nMeses con menos ventas:")
            for i in range(0,6):
                month = month_most_sales[11-i] # Del ultimo al primero
                print(f"{i+1}.- {month_list[month-1]}")
            print("")
            # Graficar resultados
            plot.bar_summary(sales_month, f"Ventas Mensuales en {year}", "Mes",
                             "No. de Ventas", "mes_ventas")
        elif menu_sales_option == 2:
            # Se obtienen ingresos y se muestran resultados
            income_month = service.get_monthly_income(year, refund_status=refunds_case)
            # Se muestran los resultados de cada mes
            print(f"Ingresos mensuales del año {year}:")
            for month in income_month.keys():
                print(f"{month}.- {month_list[month-1]}: ${income_month[month]:,.2f}")
            # Se ordenan los meses en una lista de más a menos ingresos
            month_most_income = sorted(income_month, key=income_month.get, reverse=True)
            # Se presentan los meses con mayor número de ingresos
            print("\nMeses con más ingresos:")
            for i in range(0,6):
                month = month_most_income[i]
                print(f"{i+1}.- {month_list[month-1]}")
            # Se presentan los meses con menor número de ingresos
            print("\nMeses con menos ingresos:")
            for i in range(0,6):
                month = month_most_income[11-i] # Del ultimo al primero
                print(f"{i+1}.- {month_list[month-1]}")
            print("")
            # Graficar resultados
            plot.bar_summary(income_month, f"Ingresos Mensuales en {year}", "Mes",
                             "Ingresos [$]", "mes_ingresos", "green")
    
    elif main_menu_option == 6:
        # Caso ventas por categorias
        # Obtener no. de productos por categoria y mostrar
        category_products = service.count_category_products()
        print("Productos por categoria:")
        for category in category_products.keys():
            print(f"- {category}: {category_products[category]}")
        print("")
        # Graficar resultados
        plot.bar_summary(category_products, "Productos por categoría", "Categoría",
                        "No. de Producto", "categoria_productos", "red")
        # Obtener ventas por categoria y mostrar
        category_sales = service.get_category_sales(refund_status=False)
        print("\nNúmero de ventas por categoria:")
        for category in category_sales.keys():
            print(f"- {category}: {category_sales[category]}")
        print("")
        # Graficar resultados
        plot.bar_summary(category_sales, "Ventas por categoría", "Categoría",
                        "No. de Ventas", "categoria_ventas")
        # Obtener ingresos por categoria y mostrar
        category_income = service.get_category_income(refund_status=False)
        print("\nIngresos por categoria:")
        for category in category_income.keys():
            print(f"- {category}: ${category_income[category]:,.2f}")
        print("")
        # Graficar resultados
        plot.bar_summary(category_income, "Ingresos por categoría", "Categoría",
                        "Ingresos [$]", "categoria_ingresos", "green")
    
    elif main_menu_option == 7:
        print("Opción no disponible.")
    
    elif main_menu_option == 8:
        break
    # Despues de la consulta de un caso, validar si se desea continuar o salir.
    print('')
    data_access = validate_question(continue_question)

print("\n¡Hasta la proxima!")
