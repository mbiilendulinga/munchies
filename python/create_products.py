# create_products.py

import mysql.connector
from mysql.connector import Error
from datetime import date


DB_NAME = "munchies"
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "password"


products = [
    # =========================================================
    # CEREALS
    # =========================================================

    {
        "product_id": "PROD001",
        "product_name": "Munchies Original Cornflakes",
        "category": "Cereal",
        "subcategory": "Cornflakes",
        "brand": "Munchies",
        "pack_size_g": 500,
        "unit_of_measure": "Pack",
        "unit_price": 48.50,
        "standard_cost": 31.20,
        "launch_date": date(2022, 1, 15),
        "product_status": "Active"
    },

    {
        "product_id": "PROD002",
        "product_name": "Munchies Honey Cornflakes",
        "category": "Cereal",
        "subcategory": "Cornflakes",
        "brand": "Munchies",
        "pack_size_g": 500,
        "unit_of_measure": "Pack",
        "unit_price": 55.00,
        "standard_cost": 35.80,
        "launch_date": date(2022, 2, 22),
        "product_status": "Active"
    },

    {
        "product_id": "PROD003",
        "product_name": "Munchies Bran Flakes",
        "category": "Cereal",
        "subcategory": "Bran Flakes",
        "brand": "Munchies",
        "pack_size_g": 500,
        "unit_of_measure": "Pack",
        "unit_price": 52.50,
        "standard_cost": 34.10,
        "launch_date": date(2022, 3, 18),
        "product_status": "Active"
    },

    {
        "product_id": "PROD004",
        "product_name": "Munchies Honey Bran Flakes",
        "category": "Cereal",
        "subcategory": "Bran Flakes",
        "brand": "Munchies",
        "pack_size_g": 500,
        "unit_of_measure": "Pack",
        "unit_price": 59.50,
        "standard_cost": 38.90,
        "launch_date": date(2022, 4, 27),
        "product_status": "Active"
    },

    {
        "product_id": "PROD005",
        "product_name": "Munchies Original Wheat Cereal",
        "category": "Cereal",
        "subcategory": "Wheat Cereal",
        "brand": "Munchies",
        "pack_size_g": 500,
        "unit_of_measure": "Pack",
        "unit_price": 54.00,
        "standard_cost": 36.40,
        "launch_date": date(2022, 5, 13),
        "product_status": "Active"
    },

    {
        "product_id": "PROD006",
        "product_name": "Munchies Chocolate Wheat Cereal",
        "category": "Cereal",
        "subcategory": "Wheat Cereal",
        "brand": "Munchies",
        "pack_size_g": 500,
        "unit_of_measure": "Pack",
        "unit_price": 62.00,
        "standard_cost": 40.50,
        "launch_date": date(2022, 6, 21),
        "product_status": "Active"
    },

    {
        "product_id": "PROD007",
        "product_name": "Munchies Strawberry Crunch",
        "category": "Cereal",
        "subcategory": "Crunch",
        "brand": "Munchies",
        "pack_size_g": 500,
        "unit_of_measure": "Pack",
        "unit_price": 64.50,
        "standard_cost": 42.30,
        "launch_date": date(2022, 7, 8),
        "product_status": "Active"
    },

    {
        "product_id": "PROD008",
        "product_name": "Munchies Banana Crunch",
        "category": "Cereal",
        "subcategory": "Crunch",
        "brand": "Munchies",
        "pack_size_g": 500,
        "unit_of_measure": "Pack",
        "unit_price": 63.00,
        "standard_cost": 41.70,
        "launch_date": date(2022, 8, 19),
        "product_status": "Active"
    },

    {
        "product_id": "PROD009",
        "product_name": "Munchies Chocolate Crunch",
        "category": "Cereal",
        "subcategory": "Crunch",
        "brand": "Munchies",
        "pack_size_g": 500,
        "unit_of_measure": "Pack",
        "unit_price": 67.50,
        "standard_cost": 44.20,
        "launch_date": date(2022, 9, 16),
        "product_status": "Active"
    },

    # =========================================================
    # SNACKS
    # =========================================================

    {
        "product_id": "PROD010",
        "product_name": "Munchies Potato Crisps Original",
        "category": "Snacks",
        "subcategory": "Potato Crisps",
        "brand": "Munchies",
        "pack_size_g": 100,
        "unit_of_measure": "Pack",
        "unit_price": 15.00,
        "standard_cost": 8.40,
        "launch_date": date(2022, 1, 29),
        "product_status": "Active"
    },

    {
        "product_id": "PROD011",
        "product_name": "Munchies Potato Crisps Chilli",
        "category": "Snacks",
        "subcategory": "Potato Crisps",
        "brand": "Munchies",
        "pack_size_g": 100,
        "unit_of_measure": "Pack",
        "unit_price": 16.50,
        "standard_cost": 9.10,
        "launch_date": date(2022, 3, 11),
        "product_status": "Active"
    },

    {
        "product_id": "PROD012",
        "product_name": "Munchies Potato Crisps Cheese & Onion",
        "category": "Snacks",
        "subcategory": "Potato Crisps",
        "brand": "Munchies",
        "pack_size_g": 100,
        "unit_of_measure": "Pack",
        "unit_price": 17.00,
        "standard_cost": 9.60,
        "launch_date": date(2022, 5, 6),
        "product_status": "Active"
    },

    {
        "product_id": "PROD013",
        "product_name": "Munchies Salted Peanuts",
        "category": "Snacks",
        "subcategory": "Peanuts",
        "brand": "Munchies",
        "pack_size_g": 100,
        "unit_of_measure": "Pack",
        "unit_price": 18.00,
        "standard_cost": 10.20,
        "launch_date": date(2022, 6, 17),
        "product_status": "Active"
    },

    {
        "product_id": "PROD014",
        "product_name": "Munchies Honey Roasted Peanuts",
        "category": "Snacks",
        "subcategory": "Peanuts",
        "brand": "Munchies",
        "pack_size_g": 100,
        "unit_of_measure": "Pack",
        "unit_price": 21.50,
        "standard_cost": 12.40,
        "launch_date": date(2022, 8, 5),
        "product_status": "Active"
    },

    {
        "product_id": "PROD015",
        "product_name": "Munchies Chocolate Biscuits",
        "category": "Snacks",
        "subcategory": "Biscuits",
        "brand": "Munchies",
        "pack_size_g": 120,
        "unit_of_measure": "Pack",
        "unit_price": 19.50,
        "standard_cost": 11.30,
        "launch_date": date(2022, 9, 23),
        "product_status": "Active"
    },

    {
        "product_id": "PROD016",
        "product_name": "Munchies Coconut Biscuits",
        "category": "Snacks",
        "subcategory": "Biscuits",
        "brand": "Munchies",
        "pack_size_g": 120,
        "unit_of_measure": "Pack",
        "unit_price": 18.50,
        "standard_cost": 10.80,
        "launch_date": date(2022, 10, 14),
        "product_status": "Active"
    },

    {
        "product_id": "PROD017",
        "product_name": "Munchies Cream Biscuits",
        "category": "Snacks",
        "subcategory": "Biscuits",
        "brand": "Munchies",
        "pack_size_g": 120,
        "unit_of_measure": "Pack",
        "unit_price": 20.00,
        "standard_cost": 11.70,
        "launch_date": date(2022, 11, 26),
        "product_status": "Active"
    }
]


def create_products():
    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=DB_NAME
        )

        if connection.is_connected():
            print("Connected to Munchies database.")

            cursor = connection.cursor()

            insert_query = """
                INSERT INTO products (
                    product_id,
                    product_name,
                    category,
                    subcategory,
                    brand,
                    pack_size_g,
                    unit_of_measure,
                    unit_price,
                    standard_cost,
                    launch_date,
                    product_status
                )
                VALUES (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s
                )
            """

            values = [
                (
                    p["product_id"],
                    p["product_name"],
                    p["category"],
                    p["subcategory"],
                    p["brand"],
                    p["pack_size_g"],
                    p["unit_of_measure"],
                    p["unit_price"],
                    p["standard_cost"],
                    p["launch_date"],
                    p["product_status"]
                )
                for p in products
            ]

            cursor.executemany(insert_query, values)
            connection.commit()

            print(f"Successfully inserted {cursor.rowcount} products.")

            cursor.execute("""
                SELECT
                    product_id,
                    product_name,
                    category,
                    subcategory,
                    pack_size_g,
                    unit_price,
                    standard_cost,
                    launch_date
                FROM products
                ORDER BY product_id
            """)

            rows = cursor.fetchall()

            print("\nProducts in database:")
            print("-" * 125)

            for row in rows:
                print(
                    f"{row[0]:<10} | "
                    f"{row[1]:<38} | "
                    f"{row[2]:<10} | "
                    f"{row[3]:<16} | "
                    f"{row[4]:>6}g | "
                    f"K{row[5]:>7.2f} | "
                    f"K{row[6]:>7.2f} | "
                    f"{row[7]}"
                )

            print("-" * 125)

    except Error as e:
        print(f"Database error: {e}")

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()
            print("\nDatabase connection closed.")


if __name__ == "__main__":
    create_products()