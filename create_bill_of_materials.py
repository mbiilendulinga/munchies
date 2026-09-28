import mysql.connector
from mysql.connector import Error
from datetime import date

DB_NAME = "munchies"
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "password"

bom_data = [
    ("PROD001", "MAT001", 0.3200, "kg"),
    ("PROD001", "MAT009", 0.0450, "kg"),
    ("PROD001", "MAT033", 0.0060, "kg"),
    ("PROD001", "MAT014", 0.0180, "litre"),
    ("PROD001", "MAT040", 0.0020, "kg"),

    ("PROD002", "MAT001", 0.3000, "kg"),
    ("PROD002", "MAT009", 0.0350, "kg"),
    ("PROD002", "MAT012", 0.0250, "kg"),
    ("PROD002", "MAT033", 0.0050, "kg"),
    ("PROD002", "MAT014", 0.0180, "litre"),

    ("PROD003", "MAT004", 0.3100, "kg"),
    ("PROD003", "MAT006", 0.0800, "kg"),
    ("PROD003", "MAT009", 0.0400, "kg"),
    ("PROD003", "MAT033", 0.0060, "kg"),
    ("PROD003", "MAT014", 0.0170, "litre"),

    ("PROD004", "MAT004", 0.2900, "kg"),
    ("PROD004", "MAT006", 0.0750, "kg"),
    ("PROD004", "MAT009", 0.0350, "kg"),
    ("PROD004", "MAT012", 0.0200, "kg"),
    ("PROD004", "MAT033", 0.0050, "kg"),

    ("PROD005", "MAT003", 0.3200, "kg"),
    ("PROD005", "MAT009", 0.0420, "kg"),
    ("PROD005", "MAT033", 0.0060, "kg"),
    ("PROD005", "MAT014", 0.0180, "litre"),
    ("PROD005", "MAT040", 0.0020, "kg"),

    ("PROD006", "MAT003", 0.3000, "kg"),
    ("PROD006", "MAT023", 0.0300, "kg"),
    ("PROD006", "MAT009", 0.0450, "kg"),
    ("PROD006", "MAT033", 0.0050, "kg"),
    ("PROD006", "MAT014", 0.0180, "litre"),

    ("PROD007", "MAT001", 0.2800, "kg"),
    ("PROD007", "MAT009", 0.0400, "kg"),
    ("PROD007", "MAT029", 0.0120, "kg"),
    ("PROD007", "MAT033", 0.0050, "kg"),
    ("PROD007", "MAT014", 0.0180, "litre"),

    ("PROD008", "MAT001", 0.2800, "kg"),
    ("PROD008", "MAT009", 0.0400, "kg"),
    ("PROD008", "MAT030", 0.0120, "kg"),
    ("PROD008", "MAT033", 0.0050, "kg"),
    ("PROD008", "MAT014", 0.0180, "litre"),

    ("PROD009", "MAT001", 0.2750, "kg"),
    ("PROD009", "MAT023", 0.0320, "kg"),
    ("PROD009", "MAT009", 0.0450, "kg"),
    ("PROD009", "MAT033", 0.0050, "kg"),
    ("PROD009", "MAT014", 0.0180, "litre"),

    ("PROD010", "MAT002", 0.1600, "kg"),
    ("PROD010", "MAT014", 0.0250, "litre"),
    ("PROD010", "MAT033", 0.0060, "kg"),
    ("PROD010", "MAT045", 0.0060, "kg"),
    ("PROD010", "MAT047", 1.0000, "units"),

    ("PROD011", "MAT002", 0.1600, "kg"),
    ("PROD011", "MAT014", 0.0250, "litre"),
    ("PROD011", "MAT033", 0.0050, "kg"),
    ("PROD011", "MAT034", 0.0060, "kg"),
    ("PROD011", "MAT047", 1.0000, "units"),

    ("PROD012", "MAT002", 0.1600, "kg"),
    ("PROD012", "MAT014", 0.0250, "litre"),
    ("PROD012", "MAT033", 0.0050, "kg"),
    ("PROD012", "MAT035", 0.0080, "kg"),
    ("PROD012", "MAT036", 0.0040, "kg"),
    ("PROD012", "MAT047", 1.0000, "units"),

    ("PROD013", "MAT019", 0.0850, "kg"),
    ("PROD013", "MAT033", 0.0040, "kg"),
    ("PROD013", "MAT014", 0.0060, "litre"),
    ("PROD013", "MAT047", 1.0000, "units"),

    ("PROD014", "MAT019", 0.0800, "kg"),
    ("PROD014", "MAT012", 0.0150, "kg"),
    ("PROD014", "MAT009", 0.0100, "kg"),
    ("PROD014", "MAT033", 0.0030, "kg"),
    ("PROD014", "MAT014", 0.0060, "litre"),
    ("PROD014", "MAT047", 1.0000, "units"),

    ("PROD015", "MAT003", 0.0550, "kg"),
    ("PROD015", "MAT009", 0.0250, "kg"),
    ("PROD015", "MAT018", 0.0200, "kg"),
    ("PROD015", "MAT023", 0.0120, "kg"),
    ("PROD015", "MAT040", 0.0020, "kg"),
    ("PROD015", "MAT048", 1.0000, "units"),

    ("PROD016", "MAT003", 0.0550, "kg"),
    ("PROD016", "MAT009", 0.0240, "kg"),
    ("PROD016", "MAT018", 0.0200, "kg"),
    ("PROD016", "MAT032", 0.0080, "kg"),
    ("PROD016", "MAT040", 0.0020, "kg"),
    ("PROD016", "MAT048", 1.0000, "units"),

    ("PROD017", "MAT003", 0.0550, "kg"),
    ("PROD017", "MAT009", 0.0240, "kg"),
    ("PROD017", "MAT018", 0.0200, "kg"),
    ("PROD017", "MAT032", 0.0100, "kg"),
    ("PROD017", "MAT040", 0.0020, "kg"),
    ("PROD017", "MAT048", 1.0000, "units")
]

try:
    connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    if connection.is_connected():
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT product_id FROM products")
        product_ids = {
            row["product_id"]
            for row in cursor.fetchall()
        }

        cursor.execute("SELECT material_id FROM raw_materials")
        material_ids = {
            row["material_id"]
            for row in cursor.fetchall()
        }

        cursor.close()

        valid_bom = []
        used_pairs = set()

        for index, item in enumerate(bom_data, start=1):
            product_id, material_id, quantity_required, unit_of_measure = item

            if product_id not in product_ids:
                raise ValueError(f"Product {product_id} does not exist.")

            if material_id not in material_ids:
                raise ValueError(f"Material {material_id} does not exist.")

            pair = (product_id, material_id)

            if pair in used_pairs:
                raise ValueError(
                    f"Duplicate product/material combination: {product_id} / {material_id}"
                )

            used_pairs.add(pair)

            bom_id = f"BOM{index:03d}"

            valid_bom.append((
                bom_id,
                product_id,
                material_id,
                quantity_required,
                unit_of_measure,
                date(2023, 1, 1),
                "Active"
            ))

        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        cursor = connection.cursor()

        query = """
        INSERT INTO bill_of_materials (
            bom_id,
            product_id,
            material_id,
            quantity_required,
            unit_of_measure,
            effective_date,
            status
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.executemany(query, valid_bom)
        connection.commit()

        print(f"Inserted {cursor.rowcount} BOM records into {DB_NAME}.")
        print("\nSample BOM records:")

        for bom in valid_bom[:10]:
            print(
                bom[0],
                "| Product:",
                bom[1],
                "| Material:",
                bom[2],
                "| Quantity:",
                bom[3],
                bom[4],
                "|",
                bom[6]
            )

        cursor.close()
        connection.close()

except Error as e:
    print(f"Database error: {e}")

except ValueError as e:
    print(f"Validation error: {e}")