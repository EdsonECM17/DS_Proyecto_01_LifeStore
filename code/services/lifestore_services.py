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
            refund_status (bool or None, optional):  Ventas devueltas (True) o no devluetas (False). Defaults to None.

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
            refund_status (bool or None, optional):  Ventas devueltas (True) o no devluetas (False). Defaults to None.

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