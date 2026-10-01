import mysql.connector
from mysql.connector import Error
from datetime import date, timedelta
import random

DB_NAME = "munchies"
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "password"

random.seed(2026)

supplier_names = [
    "Kafue Grain Traders",
    "Zambezi Grain Supplies",
    "Central Milling Suppliers",
    "Lusaka Grain & Foods",
    "Copperbelt Grain Traders",
    "Eastern Agricultural Supplies",
    "Northern Farm Inputs",
    "Southern Grain Merchants",
    "Mumbwa Agricultural Supplies",
    "Chisamba Farm Supplies",

    "Lusaka Packaging Solutions",
    "Central Packaging Supplies",
    "Copperbelt Packaging Traders",
    "Zambezi Packaging Industries",
    "Manda Hill Packaging Supplies",
    "Kafue Packaging Traders",
    "Kitwe Packaging Solutions",

    "Lusaka Food Ingredients",
    "Zambezi Ingredients Ltd",
    "Central Food Ingredients",
    "Copperbelt Food Ingredients",
    "Eastern Ingredients Traders",
    "Southern Food Supplies",
    "Lusaka Flavour & Ingredients",

    "Zambezi Oils & Commodities",
    "Lusaka Edible Oils",
    "Copperbelt Oil Suppliers",
    "Central Oils & Foods",

    "Lusaka Industrial Supplies",
    "Kafue Cleaning Solutions",
    "Copperbelt Hygiene Supplies",
    "Central Chemical Traders",
    "Zambezi Industrial Chemicals",

    "Choma Agricultural Traders",
    "Chipata Farm Supplies",
    "Kasama Agricultural Suppliers",
    "Ndola Food Commodities",
    "Kitwe Agricultural Traders",
    "Mazabuka Grain & Supplies",
    "Kabwe Farm & Food Supplies",
    "Solwezi Agricultural Traders",
    "Mansa Food & Agricultural Supplies"
]

locations = [
    ("Lusaka", "Lusaka"),
    ("Lusaka", "Lusaka"),
    ("Lusaka", "Lusaka"),
    ("Chilanga", "Lusaka"),
    ("Kafue", "Lusaka"),
    ("Kabwe", "Central"),
    ("Kapiri Mposhi", "Central"),
    ("Mkushi", "Central"),
    ("Kitwe", "Copperbelt"),
    ("Ndola", "Copperbelt"),
    ("Chingola", "Copperbelt"),
    ("Mufulira", "Copperbelt"),
    ("Choma", "Southern"),
    ("Mazabuka", "Southern"),
    ("Livingstone", "Southern"),
    ("Chipata", "Eastern"),
    ("Petauke", "Eastern"),
    ("Katete", "Eastern"),
    ("Kasama", "Northern"),
    ("Mbala", "Northern"),
    ("Mansa", "Luapula"),
    ("Samfya", "Luapula"),
    ("Mongu", "Western"),
    ("Solwezi", "North-Western")
]

supplier_type_rules = {
    "Grain Supplier": ["Lusaka", "Central", "Copperbelt", "Southern", "Eastern", "Northern"],
    "Agricultural Supplier": ["Lusaka", "Central", "Copperbelt", "Southern", "Eastern", "Northern", "Luapula", "North-Western"],
    "Packaging Supplier": ["Lusaka", "Copperbelt", "Central"],
    "Ingredient Supplier": ["Lusaka", "Copperbelt", "Central", "Southern", "Eastern"],
    "Oil Supplier": ["Lusaka", "Copperbelt", "Central"],
    "Chemical & Cleaning Supplier": ["Lusaka", "Copperbelt", "Central"]
}

type_sequence = [
    "Grain Supplier",
    "Grain Supplier",
    "Grain Supplier",
    "Grain Supplier",
    "Grain Supplier",
    "Grain Supplier",
    "Agricultural Supplier",
    "Agricultural Supplier",
    "Agricultural Supplier",
    "Agricultural Supplier",
    "Agricultural Supplier",
    "Agricultural Supplier",
    "Agricultural Supplier",
    "Agricultural Supplier",
    "Packaging Supplier",
    "Packaging Supplier",
    "Packaging Supplier",
    "Packaging Supplier",
    "Packaging Supplier",
    "Packaging Supplier",
    "Packaging Supplier",
    "Ingredient Supplier",
    "Ingredient Supplier",
    "Ingredient Supplier",
    "Ingredient Supplier",
    "Ingredient Supplier",
    "Ingredient Supplier",
    "Ingredient Supplier",
    "Oil Supplier",
    "Oil Supplier",
    "Oil Supplier",
    "Oil Supplier",
    "Chemical & Cleaning Supplier",
    "Chemical & Cleaning Supplier",
    "Chemical & Cleaning Supplier",
    "Chemical & Cleaning Supplier",
    "Agricultural Supplier",
    "Agricultural Supplier",
    "Agricultural Supplier",
    "Grain Supplier",
    "Agricultural Supplier",
    "Agricultural Supplier"
]

payment_terms_by_type = {
    "Grain Supplier": [14, 30, 30, 45, 60],
    "Agricultural Supplier": [14, 30, 30, 45],
    "Packaging Supplier": [30, 45, 60],
    "Ingredient Supplier": [14, 30, 45, 60],
    "Oil Supplier": [30, 45, 60],
    "Chemical & Cleaning Supplier": [14, 30, 45]
}

start_date = date(2019, 1, 1)
end_date = date(2025, 6, 30)

suppliers = []

for i in range(42):
    supplier_id = f"SUP{i + 1:03d}"
    supplier_name = supplier_names[i]
    supplier_type = type_sequence[i]

    valid_locations = [
        location for location in locations
        if location[1] in supplier_type_rules[supplier_type]
    ]

    city, region = random.choice(valid_locations)

    supplier_since = start_date + timedelta(
        days=random.randint(0, (end_date - start_date).days)
    )

    payment_terms_days = random.choice(
        payment_terms_by_type[supplier_type]
    )

    status = "Inactive" if random.random() < 0.07 else "Active"

    suppliers.append((
        supplier_id,
        supplier_name,
        supplier_type,
        city,
        region,
        "Zambia",
        payment_terms_days,
        supplier_since,
        status
    ))

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
        INSERT INTO suppliers (
            supplier_id,
            supplier_name,
            supplier_type,
            city,
            region,
            country,
            payment_terms_days,
            supplier_since,
            status
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.executemany(query, suppliers)
        connection.commit()

        print(f"Inserted {cursor.rowcount} suppliers into {DB_NAME}.")
        print("\nSample suppliers:")

        for supplier in suppliers[:10]:
            print(
                supplier[0],
                "|",
                supplier[1],
                "|",
                supplier[2],
                "|",
                supplier[3],
                "|",
                supplier[4],
                "|",
                supplier[6],
                "days",
                "|",
                supplier[8]
            )

        cursor.close()
        connection.close()

except Error as e:
    print(f"Database error: {e}")