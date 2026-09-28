import mysql.connector
from mysql.connector import Error
from datetime import date, timedelta
import random

DB_NAME = "munchies"
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "password"

random.seed(2026)

START_DATE = date(2023, 1, 1)
END_DATE = date(2025, 12, 31)
TOTAL_RECORDS = 22718

warehouses = [
    ("Lusaka Central Warehouse", "Distribution Warehouse", "Lusaka", 0.42),
    ("Copperbelt Distribution Warehouse", "Distribution Warehouse", "Ndola", 0.28),
    ("Southern Distribution Warehouse", "Distribution Warehouse", "Choma", 0.17),
    ("Northern Distribution Warehouse", "Distribution Warehouse", "Kasama", 0.13)
]

product_weights = {
    "PROD001": 1.35,
    "PROD002": 1.20,
    "PROD003": 1.15,
    "PROD004": 0.95,
    "PROD005": 1.10,
    "PROD006": 0.95,
    "PROD007": 0.80,
    "PROD008": 0.75,
    "PROD009": 0.70,
    "PROD010": 1.20,
    "PROD011": 0.90,
    "PROD012": 0.85,
    "PROD013": 1.00,
    "PROD014": 0.75,
    "PROD015": 1.05,
    "PROD016": 0.80,
    "PROD017": 0.70
}

try:
    connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    if connection.is_connected():
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                product_id,
                product_name,
                category,
                standard_cost,
                launch_date,
                product_status
            FROM products
        """)

        products = cursor.fetchall()

        cursor.execute("""
            SELECT
                production_date,
                product_id,
                factory_city,
                produced_quantity,
                rejected_quantity,
                production_status
            FROM production
            WHERE production_date BETWEEN %s AND %s
        """, (START_DATE, END_DATE))

        production_records = cursor.fetchall()

        cursor.close()

        product_lookup = {
            product["product_id"]: product
            for product in products
        }

        product_ids = [
            product["product_id"]
            for product in products
            if product["product_status"] == "Active"
        ]

        product_weight_list = [
            product_weights[product_id]
            for product_id in product_ids
        ]

        warehouse_names = [warehouse[0] for warehouse in warehouses]
        warehouse_weights = [warehouse[3] for warehouse in warehouses]

        production_by_product = {}

        for production in production_records:
            product_id = production["product_id"]

            if product_id not in production_by_product:
                production_by_product[product_id] = []

            production_by_product[product_id].append(production)

        production_totals = {}

        for product_id in product_ids:
            production_totals[product_id] = sum(
                max(
                    0,
                    float(record["produced_quantity"])
                    - float(record["rejected_quantity"])
                )
                for record in production_by_product.get(product_id, [])
            )

        selected_combinations = set()
        inventory_records = []

        days_in_period = (END_DATE - START_DATE).days

        while len(inventory_records) < TOTAL_RECORDS:
            product_id = random.choices(
                product_ids,
                weights=product_weight_list,
                k=1
            )[0]

            warehouse_name = random.choices(
                warehouse_names,
                weights=warehouse_weights,
                k=1
            )[0]

            product = product_lookup[product_id]

            earliest_date = max(
                START_DATE,
                product["launch_date"]
            )

            days_available = (END_DATE - earliest_date).days

            snapshot_date = earliest_date + timedelta(
                days=random.randint(0, days_available)
            )

            combination = (
                snapshot_date,
                product_id,
                warehouse_name
            )

            if combination in selected_combinations:
                continue

            selected_combinations.add(combination)

            warehouse = next(
                item for item in warehouses
                if item[0] == warehouse_name
            )

            warehouse_share = warehouse[3]

            total_production = production_totals.get(
                product_id,
                0
            )

            base_stock = (
                total_production
                * warehouse_share
                * random.uniform(0.012, 0.032)
            )

            opening_stock = max(
                0,
                round(base_stock)
            )

            production_received = round(
                total_production
                * warehouse_share
                * random.uniform(0.004, 0.018)
            )

            demand_factor = product_weights[product_id]

            expected_sales = (
                opening_stock
                + production_received
            ) * random.uniform(
                0.25,
                0.65
            ) * min(
                demand_factor,
                1.5
            )

            units_sold = min(
                opening_stock + production_received,
                max(
                    0,
                    round(expected_sales)
                )
            )

            damaged_rate = random.choices(
                [
                    random.uniform(0.001, 0.003),
                    random.uniform(0.003, 0.008),
                    random.uniform(0.008, 0.018)
                ],
                weights=[70, 25, 5],
                k=1
            )[0]

            available_stock = (
                opening_stock
                + production_received
                - units_sold
            )

            damaged_units = min(
                max(0, round(
                    (opening_stock + production_received)
                    * damaged_rate
                )),
                max(0, available_stock)
            )

            closing_stock = (
                opening_stock
                + production_received
                - units_sold
                - damaged_units
            )

            closing_stock = max(
                0,
                round(closing_stock)
            )

            stock_value = round(
                closing_stock
                * float(product["standard_cost"]),
                2
            )

            inventory_id = f"INV{len(inventory_records) + 1:05d}"

            inventory_records.append((
                inventory_id,
                snapshot_date,
                product_id,
                warehouse_name,
                warehouse[1],
                warehouse[2],
                opening_stock,
                production_received,
                units_sold,
                damaged_units,
                closing_stock,
                stock_value
            ))

        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        cursor = connection.cursor()

        query = """
        INSERT INTO inventory (
            inventory_id,
            snapshot_date,
            product_id,
            warehouse_name,
            warehouse_type,
            warehouse_city,
            opening_stock,
            production_received,
            units_sold,
            damaged_units,
            closing_stock,
            stock_value
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.executemany(query, inventory_records)
        connection.commit()

        print(f"Inserted {cursor.rowcount} inventory records into {DB_NAME}.")
        print("\nSample inventory records:")

        for inventory in inventory_records[:10]:
            print(
                inventory[0],
                "|",
                inventory[1],
                "| Product:",
                inventory[2],
                "| Warehouse:",
                inventory[3],
                "| Opening:",
                inventory[6],
                "| Production:",
                inventory[7],
                "| Sold:",
                inventory[8],
                "| Damaged:",
                inventory[9],
                "| Closing:",
                inventory[10],
                "| Value: K",
                inventory[11]
            )

        cursor.close()
        connection.close()

except Error as e:
    print(f"Database error: {e}")