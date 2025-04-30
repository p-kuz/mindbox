from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder.appName("ProductsAndCategories").getOrCreate()

# Таблица продуктов
products = spark.createDataFrame([
    (1, "Apple"),
    (2, "Banana"),
    (3, "Carrot"),
    (4, "Donut")
], ["product_id", "product_name"])

# Таблица категорий
categories = spark.createDataFrame([
    (1, "Fruit"),
    (2, "Vegetable")
], ["category_id", "category_name"])

# Таблица связей между продуктами и категориями
product_category_links = spark.createDataFrame([
    (1, 1),  # Apple -> Fruit
    (2, 1),  # Banana -> Fruit
    (3, 2)   # Carrot -> Vegetable
], ["product_id", "category_id"])

# Получаем пары: продукт - категория
product_category_pairs = product_category_links \
    .join(products, "product_id") \
    .join(categories, "category_id") \
    .select("product_name", "category_name")

# Продукты без категорий
products_without_categories = products \
    .join(product_category_links, "product_id", "left_anti") \
    .select("product_name")

# Результат
print("Пары: Продукт — Категория")
product_category_pairs.show()

print("Продукты без категорий")
products_without_categories.show()
