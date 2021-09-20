"""
LIFESTORE_DATA_FRAMES

Este script convierte las listas de datos de entrada  en data/filestore_file.py
a DataFrames, para optimizar su manipulación. Los nombres de las columnas de
cada tabla se asignaron de acuerdo a la documentación de ese script.

Este modulo incluye el siguiente procesamiento: 
     - En la datos de ventas, se conservan solo los pertenecientes al 
       año de interes (2020).

"""

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
