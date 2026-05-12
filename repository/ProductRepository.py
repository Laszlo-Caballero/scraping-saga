import aiosqlite
from model.product import Product
import json
from utils.utils import singleton

@singleton()
class ProductRepository:

    def __init__(self):
        self.db_path = "products.db"

    async def create_table(self):

        async with aiosqlite.connect(self.db_path) as db:

            await db.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    price TEXT,
                    buy_by TEXT,
                    images TEXT,
                    brand TEXT,
                    url TEXT,
                    caracteristics TEXT,
                    spects TEXT,
                    category TEXT,
                    sub_category TEXT,
                    errors TEXT,
                    especific_errors TEXT
                )
            """)

            await db.commit()

    async def insert_product(self, product: Product):

        async with aiosqlite.connect(self.db_path) as db:

            await db.execute("""
                INSERT INTO products (
                    name,
                    price,
                    buy_by,
                    brand,
                    url,
                    caracteristics,
                    spects,
                    category,
                    sub_category,
                    errors,
                    especific_errors,
                    images
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                product.name,
                json.dumps(product.price),
                product.buy_by,
                product.brand,
                product.url,
                json.dumps(product.caracteristics),
                json.dumps(product.spects),
                product.category,
                product.sub_category,
                product.error,
                json.dumps(product.especific_error),
                json.dumps(product.images)
            ))

            await db.commit()

    async def update_product(
        self,
        product: Product
    ):

        async with aiosqlite.connect(self.db_path) as db:

            await db.execute("""
                UPDATE products
                SET
                    name = ?,
                    price = ?,
                    buy_by = ?,
                    brand = ?,
                    url = ?,
                    caracteristics = ?,
                    spects = ?,
                    category = ?,
                    sub_category = ?,
                    errors = ?,
                    especific_errors = ?,
                    images = ?
                WHERE id = ?
            """, (
                product.name,
                json.dumps(product.price),
                product.buy_by,
                product.brand,
                product.url,
                json.dumps(product.caracteristics),
                json.dumps(product.spects),
                product.category,
                product.sub_category,
                product.error,
                json.dumps(product.especific_error),
                json.dumps(product.images),
                product.id
            ))

            await db.commit()

    async def get_products(self) -> list[Product]:

        async with aiosqlite.connect(self.db_path) as db:

            cursor = await db.execute(
                "SELECT * FROM products"
            )

            rows = await cursor.fetchall()

            products = []

            for row in rows:

                product = Product(
                    id=row[0],
                    name=row[1],
                    price=json.loads(row[2]),
                    buy_by=row[3],
                    images = json.loads(row[4]),
                    brand=row[5],
                    url=row[6],
                    caracteristics=json.loads(row[7]),
                    spects=json.loads(row[8]),
                    category=row[9],
                    sub_category=row[10],
                    error=row[11],
                    especific_error=json.loads(row[12])
                )

                products.append(product)

            return products