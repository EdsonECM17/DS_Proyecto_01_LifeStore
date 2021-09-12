from data.lifestore_file import lifestore_products, lifestore_sales, lifestore_searches

# CONTANTES GLOABLES
# Lista de meses del año (como texto)
month_list = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
# Lista de usuarios validos para login
admin_users = {'edson': 'lifestore12345', 'carlos': 'holamundo', 'luis':'noholamundo'}

# Login de usuario
data_access = False # If true, accede a la información de LifeStore
additional_attempts = 3 # Intentos extra en caso de login fallido
user = input("Ingrese su usuario: ")
password = input("Ingrese su contraseña: ")
while data_access is False and additional_attempts > 0:
     
    # Validar si el usuario existe
    if user in admin_users.keys():
        #  Caso: Usuario/Contraseña validos
        if password == admin_users[user]:
            data_access = True
            print("Bienvenido "+user+".")
    # Caso: usuario o contraseña son invalidos
    if data_access is False:
        additional_attempts-=1
        if additional_attempts == 0:
            continue
        print("Error con el usuario o contraseña proporcionados. Revise e intente nuevamente.")
        # Reingresar datos para siguiente iteración
        user = input("Ingrese su usuario nuevamente: ")
        password = input("Ingrese su contraseña nuevamente: ")

# Acceso correcto
if data_access:
    # ANALISIS DE VENTAS Y BUSQUEDAS POR PRODUCTO

    # Inicializar variables relacionadas al producto
    sales_per_product = {}  #  Ventas de cada productio (id_product:total_sales_of_product)
    searches_per_product = {}  # Busquedas de cada productio (id_product:total_searches_of_product)
    not_sold_products = []  # Id de productos no vendidos
    reviews_per_product_sum = {}  # Suma de reseñas (id_product:reviews_sum)
    reviews_per_product_avg = {} # Promedio de reseñas de cada producto (id_product:reviews_avg)
    refunds_per_product = {}  # Conteo de devoluciones por producto (id_product:refunds_sum)
    refund_per_product_pct = {} # Porcentaje de devoluciones de producto respecto a total vendido (id_product:refunds_avg)
    reviews_weight = 0.6  # Valor de reseñas para determinar calificación de producto.
    refunds_weight = 0.4  # Valor de rembolsos para determinar calificación de producto.
    grade_product = {}  # Calificación de producto. 60 % reviews y 40 % porcentaje de devoluciones. (id_product: grade)

    # Iniciar analisis de cada producto
    for product in lifestore_products:
        sales_per_product[product[0]] = 0
        searches_per_product[product[0]] = 0
        refunds_per_product[product[0]] = 0
        reviews_per_product_sum[product[0]] = 0

        # Contar ventas del producto y sumar reseñas y devoluciones
        for sale in lifestore_sales:
            if sale[1] == product[0]:
                sales_per_product[product[0]] +=1
                reviews_per_product_sum[product[0]]+= sale[2]
                refunds_per_product[product[0]] += sale[4]
        # Contar busqueda de producto
        for search in lifestore_searches:
            if search[1] == product[0]:
                searches_per_product[product[0]] +=1

    # Resumen de analisis por producto
    # Identificar id de 50 productos mas vendidos
    most_sold_products = sorted(sales_per_product, key=sales_per_product.get, reverse=True)[:50]
    # Identificar id de 100 productos mas buscados
    most_searched_products = sorted(searches_per_product, key=searches_per_product.get, reverse=True)[:100]
    # Identificar id de 50 productos menos vendidos
    less_sold_products = sorted(sales_per_product, key=sales_per_product.get)[:50]
    # Identificar id de 100 productos menos buscados
    less_searched_products = sorted(searches_per_product, key=searches_per_product.get)[:100]

    # Obtener promedio de reseñas de cada producto y porcentaje de devoluaciones
    for id_product in reviews_per_product_sum.keys():
        # Procesar datos solo en casos de que existan ventas del producto
        if sales_per_product[id_product] > 0:
            reviews_per_product_avg[id_product] = reviews_per_product_sum[id_product]/sales_per_product[id_product]
            refund_per_product_pct[id_product] = round((refunds_per_product[id_product]/sales_per_product[id_product])*100, 2)
        else:
            reviews_per_product_avg[id_product] = 0
            refund_per_product_pct[id_product] = 0
    
    for id_product in refund_per_product_pct.keys():
        # Se consideran solo productos con ventas
        if sales_per_product[id_product] > 0:
            # Obtener partes de califiguración y sumarlas para obtener la calificación
            reviews_part = reviews_weight*(reviews_per_product_avg[id_product]/5)*100
            refunds_part = refunds_weight*(100-refund_per_product_pct[id_product])
            grade_product[id_product]= reviews_part + refunds_part
        else:
            not_sold_products.append(id_product)

    # Ordenar calificaciones de mayor a menor
    grade_sorted = sorted(grade_product, key=grade_product.get, reverse=True)
    best_graded = grade_sorted[:20]
    worse_graded = grade_sorted[-20:]


    # ANALISIS DE VENTAS Y BUSQUEDAS POR TIEMPO (mes y año)
    # Inicializar datos del cada mes y datos anuales
    sales_income_per_month = {}
    sales_number_per_month = {}
    sales_year = {'sales_number': 0, 'sales_income': 0}
    for i in range(1,13):
        sales_income_per_month[i] = 0
        sales_number_per_month[i] = 0
    
    # Iniciar analisis de cada venta registrada
    for sale in lifestore_sales:
        # Identificar mes de la fecha a partir del string en lifestore_sales
        month=sale[3].split('/')[1]
        # Añadir venta al conteo mensual
        sales_number_per_month[int(month)] += 1
        # Buscar precio de producto
        for product in lifestore_products:
            if sale[1] == product[0]:
                # Añadir precio a ingresos del mes
                sales_income_per_month[int(month)] += product[2]
                break
    
    # Añadir resultados de cada mes a la variable año
    for month in sales_income_per_month.keys():
        sales_year['sales_number'] += sales_number_per_month[month]
        sales_year['sales_income'] += sales_income_per_month[month]
    # Ventas promedio por mes
    month_sales_avg = round(sales_year['sales_number']/12)
    # Meses ordenados por mayor numero de ventas
    month_most_sales = sorted(sales_number_per_month, key=sales_number_per_month.get, reverse=True)

    # Resultados de analisis de tiempo
    print("Analisis por tiempo - Resultados\n\n")
    for month in sales_income_per_month.keys():
        # Generar mensaje de ingresos al mes que mostrar e imprimir.
        # Mediante month y month_list se obtiene el mes como texto
        month_income_msg = ("El mes de " + month_list[int(month-1)] + " se tuvieron ingresos de $" +
                            str(sales_income_per_month[month])+ ", con un total de " +
                            str(sales_number_per_month[month]) + " ventas.")
        print(month_income_msg)
    
    # Mostrar ventas promedio mensuales
    print("\nEn promedio al mes se venden " + str(month_sales_avg) + " productos.")

    # Mostrar ingresos y ventas totales anuales
    year_income_msg = ("\nEn total, en el año se tuvieron ingresos de $" + str(sales_year['sales_income']) +
                       ", obtenidos mediante " + str(sales_year['sales_number']) + " ventas.")
    print(year_income_msg)
    # Mostrar meses con mas ventas al año
    # For para formar string con 6 meses con mas ventas al año
    print("\nLos meses con mas ventas al año son:")
    i = 0
    for month in month_most_sales[:6]:
        i += 1
        print(" " + str(i) + ".-" + month_list[int(month-1)])

# 3 intentos fallidos
else:
    print("Demasiados intentos.\nEl acceso se ha desabilitado para este equipo.\n"+
          "Para poder acceder nuevamente, acercarse con el equipo de TI de Life Store.")
