import mysql.connector
from mysql.connector import Error
from datetime import date, timedelta
import random

DB_NAME = "munchies"
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "password"

TARGET_ROWS = 78143

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
            product_id,
            product_name,
            category,
            unit_price,
            standard_cost,
            launch_date
        FROM products
        WHERE product_status = 'Active'
    """)

    products = cursor.fetchall()

    cursor.execute("""
        SELECT
            customer_id,
            customer_type,
            region,
            customer_since,
            status
        FROM customers
    """)

    customers = cursor.fetchall()

    if not products:
        raise Exception("No products found.")

    if not customers:
        raise Exception("No customers found.")

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

    customer_weights = {
        "Supermarket": 2.8,
        "Wholesaler": 2.5,
        "Distributor": 2.2,
        "Retailer": 1.2,
        "Convenience Store": 0.8
    }

    sales_channels = {
        "Supermarket": ["Direct Sales", "Key Account"],
        "Wholesaler": ["Direct Sales", "Wholesale"],
        "Distributor": ["Distributor", "Direct Sales"],
        "Retailer": ["Direct Sales", "Retail"],
        "Convenience Store": ["Retail", "Direct Sales"]
    }

    sales_reps = [
        "M. Banda",
        "C. Phiri",
        "J. Mwansa",
        "T. Chanda",
        "B. Mulenga",
        "R. Zulu",
        "P. Tembo",
        "K. Nyirenda",
        "D. Lungu",
        "S. Mumba",
        "E. Chileshe",
        "N. Musonda"
    ]

    quantity_ranges = {
        "Supermarket": (40, 650),
        "Wholesaler": (150, 1800),
        "Distributor": (300, 3000),
        "Retailer": (10, 180),
        "Convenience Store": (5, 70)
    }

    eligible_customers = []

    for customer in customers:
        eligible_customers.append(customer)

    start_date = date(2023, 1, 1)
    end_date = date(2025, 12, 31)

    date_range = (end_date - start_date).days

    rows = []

    for i in range(1, TARGET_ROWS + 1):

        product = random.choices(
            products,
            weights=[
                product_weights.get(product["product_id"], 1.0)
                for product in products
            ],
            k=1
        )[0]

        customer = random.choices(
            eligible_customers,
            weights=[
                customer_weights.get(customer["customer_type"], 1.0)
                for customer in eligible_customers
            ],
            k=1
        )[0]

        earliest_date = max(
            start_date,
            customer["customer_since"],
            product["launch_date"]
        )

        if earliest_date > end_date:
            continue

        sale_date = earliest_date + timedelta(
            days=random.randint(
                0,
                (end_date - earliest_date).days
            )
        )

        month = sale_date.month

        seasonal_factor = 1.0

        if month in [11, 12]:
            seasonal_factor = random.uniform(1.08, 1.25)
        elif month in [1, 2]:
            seasonal_factor = random.uniform(0.88, 0.97)
        elif month in [6, 7, 8]:
            seasonal_factor = random.uniform(1.02, 1.10)

        min_qty, max_qty = quantity_ranges[
            customer["customer_type"]
        ]

        quantity = random.randint(min_qty, max_qty)

        quantity = int(quantity * seasonal_factor)

        if product["category"] == "Snacks":
            quantity = int(quantity * random.uniform(0.90, 1.10))

        if product["category"] == "Cereal":
            quantity = int(quantity * random.uniform(0.95, 1.12))

        quantity = max(quantity, 1)

        base_price = float(product["unit_price"])

        price_factor = random.uniform(0.97, 1.04)

        if customer["customer_type"] in ["Wholesaler", "Distributor"]:
            price_factor *= random.uniform(0.94, 0.99)

        unit_price = round(base_price * price_factor, 2)

        gross_amount = quantity * unit_price

        discount_rate = 0

        if customer["customer_type"] == "Distributor":
            discount_rate = random.uniform(0.02, 0.08)
        elif customer["customer_type"] == "Wholesaler":
            discount_rate = random.uniform(0.01, 0.06)
        elif customer["customer_type"] == "Supermarket":
            discount_rate = random.uniform(0.00, 0.04)
        elif customer["customer_type"] == "Retailer":
            discount_rate = random.uniform(0.00, 0.025)
        else:
            discount_rate = random.uniform(0.00, 0.015)

        if random.random() < 0.18:
            discount_rate = 0

        discount = round(
            gross_amount * discount_rate,
            2
        )

        revenue = round(
            gross_amount - discount,
            2
        )

        cost_variation = random.uniform(0.97, 1.04)

        cost = round(
            quantity *
            float(product["standard_cost"]) *
            cost_variation,
            2
        )

        profit = round(
            revenue - cost,
            2
        )

        channel = random.choice(
            sales_channels[customer["customer_type"]]
        )

        if random.random() < 0.04:
            invoice_status = "Cancelled"
            discount = 0
            revenue = 0
            profit = 0
        elif random.random() < 0.06:
            invoice_status = "Pending"
        elif random.random() < 0.08:
            invoice_status = "Partially Paid"
        else:
            invoice_status = "Paid"

        sale_id = f"SALE{i:05d}"

        rows.append((
            sale_id,
            sale_date,
            customer["customer_id"],
            product["product_id"],
            quantity,
            unit_price,
            discount,
            revenue,
            cost,
            profit,
            channel,
            random.choice(sales_reps),
            invoice_status
        ))

        if len(rows) >= 5000:
            cursor.executemany("""
                INSERT INTO sales (
                    sale_id,
                    sale_date,
                    customer_id,
                    product_id,
                    quantity,
                    unit_price,
                    discount,
                    revenue,
                    cost,
                    profit,
                    sales_channel,
                    sales_rep,
                    invoice_status
                )
                VALUES (
                    %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s
                )
            """, rows)

            connection.commit()

            print(f"Inserted {len(rows)} sales records")

            rows = []

    if rows:
        cursor.executemany("""
            INSERT INTO sales (
                sale_id,
                sale_date,
                customer_id,
                product_id,
                quantity,
                unit_price,
                discount,
                revenue,
                cost,
                profit,
                sales_channel,
                sales_rep,
                invoice_status
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s
            )
        """, rows)

        connection.commit()

        print(f"Inserted {len(rows)} sales records")

    cursor.execute("SELECT COUNT(*) AS total FROM sales")
    result = cursor.fetchone()

    print()
    print("Sales generation completed.")
    print(f"Total sales records: {result['total']}")

    cursor.close()
    connection.close()

except Error as e:
    print(f"MySQL Error: {e}")

except Exception as e:
    print(f"Error: {e}")