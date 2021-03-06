import calendar

from processing.lifestore_tables import lifestore_products, lifestore_sales, lifestore_searches
from processing.filters_df import Filters


class Service(Filters):
    """ 
    Clase que agrupa diversas operaciones de consulta de los datos de LifeStore, para apoyar
    el análisis de información.
    Esta clase es hija de la clase Filters, por lo que tiene acceso a sus métodos.
    """

    # Métodos generales
    def count_sales(self, id_product: int or None = None, start_date: str or None = None,
                    end_date: str or None = None, score_min: int or None = None,
                    score_max: int or None = None, refund_status: bool or None = None) -> int:
        """ 
        Consulta la tabla de ventas con una serie de filtros de producto y/o tiempo, extrayendo
        solo las filas de interés. Mediante un conteo de las ventas que cumplen con las condiciones
        del caso, se determina el número de ventas.

        Args:
            id_product (int or None, optional): Id de producto. Defaults to None.
            start_date (str or None, optional): Fecha de inicio de periodo de ventas considerado. Defaults to None.
            end_date (str or None, optional): Fecha de inicio de periodo de ventas considerado. Defaults to None.
            score_min (int or None, optional): Calificación mínima de venta. Defaults to None.
            score_max (int or None, optional): Calificación máxima de venta. Defaults to None.
            refund_status (bool or None, optional): Ventas devueltas (True) o no devueltas (False). Defaults to None.

        Returns:
            int: Número de ventas que tuvo el caso solicitado.
        """
        # Obtener subtabla de tabla de ventas con filas que cumplan con los filtros indicados
        sales_df = self._Filters__filter_sales_df(id_product = id_product, start_date = start_date,
                                                  end_date = end_date, refund = refund_status,
                                                  score_min = score_min, score_max = score_max)
       # Contar ventas mediante el número de filas de la tabla filtrada
        sales_number = len(sales_df)
        return sales_number

    def calculate_income(self, id_product: int or None = None, start_date: str or None = None,
                         end_date: str or None = None, score_min: int or None = None,
                         score_max: int or None = None, refund_status: bool or None = None) -> int:
        """ 
        Obtiene el total de ingresos para un producto especifico o todos los productos
        que cumplan con los filtros en las entradas.

        Args:
            id_product (int or None, optional): Id de producto. Defaults to None.
            start_date (str or None, optional): Fecha de inicio de periodo de ventas considerado. Defaults to None.
            end_date (str or None, optional): Fecha de inicio de periodo de ventas considerado. Defaults to None.
            score_min (int or None, optional): Calificación mínima de venta. Defaults to None.
            score_max (int or None, optional): Calificación máxima de venta. Defaults to None.
            refund_status (bool or None, optional): Ventas devueltas (True) o no devueltas (False). Defaults to None.

        Returns:
            int: Total de ingresos para caso solicitado.
        """
        income = 0
        # Si se incluyo un id_product en la solicitud, filtra la tabla generada ahora por producto
        if id_product is not None:
            product_sales = self.count_sales(id_product, start_date, end_date, score_min,
                                             score_max, refund_status)
            income = product_sales * lifestore_products["price"][lifestore_products["id_product"] == id_product].item()
        # Si no se indico id_product, se itera cada id, y se suman los ingresos de cada producto diferente 
        else:
            for row in lifestore_products.iterrows():
                # Se obtiene id
                id_product = row[1]['id_product']
                # Se cuentan ventas del producto
                product_sales = self.count_sales(id_product, start_date, end_date, score_min,
                                                 score_max, refund_status)
                # Se suman los ingresos del producto a los ingresos totales
                income += product_sales * lifestore_products["price"][lifestore_products["id_product"] == id_product].item()
        return income

    def count_searches(self, id_product: int or None):
        """ 
        Consulta la tabla de búsquedas con un filtro de producto y cuenta la cantidad
        de búsquedas que cumplan con las condiciones indicadas.

        Args:
            id_product (int or None, optional): Id de producto. Defaults to None.

        Returns:
            int: número de búsquedas que tuvo el caso solicitado.
        """
        # Obtener tabla de búsquedas filtrada. Si no hay filtro, se obtiene completa
        searches_df = self._Filters__filter_searches_df(id_product = id_product)
        # Contar búsquedas
        searches_number = len(searches_df)
        return searches_number

    # Métodos relacionados a tiempo
    def get_year_sales(self, year:int, id_product: int or None = None, refund_status: bool or None = None) -> int:
        """ 
        Obtiene el número de ventas anuales. Cuenta con algunos filtros opcionales que permiten
        considerar únicamente un producto o descartar las ventas que terminaron en devolución.

        Args:
            year (int): Año seleccionado.
            id_product (int or None, optional): Id de producto. Defaults to None.
            refund_status (bool or None, optional): Filtro de devoluciones. Defaults to None.

        Returns:
            int: Número de ventas anuales.
        """
        # Definir fecha de inicio del año y fecha de fin de año para filtros
        year_start= f"{year}-01-01"
        year_end = f"{year}-12-31"
        # Usar función get ventas para obtener datos de ventas anuales con los filtros
        sales_number = self.count_sales(start_date=year_start, end_date=year_end,
                                        id_product=id_product, refund_status=refund_status)
        return sales_number
    
    def get_year_income(self, year:int, id_product: int or None = None, refund_status: bool or None = None) -> int:
        """ 
        Obtiene los ingresos anuales. Cuenta con algunos filtros opcionales que permiten
        considerar únicamente un producto o descartar las ventas que terminaron en devolución.

        Args:
            year (int): Año seleccionado.
            id_product (int or None, optional): Id de producto. Defaults to None.
            refund_status (bool or None, optional): Filtro de devoluciones. Defaults to None.

        Returns:
            int: Ingresos anuales.
        """
        # Definir fecha de inicio del año y fecha de fin de año para filtros
        year_start= f"{year}-01-01"
        year_end = f"{year}-12-31"
        # Usar función get ventas para obtener datos de ingresos anuales con los filtros
        income = self.calculate_income(start_date=year_start, end_date=year_end,
                                 id_product=id_product, refund_status=refund_status)
        return income


    def get_monthly_sales(self, year: int, id_product: int or None = None, refund_status: bool or None = None) -> dict:
        """ 
        Obtiene el número de ventas de cada mes. Cuenta con algunos filtros opcionales que 
        permiten considerar únicamente un producto o descartar las ventas que terminaron en devolución.
        Las ventas de cada mes se organizan en un diccionario. 

        Args:
            year (int): Año seleccionado.
            id_product (int or None, optional): Id de producto. Defaults to None.
            refund_status (bool or None, optional): Filtro de devoluciones. Defaults to None.

        Returns:
            dict: Número de ventas de cada mes.
        """
        # Inicializa variables
        sales_dict = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0} # month: sales_number_of_month
        # Ciclo for para obtener el número de ventas de cada mes
        for month in range(1,13):
            # Obtener cantidad de dias del mes para saber ultimo día
            month_days = calendar.monthrange(year, month)[1]
            # Definir fecha de inicio del año y fecha de fin de año para filtros
            month_start = f"{year}-{month:02d}-01"
            month_end = f"{year}-{month:02d}-{month_days:02d}"
            # Obtener ventas de ese mes
            sales_dict[month] = self.count_sales(start_date=month_start, end_date=month_end,
                                                 id_product=id_product, refund_status=refund_status)
        return sales_dict

    def get_monthly_income(self, year: int, id_product: int or None = None, refund_status: bool or None = None) -> dict:
        """
        Obtiene los ingresos mensuales. Cuenta con algunos filtros opcionales que permiten
        considerar únicamente un producto o descartar las ventas que terminaron en devolución.
        Las ventas de cada mes se organizan en un diccionario.

        Args:
            year (int): Año seleccionado.
            id_product (int or None, optional): Id de producto. Defaults to None.
            refund_status (bool or None, optional): Filtro de devoluciones. Defaults to None.

        Returns:
            dict: Ingresos de cada mes.
        """
        # Inicializa variables
        income_dict = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0} # month: income_of_month
        # Ciclo for para obtener los ingresos de cada mes
        for month in range(1,13):
            # Obtener cantidad de dias del mes para saber ultimo día
            month_days = calendar.monthrange(year, month)[1]
            # Definir fecha de inicio del año y fecha de fin de año para filtros
            month_start = f"{year}-{month:02d}-01"
            month_end = f"{year}-{month:02d}-{month_days:02d}"
            # Obtener ventas de ese mes
            income_dict[month] = self.calculate_income(start_date=month_start, end_date=month_end,
                                                 id_product=id_product, refund_status=refund_status)
        return income_dict

    def get_products_sales(self, refund_status: bool or None = None,
                           start_date: str or None = None, end_date: str or None = None) -> dict:
        """ 
        Obtiene el número de ventas de cada producto de la tienda.
        Las ventas pueden filtrarse por fechas.
        Las ventas que terminaron en devolución pueden considerarse u omitirse.

        Args:
            refund_status (bool or None, optional): Ventas devueltas (True) o no devueltas (False). Defaults to None.
            start_date (str or None, optional): Fecha de inicio de periodo de ventas considerado. Defaults to None.
            end_date (str or None, optional): Fecha de inicio de periodo de ventas considerado. Defaults to None.
 
        Returns:
            dict: Ventas por producto. El key de cada elemento es el id de producto,
                  mientras que el valor corresponde al número de ventas.
        """
        # Inicializar variables
        products_sales = {}
        # Ciclo for para revisar cada producto diferente de la tabla productos
        for row in lifestore_products.iterrows():
                # Se obtiene id
                id_product = row[1]['id_product']
                # Se cuentan ventas del producto
                sales_number = self.count_sales(id_product=id_product, refund_status=refund_status,
                                                start_date=start_date, end_date=end_date)
                # Se almacena resultado en diccionario
                products_sales[id_product] = sales_number
        return products_sales

    def get_products_searches(self) -> dict:
        """ 
        Obtiene el número de búsquedas de cada producto de la tienda.
        Las búsquedas pueden filtrarse por fechas.
        bLas búsquedas que terminaron en devolución pueden considerarse u omitirse.

        Returns:
            dict: Búsquedas por producto. El key de cada elemento es el id de producto,
                  mientras que el valor corresponde al número de búsquedas.
        """
        # Inicializar variables
        products_searches = {}
        # Ciclo for para revisar cada producto diferente de la tabla productos
        for row in lifestore_products.iterrows():
                # Se obtiene id
                id_product = row[1]['id_product']
                # Se cuentan búsquedas del producto
                searches = self.count_searches(id_product=id_product)
                # Se almacena resultado en diccionario
                products_searches[id_product] = searches
        return products_searches

    def get_product_name(self, id_product: int) -> str:
        """ Obtiene el nombre del producto de la tabla lifestore_products.

        Args:
            id_product (int): ID del producto.

        Returns:
            str: Nombre del producto.
        """
        name = lifestore_products.loc[lifestore_products['id_product']== id_product, 'name'].item()
        return name

    def get_product_stock(self, id_product: int) -> int:
        """ 
        Obtiene la cantidad de unidades de un producto en inventario,
        a partir de la tabla lifestore_products.

        Args:
            id_product (int): ID del producto.

        Returns:
            int: Unidades del producto en inventario.
        """
        stock = lifestore_products.loc[lifestore_products['id_product']== id_product, 'stock'].item()
        return stock

    def get_product_grades(self, reviews_weight:float = 0.6, refunds_weight:float = 0.4,
                           start_date: str or None = None, end_date: str or None = None) -> dict:
        """ 
        Calcula la valoración que tiene los productos vendidos considerando las calificaciones
        de los clientes por cada venta y la cantidad de devoluciones que tiene el producto.
        Para usar ambos factores se asigna cierto peso a cada factor. Estos factores
        cumplen con la siguiente expresión:
        factor_calificaciones + factor_devoluciones = 1 

        Args:
            reviews_weight (float, optional): Factor de calificaciones. Defaults to 0.6.
            refunds_weight (float, optional): Factor de devoluciones. Defaults to 0.4.
            start_date (str or None, optional): Fecha de inicio de periodo de ventas considerado. Defaults to None.
            end_date (str or None, optional): Fecha de inicio de periodo de ventas considerado. Defaults to None.

        Returns:
            dict: Valoración de cada producto. 
        """
        product_grades = {}
        # Ciclo for para revisar cada producto diferente de la tabla productos
        for row in lifestore_products.iterrows():
                # Se obtiene id
                id_product = row[1]['id_product']
                # Para ese id, se obtiene tabla de ventas de producto
                sales_df = self._Filters__filter_sales_df(id_product = id_product, start_date = start_date,
                                                          end_date = end_date)
                # Determinar total de ventas
                total_sales = len(sales_df)
                # Si las ventas son mayores a cero, revisa calificaciones del producto, sino calificación N.D.
                if total_sales > 0:
                    # Caso hay ventas
                    # Obtener puntaje promedio de revisiones de clientes
                    reviews_mean = sales_df["score"].mean()
                    # Se normaliza puntaje de revisiones, valor entre 0 y 1
                    reviews_normalized = (reviews_mean-1)/(5-1)
                    # Contar devoluciones
                    total_refunds = len(sales_df[sales_df["refund"] > 0])
                    # Obtener relación entre productos no devueltos y ventas del producto
                    refunds_pct = 1 - total_refunds/total_sales
                    # Se calcula calificación dandole pesos a las revisiones y a la cantidad de productos no devueltos
                    product_grades[id_product] = round((reviews_weight*reviews_normalized + refunds_weight*refunds_pct)*100, 2)
                else:
                    # Caso no hubo ventas
                    product_grades[id_product] = 'N.D.'
 
        # Obtener subtabla de tabla de ventas con filas que cumplan con los filtros indicados
        return product_grades

    def count_category_products(self) -> dict:
        """
        Cuenta productos existentes en cada categoria.

        Returns:
            dict: Diccionario con conteo de productos de cada categoria. (category: amount_of_products)
        """
        # Inicializar variables
        products_per_category = {}
        # Se identifican las diferentes cateogrias de la tabla de producto
        categories = lifestore_products.category.unique().tolist()
        for category in categories:
            # Filtra tabla de productos por la categoria
            product_df = self._Filters__filter_products_df(category = category)
            # Cuenta elementos en tabla de productos de categoria
            products_per_category[category] = len(product_df)
        return products_per_category
    
    def get_category_sales(self, id_product: int or None = None, refund_status: bool or None = None,
                           start_date: str or None = None, end_date: str or None = None) -> dict:
        """ Clasifica en las diferentes cateogrías de producto las ventas de la empresa.

        Args:
            id_product (int or None, optional): Id de producto. Defaults to None.
            refund_status (bool or None, optional): Ventas devueltas (True) o no devueltas (False). Defaults to None.
            start_date (str or None, optional): Fecha de inicio de periodo de ventas considerado. Defaults to None.
            end_date (str or None, optional): Fecha de inicio de periodo de ventas considerado. Defaults to None.

        Returns:
            dict: Total de ventas por categoría de producto.
        """
        # Inicializar variables
        sales_per_category = {}
        # Se obtienen las ventas de cada producto
        product_sales = self.get_products_sales(refund_status=refund_status, start_date=start_date, end_date=end_date)
        # Se identifican las diferentes cateogrias de la tabla de producto
        categories = lifestore_products.category.unique().tolist()
        for category in categories:
            sales_number = 0
            # Filtra tabla de productos por la categoria
            product_df = self._Filters__filter_products_df(category = category)
            # Se suman las ventas de cada producto en la tabla filtrada
            for row in product_df.iterrows():
                # Se obtiene id
                id_product = row[1]['id_product']
                # Si suman las ventas del producto a ventas de cateogira
                sales_number += product_sales[id_product]
            # Cuenta elementos en tabla de productos de categoria
            sales_per_category[category] = sales_number
        return sales_per_category

    def get_category_income(self, id_product: int or None = None, refund_status: bool or None = None,
                            start_date: str or None = None, end_date: str or None = None) -> dict:
        """ Clasifica en las diferentes cateogrías de producto los ingresos de la empresa.

        Args:
            id_product (int or None, optional): Id de producto. Defaults to None.
            refund_status (bool or None, optional): Ventas devueltas (True) o no devueltas (False). Defaults to None.
            start_date (str or None, optional): Fecha de inicio de periodo de ventas considerado. Defaults to None.
            end_date (str or None, optional): Fecha de inicio de periodo de ventas considerado. Defaults to None.

        Returns:
            dict: Total de ingresos por categoría de producto.
        """
        income_per_category = {}
        # Se identifican las diferentes cateogrias de la tabla de producto
        categories = lifestore_products.category.unique().tolist()
        for category in categories:
            income = 0
            # Filtra tabla de productos por la categoria
            product_df = self._Filters__filter_products_df(category = category)
            # Se suman las ventas de cada producto en la tabla filtrada
            for row in product_df.iterrows():
                # Se obtiene id
                id_product = row[1]['id_product']
                # Se suman los ingresos del producto a las ventas
                income += self.calculate_income(id_product= id_product, refund_status=refund_status,
                                                start_date=start_date, end_date=end_date)
            # Cuenta elementos en tabla de productos de categoria
            income_per_category[category] = income
        return income_per_category
