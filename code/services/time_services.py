from processing.lifestore_tables import lifestore_products, lifestore_sales, lifestore_searches

class TimeServices():
    def sales_per_time(self, year:int, month: int or None = None,
                       exclude_refunds:bool=False, product_id:int or None = None) -> int:
        """ Se calcula el numero de ventas del producto en un año o mes especifico.
            Si se desea el año entero, se omite la variable month.
            Opcionalmente se puede filtrar los resultados para un producto especifico.
            Se puede ignorar tambien las ventas que terminaron en devolución.

        Args:
            year (int): Año analizado.
            month (int or None, optional): Mes especifico deseado. Defaults to None.
            exclude_refunds (bool, optional): Bool para descontar devoluciones del numero de ventas. 
                                              Defaults to False.
            product_id (int or NoneType, optional): Id de producto. Defaults to None.

        Returns:
            int: Numero de ventas en el periodo solicitado.
        """

        # Regresa una tabla con un filtro de año
        sales_df = lifestore_sales[lifestore_sales["date"].dt.year == year]
        
        # Filtra tabla por mes si se indica mes en variable month
        if month is not None:
            # Validar valor de mes
            if  0 < month < 13:
                sales_df=sales_df[sales_df["date"].dt.month == month]
            else:
                return 0
        
        # Descontar devoluciones de la tabla de ventas anuales si exclude_refunds es True
        if exclude_refunds:
            sales_df=sales_df[sales_df["refund"] == 0]

        # Si se incluyo un id_product en la solicitud, filtra la tabla generada ahora por producto
        if product_id is not None:
            sales_df=sales_df[sales_df["id_product"] == product_id]
        # Conunt sales after filter
        sales_number = len(sales_df)
        return sales_number

    def income_per_time(self, year:int, month: int or None = None,
                        exclude_refunds:bool=False, product_id:int or None = None) -> int or float:
        """ Se calculan los ingresos del producto en un año o mes especifico.
            Si se desea el año entero, se omite la variable month.
            Opcionalmente se puede filtrar los resultados para un producto especifico.
            Se puede ignorar tambien las ventas que terminaron en devolución.

        Args:
            year (int): Año analizado.
            month (int or None, optional): Mes especifico deseado. Defaults to None.
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
             product_sales = self.sales_per_time(year, month, exclude_refunds, product_id)
             income = product_sales * lifestore_products["price"][lifestore_products["id_product"] == product_id].item()
        # Si no se indico id_product, se itera cada id, y se suman los ingresos de cada producto diferente 
        else:
            for row in lifestore_products.iterrows():
                # Se obtiene id
                product_id = row[1]['id_product']
                # Se cuentan ventas del producto
                product_sales = self.sales_per_time(year, month, exclude_refunds, product_id)
                # Se suman los ingresos del producto a los ingresos totales
                income += product_sales * lifestore_products["price"][lifestore_products["id_product"] == product_id].item()
        return income
