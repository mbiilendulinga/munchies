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
TOTAL_PRODUCTION = 11173

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

category_lines = {
    "Cereal": [
        "Cereal Line 1",
        "Cereal Line 2"
    ],
    "Snacks": [
        "Snack Line 1",
        "Snack Line 2"
    ]
}

factories = [
    {
        "name": "Munchies Lusaka Factory",
        "city": "Lusaka",
        "weight": 0.50
    },
    {
        "name": "Munchies Central Factory",
        "city": "Kabwe",
        "weight": 0.30
    },
    {
        "name": "Munchies Copperbelt Factory",
        "city": "Ndola",
        "weight": 0.20
    }
]

batch_ranges = {
    "Cereal": (3500, 14000),
    "Snacks": (2500, 11000)
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
                product_status,
                launch_date
            FROM products
        """)

        products = cursor.fetchall()
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

        product_weights_list = [
            product_weights[product_id]
            for product_id in product_ids
        ]

        factory_names = [factory["name"] for factory in factories]
        factory_weights = [factory["weight"] for factory in factories]

        factory_lookup = {
            factory["name"]: factory
            for factory in factories
        }

        production_records = []

        for i in range(TOTAL_PRODUCTION):
            production_id = f"PROD{i + 1:05d}"

            product_id = random.choices(
                product_ids,
                weights=product_weights_list,
                k=1
            )[0]

            product = product_lookup[product_id]

            earliest_date = max(
                START_DATE,
                product["launch_date"]
            )

            days_available = (END_DATE - earliest_date).days

            production_date = earliest_date + timedelta(
                days=random.randint(0, days_available)
            )

            factory_name = random.choices(
                factory_names,
                weights=factory_weights,
                k=1
            )[0]

            factory = factory_lookup[factory_name]

            production_line = random.choice(
                category_lines[product["category"]]
            )

            batch_min, batch_max = batch_ranges[
                product["category"]
            ]

            planned_quantity = random.uniform(
                batch_min,
                batch_max
            )

            planned_quantity = round(planned_quantity)

            production_efficiency = random.uniform(
                0.91,
                1.00
            )

            produced_quantity = round(
                planned_quantity * production_efficiency
            )

            rejection_rate = random.choices(
                [
                    random.uniform(0.002, 0.008),
                    random.uniform(0.008, 0.018),
                    random.uniform(0.018, 0.035),
                    random.uniform(0.035, 0.060)
                ],
                weights=[65, 25, 8, 2],
                k=1
            )[0]

            rejected_quantity = round(
                produced_quantity * rejection_rate
            )

            if rejected_quantity > produced_quantity:
                rejected_quantity = produced_quantity

            cost_variation = random.uniform(
                0.94,
                1.10
            )

            production_cost = round(
                produced_quantity
                * float(product["standard_cost"])
                * cost_variation,
                2
            )

            downtime_hours = round(
                random.choices(
                    [
                        random.uniform(0.0, 0.5),
                        random.uniform(0.5, 1.5),
                        random.uniform(1.5, 3.0),
                        random.uniform(3.0, 6.0)
                    ],
                    weights=[45, 35, 17, 3],
                    k=1
                )[0],
                2
            )

            status_roll = random.random()

            if status_roll < 0.96:
                production_status = "Completed"
            elif status_roll < 0.995:
                production_status = "Completed with Issues"
            else:
                production_status = "Cancelled"

            if production_status == "Cancelled":
                produced_quantity = 0
                rejected_quantity = 0
                production_cost = round(
                    random.uniform(0.05, 0.25)
                    * planned_quantity
                    * float(product["standard_cost"]),
                    2
                )

            production_records.append((
                production_id,
                production_date,
                product_id,
                factory_name,
                factory["city"],
                production_line,
                planned_quantity,
                produced_quantity,
                rejected_quantity,
                production_cost,
                downtime_hours,
                production_status
            ))

        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        cursor = connection.cursor()

        query = """
        INSERT INTO production (
            production_id,
            production_date,
            product_id,
            factory_name,
            factory_city,
            production_line,
            planned_quantity,
            produced_quantity,
            rejected_quantity,
            production_cost,
            downtime_hours,
            production_status
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.executemany(query, production_records)
        connection.commit()

        print(f"Inserted {cursor.rowcount} production records into {DB_NAME}.")
        print("\nSample production records:")

        for production in production_records[:10]:
            print(
                production[0],
                "|",
                production[1],
                "|",
                production[2],
                "|",
                production[3],
                "| Planned:",
                production[6],
                "| Produced:",
                production[7],
                "| Rejected:",
                production[8],
                "| Cost: K",
                production[9],
                "| Downtime:",
                production[10],
                "|",
                production[11]
            )

        cursor.close()
        connection.close()

except Error as e:
    print(f"Database error: {e}")