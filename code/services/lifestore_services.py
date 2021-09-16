from processing.lifestore_tables import lifestore_products, lifestore_sales, lifestore_searches
from processing.filters_df import Filters

class Service(Filters):
    def get_sales_number(self, id_product: int or None = None, start_date: str or None = None,
                         end_date: str or None = None, score_min: int or None = None,
                         score_max: int or None = None, refund_status: bool or None = None) -> int:
        sales_df = self._Filters__filter_sales_df(id_product = id_product, start_date = start_date,
                                                  end_date = end_date, refund = refund_status,
                                                  score_min = score_min, score_max = score_max)
        sales_number = len(sales_df)
        return sales_number

    def get_income(self, id_product: int or None = None, start_date: str or None = None,
                   end_date: str or None = None, score_min: int or None = None,
                   score_max: int or None = None, refund_status: bool or None = None) -> int:
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