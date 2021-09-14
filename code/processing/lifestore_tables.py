import pandas as pd

import data.lifestore_file as lifestore

# Create dataframe of searches
lifestore_searches = pd.DataFrame(lifestore.lifestore_searches, columns = ["id_search", "id_product"])

# Create dataframe of sales
lifestore_sales = pd.DataFrame(lifestore.lifestore_sales, columns = ["id_sale", "id_product", "score", "date", "refund"])
lifestore_sales["date"] = pd.to_datetime(lifestore_sales["date"])
# Clean data to include only data from year (2020)
lifestore_sales = lifestore_sales[lifestore_sales["date"]>="1/1/2020"]

# Create dataframe of products
lifestore_products = pd.DataFrame(lifestore.lifestore_products, columns = ["id_product", "name", "price", "category", "stock"])


