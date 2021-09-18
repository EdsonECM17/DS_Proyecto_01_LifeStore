import calendar

from processing.lifestore_tables import lifestore_products, lifestore_sales, lifestore_searches
from processing.filters_df import Filters


class Service(Filters):
    """ Clase que agrupa diversas operaciones de cosulta de los datos de LifeStore, para apoyar
        el analisis de información.
        Esta clase es hija de la clase Filters, por lo que tiene acesso a sus métodos. 
    """
    def get_sales_number(self, id_product: int or None = None, start_date: str or None = None,
                         end_date: str or None = None, score_min: int or None = None,
                         score_max: int or None = None, refund_status: bool or None = None) -> int:
        """ Consulta la tabla de ventas con una serie de filtros de producto y/o tiempo, extrayendo
            solo las filas de interes. Mediante un conteo de las ventas que cumplen con las condiciones
            del caso, se determina el numero de ventas.

        Args:
            id_product (int or None, optional): Id de producto. Defaults to None.
            start_date (str or None, optional): Fecha de inicio de periodo de ventas considerado. Defaults to None.
            end_date (str or None, optional): Fecha de inicio de periodo de ventas considerado. Defaults to None.
            score_min (int or None, optional): Calificación minima de venta. Defaults to None.
            score_max (int or None, optional): Calificación maxima de venta. Defaults to None.
            refund_status (bool or None, optional): Ventas devueltas (True) o no devluetas (False). Defaults to None.

        Returns:
            int: Numero de ventas que tuvo el caso solicitado.
        """
        # Obtener subtabla de tabla de ventas con filas que cumplan con los filtros indicados
        sales_df = self._Filters__filter_sales_df(id_product = id_product, start_date = start_date,
                                                  end_date = end_date, refund = refund_status,
                                                  score_min = score_min, score_max = score_max)
       # Contar ventas mediante el numero de filas de la tabla filtrada
        sales_number = len(sales_df)
        return sales_number

    def get_income(self, id_product: int or None = None, start_date: str or None = None,
                   end_date: str or None = None, score_min: int or None = None,
                   score_max: int or None = None, refund_status: bool or None = None) -> int:
        """ Obtiene el total de ingresos para un producto especifico o todos los productos
            que cumplan con los filtros en las entradas.

        Args:
            id_product (int or None, optional): Id de producto. Defaults to None.
            start_date (str or None, optional): Fecha de inicio de periodo de ventas considerado. Defaults to None.
            end_date (str or None, optional): Fecha de inicio de periodo de ventas considerado. Defaults to None.
            score_min (int or None, optional): Calificación minima de venta. Defaults to None.
            score_max (int or None, optional): Calificación maxima de venta. Defaults to None.
            refund_status (bool or None, optional): Ventas devueltas (True) o no devluetas (False). Defaults to None.

        Returns:
            int: Total de ingresos para caso solicitado.
        """
        income = 0
        # Si se incluyo un id_product en la solicitud, filtra la tabla generada ahora por producto
        if id_product is not None:
            product_sales = self.get_sales_number(id_product, start_date, end_date, score_min,
                                                  score_max, refund_status)
            income = product_sales * lifestore_products["price"][lifestore_products["id_product"] == id_product].item()
        # Si no se indico id_product, se itera cada id, y se suman los ingresos de cada producto diferente 
        else:
            for row in lifestore_products.iterrows():
                # Se obtiene id
                id_product = row[1]['id_product']
                # Se cuentan ventas del producto
                product_sales = self.get_sales_number(id_product, start_date, end_date, score_min,
                                                      score_max, refund_status)
                # Se suman los ingresos del producto a los ingresos totales
                income += product_sales * lifestore_products["price"][lifestore_products["id_product"] == id_product].item()
        return income

    def get_searches_number(self, id_product: int or None):
        """ Consulta la tabla de busquedas con un filtro de producto y cuenta la cantidad
            de busquedas que cumplan con las condiciones indicadas.

        Args:
            id_product (int or None, optional): Id de producto. Defaults to None.

        Returns:
            int: Numero de busquedas que tuvo el caso solicitado.
        """
        # Obtener tabla de busquedas filtrada. Si no hay filtro, se obtiene completa. 
        searches_df = self._Filters__filter_searches_df(id_product = id_product)
        # Contar busquedas
        searches_number = len(searches_df)
        return searches_number

    def year_sales(self, year:int, id_product: int or None = None, refund_status: bool or None = None) -> int:
        """ Obtiene el número de ventas anuales. Cuenta con algunos filtros opcionales que permiten
            considerar unicamente un producto o descartar las ventas que terminaron en devolución.

        Args:
            year (int): Año seleccionado.
            id_product (int or None, optional): Id de producto. Defaults to None.
            refund_status (bool or None, optional): Filtro de devoluciones. Defaults to None.

        Returns:
            int: Número de ventas anuales
        """
        # Definir fecha de inicio del año y fecha de fin de año para filtros
        year_start= f"{year}-01-01"
        year_end = f"{year}-12-31"
        # Usar función get ventas para obtener datos de ventas anuales con los filtros
        sales_number = self.get_sales_number(start_date=year_start, end_date=year_end,
                                             id_product=id_product, refund_status=refund_status)
        return sales_number
    
    def year_income(self, year:int, id_product: int or None = None, refund_status: bool or None = None) -> int:
        """ Obtiene los ingresos anuales. Cuenta con algunos filtros opcionales que permiten
            considerar unicamente un producto o descartar las ventas que terminaron en devolución.

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
        income = self.get_income(start_date=year_start, end_date=year_end,
                                 id_product=id_product, refund_status=refund_status)
        return income


    def month_sales(self, year: int, id_product: int or None = None, refund_status: bool or None = None) -> dict:
        """ Obtiene el número de ventas de cada mes. Cuenta con algunos filtros opcionales que permiten
            considerar unicamente un producto o descartar las ventas que terminaron en devolución.
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
        # Ciclo for para obtener el numero de ventas de cada mes
        for month in range(1,13):
            # Obtener cantidad de dias del mes para saber ultimo dia
            month_days = calendar.monthrange(year, month)[1]
            # Definir fecha de inicio del año y fecha de fin de año para filtros
            month_start = f"{year}-{month:02d}-01"
            month_end = f"{year}-{month:02d}-{month_days:02d}"
            # Obtener ventas de ese mes
            sales_dict[month] = self.get_sales_number(start_date=month_start, end_date=month_end,
                                                      id_product=id_product, refund_status=refund_status)

        return sales_dict
        

    def month_income(self, year: int, id_product: int or None = None, refund_status: bool or None = None) -> dict:
        """ Obtiene los ingresos mensuales. Cuenta con algunos filtros opcionales que permiten
            considerar unicamente un producto o descartar las ventas que terminaron en devolución.
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
            # Obtener cantidad de dias del mes para saber ultimo dia
            month_days = calendar.monthrange(year, month)[1]
            # Definir fecha de inicio del año y fecha de fin de año para filtros
            month_start = f"{year}-{month:02d}-01"
            month_end = f"{year}-{month:02d}-{month_days:02d}"
            # Obtener ventas de ese mes
            income_dict[month] = self.get_income(start_date=month_start, end_date=month_end,
                                                 id_product=id_product, refund_status=refund_status)
        return income_dict