import mysql.connector
from mysql.connector import Error
from datetime import timedelta
import random

DB_NAME = "munchies"
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "password"

TARGET_ROWS = 31684

random.seed(2026)

try:
    connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            s.sale_id,
            s.sale_date,
            s.customer_id,
            s.product_id,
            s.quantity,
            s.invoice_status,
            c.customer_type,
            c.region
        FROM sales s
        JOIN customers c
            ON s.customer_id = c.customer_id
        WHERE s.invoice_status != 'Cancelled'
    """)

    sales = cursor.fetchall()

    if not sales:
        raise Exception("No eligible sales found.")

    delivery_candidates = []

    customer_delivery_weights = {
        "Supermarket": 1.00,
        "Wholesaler": 0.95,
        "Distributor": 0.90,
        "Retailer": 0.55,
        "Convenience Store": 0.35
    }

    region_distance_ranges = {
        "Lusaka": (8, 85),
        "Copperbelt": (10, 120),
        "Central": (20, 180),
        "Southern": (40, 260),
        "Eastern": (50, 320),
        "Northern": (80, 420),
        "Luapula": (120, 480),
        "Western": (180, 600),
        "North-Western": (100, 500)
    }

    for sale in sales:
        weight = customer_delivery_weights.get(
            sale["customer_type"],
            0.50
        )

        if random.random() < weight:
            delivery_candidates.append(sale)

    if len(delivery_candidates) < TARGET_ROWS:
        delivery_candidates = sales

    selected_sales = random.sample(
        delivery_candidates,
        min(TARGET_ROWS, len(delivery_candidates))
    )

    rows = []

    delivery_statuses = [
        "Delivered",
        "Delivered",
        "Delivered",
        "Delivered",
        "Delivered",
        "Delivered",
        "Late",
        "Late",
        "Partially Delivered",
        "Failed Delivery",
        "In Transit"
    ]

    for i, sale in enumerate(selected_sales, start=1):

        sale_quantity = float(sale["quantity"])

        shipment_date = sale["sale_date"] + timedelta(
            days=random.randint(0, 3)
        )

        status = random.choices(
            delivery_statuses,
            weights=[55, 55, 55, 55, 55, 55, 10, 8, 7, 3, 7],
            k=1
        )[0]

        if status == "Delivered":
            delivery_days = random.choices(
                [1, 2, 3, 4, 5],
                weights=[20, 40, 25, 10, 5],
                k=1
            )[0]

            delivery_date = shipment_date + timedelta(
                days=delivery_days
            )

            quantity_shipped = round(
                sale_quantity *
                random.uniform(0.96, 1.00)
            )

        elif status == "Late":
            delivery_days = random.randint(5, 12)

            delivery_date = shipment_date + timedelta(
                days=delivery_days
            )

            quantity_shipped = round(
                sale_quantity *
                random.uniform(0.90, 1.00)
            )

        elif status == "Partially Delivered":
            delivery_days = random.randint(2, 8)

            delivery_date = shipment_date + timedelta(
                days=delivery_days
            )

            quantity_shipped = round(
                sale_quantity *
                random.uniform(0.45, 0.89)
            )

        elif status == "Failed Delivery":
            delivery_date = None

            quantity_shipped = round(
                sale_quantity *
                random.uniform(0.00, 0.25)
            )

        else:
            delivery_date = None

            quantity_shipped = round(
                sale_quantity *
                random.uniform(0.20, 0.80)
            )

        if quantity_shipped < 0:
            quantity_shipped = 0

        min_distance, max_distance = region_distance_ranges.get(
            sale["region"],
            (20, 300)
        )

        distance_km = round(
            random.uniform(
                min_distance,
                max_distance
            ),
            2
        )

        base_delivery_cost = (
            180 +
            (distance_km * random.uniform(2.20, 4.20))
        )

        quantity_factor = max(
            1,
            quantity_shipped / 100
        )

        delivery_cost = round(
            base_delivery_cost *
            (0.85 + quantity_factor * 0.15),
            2
        )

        delivery_id = f"DEL{i:05d}"

        rows.append((
            delivery_id,
            sale["sale_id"],
            sale["customer_id"],
            sale["product_id"],
            shipment_date,
            delivery_date,
            quantity_shipped,
            status,
            delivery_cost,
            distance_km
        ))

        if len(rows) >= 5000:
            cursor.executemany("""
                INSERT INTO deliveries (
                    delivery_id,
                    sale_id,
                    customer_id,
                    product_id,
                    shipment_date,
                    delivery_date,
                    quantity_shipped,
                    delivery_status,
                    delivery_cost,
                    distance_km
                )
                VALUES (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s
                )
            """, rows)

            connection.commit()

            print(f"Inserted {len(rows)} delivery records")

            rows = []

    if rows:
        cursor.executemany("""
            INSERT INTO deliveries (
                delivery_id,
                sale_id,
                customer_id,
                product_id,
                shipment_date,
                delivery_date,
                quantity_shipped,
                delivery_status,
                delivery_cost,
                distance_km
            )
            VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s
            )
        """, rows)

        connection.commit()

        print(f"Inserted {len(rows)} delivery records")

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM deliveries
    """)

    result = cursor.fetchone()

    print()
    print("Delivery generation completed.")
    print(f"Total delivery records: {result['total']}")

    cursor.close()
    connection.close()

except Error as e:
    print(f"MySQL Error: {e}")

except Exception as e:
    print(f"Error: {e}")