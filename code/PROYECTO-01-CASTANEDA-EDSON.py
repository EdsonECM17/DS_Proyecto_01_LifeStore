from data.lifestore_file import lifestore_products, lifestore_sales, lifestore_searches

# Se agrega lista de usuarios validos para login
admin_users = {'ecastaneda': 'lifestore12345', 'cguillen': 'holamundo'}

# Login de usuario
acesso = True # If true, accede a la información de LifeStore
additional_attempts = 2 # Intentos extra en caso de login fallido
user = input("Ingrese su usuario: ")
password = input("Ingrese su contraseña: ")
while acesso is False and additional_attempts > 0:
     
    # Validar si el usuario existe
    if user in admin_users.keys():
        #  Caso: Usuario/Contraseña validos
        if password == admin_users[user]:
            acesso = True
            print("Bienvenido "+user+".")
    # Caso: usuario o contraseña son invalidos
    if acesso is False:
        additional_attempts-=1
        print("Error con el usuario o contraseña proporcionados. Revise e intente nuevamente.")
        # Reingresar datos para siguiente iteración
        user = input("Ingrese su usuario nuevamente: ")
        password = input("Ingrese su contraseña nuevamente: ")

# Acceso correcto
if acesso:
    # ANALISIS DE VENTAS Y BUSQUEDAS POR PRODUCTO

    # Inicializar variables relacionadas al producto
    sales_per_product = {}  #  Ventas de cada productio (id_product:total_sales_of_product)
    searches_per_product = {}  # Busquedas de cada productio (id_product:total_searches_of_product)
    reviews_per_product_sum = {}  # Suma de reseñas (id_product:reviews_sum)
    reviews_per_product_avg = {} # Promedio de reseñas de cada producto (id_product:reviews_avg)
    refunds_per_product = {}  # Conteo de devoluciones por producto (id_product:refunds_sum)
    refund_per_product_pct = {} # Porcentaje de devoluciones de producto respecto a total vendido (id_product:refunds_avg)

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
    month_sales_avg = round(sales_year['sales_number']/12, 2)
    # Meses ordenados por mayor numero de ventas
    month_most_sales = sorted(sales_number_per_month, key=sales_number_per_month.get, reverse=True)


# 3 intentos fallidos
else:
    print("Demasiados intentos.\nEl acesso se ha desabilitado para este equipo.\n"+
          "Para poder acceder nuevamente, acercarse con el equipo de TI de Life Store.")
