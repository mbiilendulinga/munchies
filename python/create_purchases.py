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
TOTAL_PURCHASES = 4137

material_supplier_types = {
    "Grains & Cereals": ["Grain Supplier", "Agricultural Supplier"],
    "Sweeteners": ["Ingredient Supplier", "Agricultural Supplier"],
    "Oils & Fats": ["Oil Supplier", "Ingredient Supplier"],
    "Nuts & Seeds": ["Agricultural Supplier", "Ingredient Supplier"],
    "Cocoa & Chocolate": ["Ingredient Supplier"],
    "Flavourings": ["Ingredient Supplier"],
    "Salt & Seasonings": ["Ingredient Supplier"],
    "Food Additives": ["Ingredient Supplier"],
    "Packaging Materials": ["Packaging Supplier"],
    "Cleaning & Sanitation": ["Chemical & Cleaning Supplier"]
}

material_weights = {
    "MAT001": 1.35,
    "MAT002": 1.20,
    "MAT003": 1.40,
    "MAT004": 1.00,
    "MAT005": 0.55,
    "MAT006": 0.85,
    "MAT007": 0.45,
    "MAT008": 0.75,
    "MAT009": 1.30,
    "MAT010": 0.45,
    "MAT011": 0.35,
    "MAT012": 0.25,
    "MAT013": 0.25,
    "MAT014": 1.20,
    "MAT015": 0.70,
    "MAT016": 0.65,
    "MAT017": 0.50,
    "MAT018": 0.45,
    "MAT019": 0.90,
    "MAT020": 0.45,
    "MAT021": 0.25,
    "MAT022": 0.30,
    "MAT023": 0.45,
    "MAT024": 0.35,
    "MAT025": 0.25,
    "MAT026": 0.15,
    "MAT027": 0.20,
    "MAT028": 0.20,
    "MAT029": 0.25,
    "MAT030": 0.20,
    "MAT031": 0.15,
    "MAT032": 0.15,
    "MAT033": 0.70,
    "MAT034": 0.30,
    "MAT035": 0.25,
    "MAT036": 0.25,
    "MAT037": 0.20,
    "MAT038": 0.20,
    "MAT039": 0.15,
    "MAT040": 0.25,
    "MAT041": 0.20,
    "MAT042": 0.15,
    "MAT043": 0.15,
    "MAT044": 0.10,
    "MAT045": 1.15,
    "MAT046": 1.00,
    "MAT047": 1.05,
    "MAT048": 1.10,
    "MAT049": 0.80,
    "MAT050": 0.30,
    "MAT051": 0.60,
    "MAT052": 0.25,
    "MAT053": 0.30,
    "MAT054": 0.25,
    "MAT055": 0.20,
    "MAT056": 0.15,
    "MAT057": 0.15,
    "MAT058": 0.10,
    "MAT059": 0.55,
    "MAT060": 0.15,
    "MAT061": 0.10
}

quantity_ranges = {
    "kg": (300, 3500),
    "litre": (200, 2500),
    "units": (1000, 30000),
    "rolls": (20, 250),
    "boxes": (20, 150)
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
                supplier_id,
                supplier_name,
                supplier_type,
                supplier_since,
                status
            FROM suppliers
        """)
        suppliers = cursor.fetchall()

        cursor.execute("""
            SELECT
                material_id,
                material_name,
                material_category,
                unit_of_measure,
                standard_cost,
                material_status
            FROM raw_materials
        """)
        materials = cursor.fetchall()

        cursor.close()

        supplier_map = {}

        for material in materials:
            valid_suppliers = [
                supplier
                for supplier in suppliers
                if supplier["supplier_type"] in material_supplier_types[material["material_category"]]
                and supplier["status"] == "Active"
            ]

            supplier_map[material["material_id"]] = valid_suppliers

        material_choices = []
        material_lookup = {}

        for material in materials:
            material_id = material["material_id"]
            weight = material_weights.get(material_id, 0.25)

            material_choices.append((material_id, weight))
            material_lookup[material_id] = material

        purchase_records = []
        purchase_number = 1

        while len(purchase_records) < TOTAL_PURCHASES:
            material_id = random.choices(
                [item[0] for item in material_choices],
                weights=[item[1] for item in material_choices],
                k=1
            )[0]

            material = material_lookup[material_id]
            eligible_suppliers = supplier_map[material_id]

            if not eligible_suppliers:
                continue

            supplier = random.choice(eligible_suppliers)

            earliest_date = max(
                START_DATE,
                supplier["supplier_since"]
            )

            if earliest_date > END_DATE:
                continue

            days_available = (END_DATE - earliest_date).days
            order_date = earliest_date + timedelta(
                days=random.randint(0, days_available)
            )

            expected_days = random.randint(3, 14)
            expected_date = order_date + timedelta(days=expected_days)

            status_roll = random.random()

            if status_roll < 0.86:
                status = "Received"
            elif status_roll < 0.93:
                status = "Partially Received"
            elif status_roll < 0.97:
                status = "Pending"
            else:
                status = "Cancelled"

            quantity_min, quantity_max = quantity_ranges[
                material["unit_of_measure"]
            ]

            quantity_ordered = random.uniform(
                quantity_min,
                quantity_max
            )

            if material["unit_of_measure"] in ["units", "boxes", "rolls"]:
                quantity_ordered = round(quantity_ordered)
            else:
                quantity_ordered = round(quantity_ordered, 2)

            cost_variation = random.uniform(0.90, 1.12)
            unit_cost = round(
                float(material["standard_cost"]) * cost_variation,
                4
            )

            total_cost = round(
                quantity_ordered * unit_cost,
                2
            )

            actual_receipt_date = None
            quantity_received = 0

            if status == "Received":
                delay_days = random.choices(
                    [-3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7],
                    weights=[2, 3, 5, 18, 18, 15, 12, 9, 6, 4, 2],
                    k=1
                )[0]

                actual_receipt_date = expected_date + timedelta(
                    days=delay_days
                )

                if actual_receipt_date < order_date:
                    actual_receipt_date = order_date + timedelta(
                        days=random.randint(1, expected_days)
                    )

                quantity_received = quantity_ordered

            elif status == "Partially Received":
                delay_days = random.randint(-1, 8)

                actual_receipt_date = expected_date + timedelta(
                    days=delay_days
                )

                if actual_receipt_date < order_date:
                    actual_receipt_date = order_date + timedelta(days=1)

                received_percentage = random.uniform(0.55, 0.94)

                quantity_received = quantity_ordered * received_percentage

                if material["unit_of_measure"] in ["units", "boxes", "rolls"]:
                    quantity_received = round(quantity_received)
                else:
                    quantity_received = round(quantity_received, 2)

            purchase_id = f"PUR{purchase_number:05d}"

            purchase_records.append((
                purchase_id,
                supplier["supplier_id"],
                material_id,
                order_date,
                expected_date,
                actual_receipt_date,
                quantity_ordered,
                quantity_received,
                unit_cost,
                total_cost,
                status
            ))

            purchase_number += 1

        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        cursor = connection.cursor()

        query = """
        INSERT INTO purchases (
            purchase_id,
            supplier_id,
            material_id,
            order_date,
            expected_date,
            actual_receipt_date,
            quantity_ordered,
            quantity_received,
            unit_cost,
            total_cost,
            status
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.executemany(query, purchase_records)
        connection.commit()

        print(f"Inserted {cursor.rowcount} purchases into {DB_NAME}.")
        print("\nSample purchases:")

        for purchase in purchase_records[:10]:
            print(
                purchase[0],
                "| Supplier:",
                purchase[1],
                "| Material:",
                purchase[2],
                "| Ordered:",
                purchase[6],
                "| Received:",
                purchase[7],
                "| Cost: K",
                purchase[9],
                "|",
                purchase[10]
            )

        cursor.close()
        connection.close()

except Error as e:
    print(f"Database error: {e}")