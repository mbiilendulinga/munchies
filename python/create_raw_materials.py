import mysql.connector
from mysql.connector import Error
import random

DB_NAME = "munchies"
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "password"

random.seed(2026)

materials = [
    ("MAT001", "Maize Flour", "Grains & Cereals", "kg", 8.50, 2500),
    ("MAT002", "White Maize Meal", "Grains & Cereals", "kg", 7.80, 3000),
    ("MAT003", "Wheat Flour", "Grains & Cereals", "kg", 12.50, 2200),
    ("MAT004", "Wheat Bran", "Grains & Cereals", "kg", 6.20, 1800),
    ("MAT005", "Oat Flakes", "Grains & Cereals", "kg", 16.50, 1200),
    ("MAT006", "Whole Wheat Flour", "Grains & Cereals", "kg", 14.20, 1500),
    ("MAT007", "Rice Flour", "Grains & Cereals", "kg", 13.80, 1000),
    ("MAT008", "Corn Grits", "Grains & Cereals", "kg", 9.40, 1800),

    ("MAT009", "Granulated Sugar", "Sweeteners", "kg", 18.00, 1800),
    ("MAT010", "Icing Sugar", "Sweeteners", "kg", 20.50, 700),
    ("MAT011", "Glucose Syrup", "Sweeteners", "kg", 24.00, 600),
    ("MAT012", "Honey", "Sweeteners", "kg", 48.00, 400),
    ("MAT013", "Malt Extract", "Sweeteners", "kg", 32.00, 350),

    ("MAT014", "Vegetable Oil", "Oils & Fats", "litre", 24.50, 1200),
    ("MAT015", "Sunflower Oil", "Oils & Fats", "litre", 27.50, 900),
    ("MAT016", "Palm Oil", "Oils & Fats", "kg", 21.00, 1000),
    ("MAT017", "Shortening", "Oils & Fats", "kg", 29.00, 700),
    ("MAT018", "Margarine", "Oils & Fats", "kg", 31.50, 600),

    ("MAT019", "Raw Peanuts", "Nuts & Seeds", "kg", 34.00, 900),
    ("MAT020", "Roasted Peanuts", "Nuts & Seeds", "kg", 39.00, 600),
    ("MAT021", "Sesame Seeds", "Nuts & Seeds", "kg", 42.00, 300),
    ("MAT022", "Peanut Paste", "Nuts & Seeds", "kg", 46.00, 350),

    ("MAT023", "Cocoa Powder", "Cocoa & Chocolate", "kg", 68.00, 350),
    ("MAT024", "Chocolate Compound", "Cocoa & Chocolate", "kg", 82.00, 300),
    ("MAT025", "Chocolate Chips", "Cocoa & Chocolate", "kg", 75.00, 250),
    ("MAT026", "Cocoa Butter", "Cocoa & Chocolate", "kg", 95.00, 150),

    ("MAT027", "Vanilla Flavour", "Flavourings", "kg", 125.00, 80),
    ("MAT028", "Chocolate Flavour", "Flavourings", "kg", 110.00, 100),
    ("MAT029", "Strawberry Flavour", "Flavourings", "kg", 118.00, 100),
    ("MAT030", "Banana Flavour", "Flavourings", "kg", 105.00, 100),
    ("MAT031", "Honey Flavour", "Flavourings", "kg", 115.00, 80),
    ("MAT032", "Cream Flavour", "Flavourings", "kg", 120.00, 80),

    ("MAT033", "Table Salt", "Salt & Seasonings", "kg", 7.50, 800),
    ("MAT034", "Chilli Powder", "Salt & Seasonings", "kg", 38.00, 250),
    ("MAT035", "Cheese Seasoning", "Salt & Seasonings", "kg", 72.00, 200),
    ("MAT036", "Onion Powder", "Salt & Seasonings", "kg", 45.00, 200),
    ("MAT037", "Garlic Powder", "Salt & Seasonings", "kg", 48.00, 180),
    ("MAT038", "BBQ Seasoning", "Salt & Seasonings", "kg", 55.00, 150),

    ("MAT039", "Lecithin", "Food Additives", "kg", 86.00, 120),
    ("MAT040", "Sodium Bicarbonate", "Food Additives", "kg", 22.00, 250),
    ("MAT041", "Citric Acid", "Food Additives", "kg", 31.00, 180),
    ("MAT042", "Calcium Carbonate", "Food Additives", "kg", 18.50, 200),
    ("MAT043", "Preservative Blend", "Food Additives", "kg", 92.00, 100),
    ("MAT044", "Antioxidant Blend", "Food Additives", "kg", 105.00, 80),

    ("MAT045", "Plastic Packaging Film", "Packaging Materials", "kg", 32.00, 1200),
    ("MAT046", "Printed Cereal Boxes", "Packaging Materials", "units", 2.80, 15000),
    ("MAT047", "Snack Pouches", "Packaging Materials", "units", 1.90, 20000),
    ("MAT048", "Product Labels", "Packaging Materials", "units", 0.45, 30000),
    ("MAT049", "Shipping Cartons", "Packaging Materials", "units", 4.50, 8000),
    ("MAT050", "Packaging Tape", "Packaging Materials", "rolls", 18.00, 300),
    ("MAT051", "Plastic Bags", "Packaging Materials", "units", 0.80, 12000),
    ("MAT052", "Pallet Wrap", "Packaging Materials", "kg", 38.00, 400),

    ("MAT053", "Industrial Detergent", "Cleaning & Sanitation", "litre", 28.00, 250),
    ("MAT054", "Food Grade Sanitizer", "Cleaning & Sanitation", "litre", 42.00, 180),
    ("MAT055", "Disinfectant", "Cleaning & Sanitation", "litre", 24.00, 200),
    ("MAT056", "Caustic Cleaning Solution", "Cleaning & Sanitation", "litre", 35.00, 150),
    ("MAT057", "Hand Sanitizer", "Cleaning & Sanitation", "litre", 45.00, 100),
    ("MAT058", "Machine Cleaning Solvent", "Cleaning & Sanitation", "litre", 58.00, 80),

    ("MAT059", "Corrugated Sheets", "Packaging Materials", "units", 3.20, 5000),
    ("MAT060", "Food Grade Gloves", "Cleaning & Sanitation", "boxes", 65.00, 120),
    ("MAT061", "Cleaning Brushes", "Cleaning & Sanitation", "units", 22.00, 80)
]

try:
    connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    if connection.is_connected():
        cursor = connection.cursor()

        query = """
        INSERT INTO raw_materials (
            material_id,
            material_name,
            material_category,
            unit_of_measure,
            standard_cost,
            reorder_level
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.executemany(query, materials)
        connection.commit()

        print(f"Inserted {cursor.rowcount} raw materials into {DB_NAME}.")
        print("\nSample raw materials:")

        for material in materials[:10]:
            print(
                material[0],
                "|",
                material[1],
                "|",
                material[2],
                "|",
                material[3],
                "| K",
                material[4],
                "| Reorder:",
                material[5]
            )

        cursor.close()
        connection.close()

except Error as e:
    print(f"Database error: {e}")