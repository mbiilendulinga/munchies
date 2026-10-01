
import mysql.connector
from mysql.connector import Error
from datetime import timedelta
import random

DB_NAME = "munchies"
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "password"

TARGET_ROWS = 1847

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
            c.customer_type
        FROM sales s
        JOIN customers c
            ON s.customer_id = c.customer_id
        WHERE s.invoice_status != 'Cancelled'
    """)

    sales = cursor.fetchall()

    if not sales:
        raise Exception("No eligible sales found.")

    product_factories = [
        "Munchies Lusaka Factory",
        "Munchies Central Factory",
        "Munchies Copperbelt Factory"
    ]

    event_types = [
        "Customer Return",
        "Quality Complaint",
        "Damaged Product",
        "Manufacturing Defect",
        "Packaging Defect",
        "Expired Product",
        "Short Shipment"
    ]

    event_type_weights = [
        35,
        18,
        17,
        9,
        10,
        6,
        5
    ]

    reasons = {
        "Customer Return": [
            "Customer changed order",
            "Excess stock at customer",
            "Product not required",
            "Customer specification issue"
        ],
        "Quality Complaint": [
            "Taste concern",
            "Texture concern",
            "Product appearance",
            "Customer quality complaint"
        ],
        "Damaged Product": [
            "Damaged during transport",
            "Crushed packaging",
            "Torn packaging",
            "Water damaged cartons"
        ],
        "Manufacturing Defect": [
            "Incorrect product formulation",
            "Production defect",
            "Inconsistent product quality",
            "Foreign material concern"
        ],
        "Packaging Defect": [
            "Seal failure",
            "Incorrect label",
            "Damaged pouch",
            "Loose packaging"
        ],
        "Expired Product": [
            "Expired stock",
            "Short remaining shelf life",
            "Shelf-life concern"
        ],
        "Short Shipment": [
            "Quantity discrepancy",
            "Missing cartons",
            "Short delivered quantity"
        ]
    }

    status_weights = {
        "Customer Return": {
            "Resolved": 80,
            "Closed": 15,
            "Open": 5
        },
        "Quality Complaint": {
            "Resolved": 65,
            "Closed": 15,
            "Open": 20
        },
        "Damaged Product": {
            "Resolved": 75,
            "Closed": 20,
            "Open": 5
        },
        "Manufacturing Defect": {
            "Resolved": 60,
            "Closed": 15,
            "Open": 25
        },
        "Packaging Defect": {
            "Resolved": 70,
            "Closed": 20,
            "Open": 10
        },
        "Expired Product": {
            "Resolved": 80,
            "Closed": 15,
            "Open": 5
        },
        "Short Shipment": {
            "Resolved": 85,
            "Closed": 12,
            "Open": 3
        }
    }

    rows = []

    selected_sales = random.choices(
        sales,
        k=TARGET_ROWS
    )

    for i, sale in enumerate(selected_sales, start=1):

        event_type = random.choices(
            event_types,
            weights=event_type_weights,
            k=1
        )[0]

        event_date = sale["sale_date"] + timedelta(
            days=random.randint(1, 45)
        )

        sale_quantity = float(sale["quantity"])

        if event_type == "Short Shipment":
            quantity = max(
                1,
                round(
                    sale_quantity *
                    random.uniform(0.01, 0.12)
                )
            )

        elif event_type == "Customer Return":
            quantity = max(
                1,
                round(
                    sale_quantity *
                    random.uniform(0.05, 0.35)
                )
            )

        elif event_type == "Damaged Product":
            quantity = max(
                1,
                round(
                    sale_quantity *
                    random.uniform(0.01, 0.18)
                )
            )

        elif event_type == "Expired Product":
            quantity = max(
                1,
                round(
                    sale_quantity *
                    random.uniform(0.05, 0.30)
                )
            )

        elif event_type == "Packaging Defect":
            quantity = max(
                1,
                round(
                    sale_quantity *
                    random.uniform(0.01, 0.20)
                )
            )

        else:
            quantity = max(
                1,
                round(
                    sale_quantity *
                    random.uniform(0.01, 0.15)
                )
            )

        reason = random.choice(
            reasons[event_type]
        )

        if event_type in [
            "Manufacturing Defect",
            "Packaging Defect"
        ]:
            customer_id = None
            factory_name = random.choice(
                product_factories
            )
        else:
            customer_id = sale["customer_id"]
            factory_name = None

        status_options = list(
            status_weights[event_type].keys()
        )

        status_probabilities = list(
            status_weights[event_type].values()
        )

        status = random.choices(
            status_options,
            weights=status_probabilities,
            k=1
        )[0]

        quality_return_id = f"RET{i:05d}"

        rows.append((
            quality_return_id,
            event_date,
            sale["product_id"],
            customer_id,
            event_type,
            quantity,
            reason,
            factory_name,
            status
        ))

        if len(rows) >= 500:
            cursor.executemany("""
                INSERT INTO quality_returns (
                    quality_return_id,
                    event_date,
                    product_id,
                    customer_id,
                    event_type,
                    quantity,
                    reason,
                    factory_name,
                    status
                )
                VALUES (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s
                )
            """, rows)

            connection.commit()

            print(
                f"Inserted {len(rows)} quality return records"
            )

            rows = []

    if rows:
        cursor.executemany("""
            INSERT INTO quality_returns (
                quality_return_id,
                event_date,
                product_id,
                customer_id,
                event_type,
                quantity,
                reason,
                factory_name,
                status
            )
            VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s
            )
        """, rows)

        connection.commit()

        print(
            f"Inserted {len(rows)} quality return records"
        )

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM quality_returns
    """)

    result = cursor.fetchone()

    print()
    print("Quality return generation completed.")
    print(f"Total quality return records: {result['total']}")

    cursor.close()
    connection.close()

except Error as e:
    print(f"MySQL Error: {e}")

except Exception as e:
    print(f"Error: {e}")

