from processing.lifestore_tables import lifestore_products, lifestore_sales, lifestore_searches

class TimeServices():
    def sales_per_year(self, year:int, exclude_refunds:bool=False, product_id:int or None = None) -> int:
        """ Se calcula los retornos del producto al año. Opcionalmente se puede filtrar
            los resultados para un producto especifico. Se puede ignorar tambien las ventas 
            que terminaron en devolución.

        Args:
            year (int): Año analizado.
            exclude_refunds (bool, optional): Bool para descontar devoluciones del numero de ventas. 
                                              Defaults to False.
            product_id (int or NoneType, optional): Id de producto. Defaults to None.

        Returns:
            int: Numero de ventas anuales.
        """

        # Regresa una tabla con un filtro de año
        year_sales_df = lifestore_sales[lifestore_sales["date"].dt.year == year]

        # Descontar devoluciones de la tabla de ventas anuales si exclude_refunds es True
        if exclude_refunds:
            year_sales_df=year_sales_df[lifestore_sales["refund"] == 0]

        # Si se incluyo un id_product en la solicitud, filtra la tabla generada ahora por producto
        if product_id is not None:
            year_sales_df=year_sales_df[lifestore_sales["id_product"] == product_id]
        # Conunt sales after filter
        sales_number = len(year_sales_df)
        return sales_number

    def income_per_year(self, year:int, exclude_refunds:bool=False, product_id:int or None = None) -> int or float:
        """ Se calculan los ingresos de un año. Opcionalmente se puede filtrar los resultados
            para un producto especifico. Se puede ignorar las ventas que terminaron en devolución.

        Args:
            year (int): Año analizado.
            exclude_refunds (bool, optional): Bool para descontar devoluciones del numero de ventas. 
                                              Defaults to False.
            product_id (int or NoneType, optional): Id de producto. Defaults to None.

        Returns:
            int or float: Ingresos anuales.

        """

        # Inicializa Ingreso
        income = 0
        # Si se incluyo un id_product en la solicitud, filtra la tabla generada ahora por producto
        if product_id is not None:
             product_sales = self.sales_per_year(year, exclude_refunds, product_id)
             income = product_sales * lifestore_products["price"][lifestore_products["id_product"] == product_id].item()
        # Si no se indico id_product, se itera cada id, y se suman los ingresos de cada producto diferente 
        else:
            for row in lifestore_products.iterrows():
                # Se obtiene id
                product_id = row[1]['id_product']
                # Se cuentan ventas del producto
                product_sales = self.sales_per_year(year, exclude_refunds, product_id)
                # Se suman los ingresos del producto a los ingresos totales
                income += product_sales * lifestore_products["price"][lifestore_products["id_product"] == product_id].item()
        return income
