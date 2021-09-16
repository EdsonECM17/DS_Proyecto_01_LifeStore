from pandas.core.frame import DataFrame

from processing.lifestore_tables import lifestore_products, lifestore_sales, lifestore_searches


class Filters():
    """Clase que permite filtrar los dataframes generados a partir de los datos de entrada,
       para optimizar los servicios de consulta de información especifica del programa.
    """
    def filter_products_df(id_product: int or None = None, category: str or None = None,
                           name: str or None = None, price_min: int or None = None,
                           price_max: int or None = None, stock_min: int or None = None,
                           stock_max: int or None = None) -> DataFrame:
        """Filtra el dataframe de productos de acuerdo a valores en las columnas que tiene
           la tabla generada. Si no hay filtro, se regresa un dataframe completo.

        Args:
            id_product (int or None, optional): Id de producto. Defaults to None.
            category (str or None, optional): Categoria de producto. Defaults to None.
            name (str or None, optional): Nombre del producto. Defaults to None.
            price_min (int or None, optional): Precio minimo de producto. Defaults to None.
            price_max (int or None, optional): Precio maximo de producto. Defaults to None.
            stock_min (int or None, optional): Inventario minimo de producto. Defaults to None.
            stock_max (int or None, optional): Inventario maximo de producto. Defaults to None.

        Returns:
            DataFrame: Dataframe con columnas de la tabla que cumplen con los filtros indicados.
        """
        product_df = lifestore_products
        # Incluir filtro por id de producto si existe
        if id_product is not None:
            product_df=product_df[product_df["id_product"] == id_product]
        # Incluir filtro por categoria de producto si existe
        if category is not None:
            product_df=product_df[product_df["category"] == category]
        # Incluir filtro por nombre de producto si existe
        if name is not None:
            product_df=product_df[product_df["name"] == name]
        # Incluir filtro por precio si existe
        if price_min is not None:
            product_df=product_df[product_df["price"] >= price_min]
        if price_max is not None:
            product_df=product_df[product_df["price"] <= price_max]
        # Incluir filtro por stock si existe
        if price_min is not None:
            product_df=product_df[product_df["stock"] >= stock_min]
        if price_max is not None:
            product_df=product_df[product_df["stock"] <= stock_max]

        return product_df


    def filter_sales_df(id_sale: int or None = None, id_product: int or None = None,
                        score_min: int or None = None, score_max: int or None = None,
                        start_date: str or None = None, end_date: str or None = None,
                        refund: bool or None = None) -> DataFrame:
        """Filtra el dataframe de ventas de acuerdo a valores en las columnas que tiene
           la tabla generada. Si no hay filtro, se regresa un dataframe completo.

        Args:
            id_sale (int or None, optional): Id de venta. Defaults to None.
            id_product (int or None, optional): Id de producto. Defaults to None.
            score_min (int or None, optional): Calificación minima de venta. Defaults to None.
            score_max (int or None, optional): Calificación maxima de venta. Defaults to None.
            start_date (str or None, optional): Fecha de inicio de periodo de ventas considerado. Defaults to None.
            end_date (str or None, optional): Fecha de inicio de periodo de ventas considerado. Defaults to None.
            refund (bool or None, optional):  Ventas devueltas (True) o no devluetas (False). Defaults to None.

        Returns:
            DataFrame: Dataframe con columnas de la tabla que cumplen con los filtros indicados.
        """
        sales_df = lifestore_sales
        # Incluir filtro por id de venta si existe
        if id_sale is not None:
            sales_df=sales_df[sales_df["id_sale"] == id_sale]
        # Incluir filtro por id de producto si existe
        if id_product is not None:
            sales_df=sales_df[sales_df["id_product"] == id_product]
        # Incluir filtro por calificacion si existe
        if score_min is not None:
            sales_df=sales_df[sales_df["score"] >= score_min]
        if score_max is not None:
            sales_df=sales_df[sales_df["score"] <= score_max]
        # Incluir filtro por fechas si existe
        if start_date is not None:
            sales_df=sales_df[sales_df["date"] >= start_date]
        if end_date is not None:
            sales_df=sales_df[sales_df["date"] <= end_date]
        # Incluir filtro por devoluciones si existe
        if refund is not None:
            sales_df=sales_df[sales_df["refund"] == int(refund)]

        return sales_df


    def filter_searches_df(id_search: int or None = None, id_product: int or None = None) -> DataFrame:
        """Filtra el dataframe de busquedas de acuerdo a valores en las columnas que tiene
           la tabla generada. Si no hay filtro, se regresa un dataframe completo.

        Args:
            id_search (int or None, optional): Id de busqueda. Defaults to None.
            id_product (int or None, optional): Id de producto. Defaults to None.

        Returns:
            DataFrame: Dataframe con columnas de la tabla que cumplen con los filtros indicados.
        """
        searches_df = lifestore_searches
        # Incluir filtro por id de busqueda si existe
        if id_search is not None:
            searches_df=searches_df[searches_df["id_search"] == id_search]
        # Incluir filtro por id de producto si existe
        if id_product is not None:
            searches_df=searches_df[searches_df["id_product"] == id_product]

        return searches_df