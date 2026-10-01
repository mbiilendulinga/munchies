
# create_customers.py

import mysql.connector
from mysql.connector import Error
from datetime import date, timedelta
import random


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

DB_NAME = "munchies"
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "password"


# ============================================================
# REPRODUCIBILITY
# ============================================================

random.seed(2026)


# ============================================================
# CUSTOMER CONFIGURATION
# ============================================================

CUSTOMER_COUNTS = {
    "Supermarket": 18,
    "Wholesaler": 20,
    "Distributor": 12,
    "Retailer": 45,
    "Convenience Store": 32
}


# ============================================================
# ZAMBIAN LOCATIONS
# ============================================================

locations = {
    "Lusaka": [
        ("Lusaka", "Lusaka"),
        ("Chilanga", "Lusaka"),
        ("Kafue", "Lusaka"),
    ],

    "Copperbelt": [
        ("Kitwe", "Copperbelt"),
        ("Ndola", "Copperbelt"),
        ("Chingola", "Copperbelt"),
        ("Mufulira", "Copperbelt"),
    ],

    "Central": [
        ("Kabwe", "Central"),
        ("Kapiri Mposhi", "Central"),
        ("Mkushi", "Central"),
    ],

    "Southern": [
        ("Livingstone", "Southern"),
        ("Choma", "Southern"),
        ("Mazabuka", "Southern"),
    ],

    "Eastern": [
        ("Chipata", "Eastern"),
        ("Petauke", "Eastern"),
        ("Katete", "Eastern"),
    ],

    "Northern": [
        ("Kasama", "Northern"),
        ("Mbala", "Northern"),
    ],

    "Luapula": [
        ("Mansa", "Luapula"),
        ("Samfya", "Luapula"),
    ],

    "Western": [
        ("Mongu", "Western"),
        ("Senanga", "Western"),
    ],

    "North-Western": [
        ("Solwezi", "North-Western"),
        ("Mwinilunga", "North-Western"),
    ]
}


# Weighted regional distribution.
# Lusaka and Copperbelt receive the largest share.

region_weights = {
    "Lusaka": 40,
    "Copperbelt": 20,
    "Central": 10,
    "Southern": 10,
    "Eastern": 7,
    "Northern": 5,
    "Luapula": 4,
    "Western": 2,
    "North-Western": 2
}


# ============================================================
# BUSINESS NAME COMPONENTS
# ============================================================

business_prefixes = [
    "Capital",
    "Riverside",
    "Manda",
    "Chilanga",
    "Kafue",
    "Central",
    "Mwamba",
    "Chanda",
    "Mulenga",
    "Bwalya",
    "Kabwe",
    "Copperbelt",
    "Zambezi",
    "Sunrise",
    "Lusaka",
    "Green Valley",
    "Golden",
    "Prime",
    "New Horizon",
    "Kamwala",
    "Eastgate",
    "Mukuba",
    "Mosi",
    "Parkview",
    "Grand",
    "Victory",
    "Bright Star",
    "Unity",
    "Great North",
    "Southern Cross",
    "Emerald",
    "Pioneer",
    "Blue Ribbon",
    "Freshland",
    "Metro"
]


business_names = [
    "Trading",
    "Enterprises",
    "Foods",
    "Grocers",
    "General Dealers",
    "Wholesale",
    "Distributors",
    "Supplies",
    "Supermarket",
    "Cash & Carry",
    "Retailers",
    "Merchants",
    "Food Distributors",
    "Market",
    "Stores"
]


# ============================================================
# CUSTOMER TYPE SETTINGS
# ============================================================

customer_settings = {

    "Supermarket": {
        "credit_min": 50000,
        "credit_max": 250000,
        "payment_terms": [30, 45],
        "name_suffixes": [
            "Supermarket",
            "Cash & Carry",
            "Foods",
            "Grocers"
        ]
    },

    "Wholesaler": {
        "credit_min": 75000,
        "credit_max": 350000,
        "payment_terms": [30, 45],
        "name_suffixes": [
            "Wholesale",
            "Wholesale Traders",
            "Merchants",
            "Cash & Carry"
        ]
    },

    "Distributor": {
        "credit_min": 100000,
        "credit_max": 500000,
        "payment_terms": [30, 45],
        "name_suffixes": [
            "Distributors",
            "Food Distributors",
            "Distribution Services",
            "Trading"
        ]
    },

    "Retailer": {
        "credit_min": 10000,
        "credit_max": 60000,
        "payment_terms": [7, 14, 30],
        "name_suffixes": [
            "General Dealers",
            "Retailers",
            "Stores",
            "Grocers",
            "Enterprises"
        ]
    },

    "Convenience Store": {
        "credit_min": 5000,
        "credit_max": 25000,
        "payment_terms": [0, 7, 14],
        "name_suffixes": [
            "Stores",
            "Mini Mart",
            "Convenience Store",
            "Grocers",
            "General Dealers"
        ]
    }
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def weighted_region():
    """Select a region according to the defined regional weights."""

    regions = list(region_weights.keys())
    weights = list(region_weights.values())

    return random.choices(
        regions,
        weights=weights,
        k=1
    )[0]


def generate_customer_name(customer_type, city, used_names):
    """Generate a unique fictional business name."""

    settings = customer_settings[customer_type]

    while True:

        prefix = random.choice(business_prefixes)
        suffix = random.choice(settings["name_suffixes"])

        # Occasionally include the city to make names more geographically
        # believable.

        if random.random() < 0.25:
            name = f"{city} {prefix} {suffix}"
        else:
            name = f"{prefix} {suffix}"

        if name not in used_names:
            used_names.add(name)
            return name


def generate_credit_limit(customer_type):
    """Generate an irregular credit limit appropriate for customer type."""

    settings = customer_settings[customer_type]

    minimum = settings["credit_min"]
    maximum = settings["credit_max"]

    # Generate an irregular amount and round to nearest K250.
    amount = random.randint(minimum, maximum)
    amount = round(amount / 250) * 250

    return float(amount)


def generate_customer_since():
    """
    Customers may have joined Munchies between 2019 and 2025.

    This allows us to have:
    - long-standing customers
    - customers acquired shortly before the analysis period
    - customers acquired during 2023-2025
    """

    start_date = date(2019, 1, 1)
    end_date = date(2025, 6, 30)

    days_between = (end_date - start_date).days

    random_days = random.randint(0, days_between)

    return start_date + timedelta(days=random_days)


# ============================================================
# GENERATE CUSTOMERS
# ============================================================

def generate_customers():

    customers = []

    used_names = set()

    customer_number = 1

    for customer_type, count in CUSTOMER_COUNTS.items():

        for _ in range(count):

            region = weighted_region()

            city, actual_region = random.choice(
                locations[region]
            )

            customer_name = generate_customer_name(
                customer_type,
                city,
                used_names
            )

            settings = customer_settings[customer_type]

            payment_terms = random.choice(
                settings["payment_terms"]
            )

            credit_limit = generate_credit_limit(
                customer_type
            )

            customer_since = generate_customer_since()

            # Most customers remain active.
            # A small percentage become inactive.
            status = (
                "Inactive"
                if random.random() < 0.07
                else "Active"
            )

            customer = {
                "customer_id": f"CUST{customer_number:03d}",
                "customer_name": customer_name,
                "customer_type": customer_type,
                "city": city,
                "region": actual_region,
                "country": "Zambia",
                "credit_limit": credit_limit,
                "payment_terms_days": payment_terms,
                "customer_since": customer_since,
                "status": status
            }

            customers.append(customer)

            customer_number += 1

    return customers


# ============================================================
# INSERT CUSTOMERS INTO MYSQL
# ============================================================

def create_customers():

    connection = None
    cursor = None

    customers = generate_customers()

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
                INSERT INTO customers (
                    customer_id,
                    customer_name,
                    customer_type,
                    city,
                    region,
                    country,
                    credit_limit,
                    payment_terms_days,
                    customer_since,
                    status
                )
                VALUES (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s
                )
            """

            values = [
                (
                    customer["customer_id"],
                    customer["customer_name"],
                    customer["customer_type"],
                    customer["city"],
                    customer["region"],
                    customer["country"],
                    customer["credit_limit"],
                    customer["payment_terms_days"],
                    customer["customer_since"],
                    customer["status"]
                )
                for customer in customers
            ]

            cursor.executemany(
                insert_query,
                values
            )

            connection.commit()

            print(
                f"Successfully inserted "
                f"{cursor.rowcount} customers."
            )

            # ------------------------------------------------
            # DISPLAY SUMMARY
            # ------------------------------------------------

            cursor.execute("""
                SELECT
                    customer_type,
                    COUNT(*) AS customer_count
                FROM customers
                GROUP BY customer_type
                ORDER BY customer_type
            """)

            type_summary = cursor.fetchall()

            print("\nCustomer Type Summary")
            print("-" * 45)

            for row in type_summary:

                print(
                    f"{row[0]:<25} | "
                    f"{row[1]:>5}"
                )

            # ------------------------------------------------
            # REGIONAL SUMMARY
            # ------------------------------------------------

            cursor.execute("""
                SELECT
                    region,
                    COUNT(*) AS customer_count
                FROM customers
                GROUP BY region
                ORDER BY customer_count DESC
            """)

            regional_summary = cursor.fetchall()

            print("\nRegional Summary")
            print("-" * 45)

            for row in regional_summary:

                print(
                    f"{row[0]:<25} | "
                    f"{row[1]:>5}"
                )

            # ------------------------------------------------
            # STATUS SUMMARY
            # ------------------------------------------------

            cursor.execute("""
                SELECT
                    status,
                    COUNT(*) AS customer_count
                FROM customers
                GROUP BY status
            """)

            status_summary = cursor.fetchall()

            print("\nCustomer Status")
            print("-" * 45)

            for row in status_summary:

                print(
                    f"{row[0]:<25} | "
                    f"{row[1]:>5}"
                )

            # ------------------------------------------------
            # SAMPLE CUSTOMERS
            # ------------------------------------------------

            cursor.execute("""
                SELECT
                    customer_id,
                    customer_name,
                    customer_type,
                    city,
                    region,
                    credit_limit,
                    payment_terms_days,
                    customer_since,
                    status
                FROM customers
                ORDER BY customer_id
                LIMIT 15
            """)

            rows = cursor.fetchall()

            print("\nSample Customers")
            print("-" * 130)

            for row in rows:

                print(
                    f"{row[0]:<9} | "
                    f"{row[1]:<32} | "
                    f"{row[2]:<18} | "
                    f"{row[3]:<17} | "
                    f"{row[4]:<15} | "
                    f"K{row[5]:>9.2f} | "
                    f"{row[6]:>2} days | "
                    f"{row[7]} | "
                    f"{row[8]}"
                )

            print("-" * 130)

    except Error as e:

        print(f"Database error: {e}")

    finally:

        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

            print("\nDatabase connection closed.")


# ============================================================
# RUN SCRIPT
# ============================================================

if __name__ == "__main__":
    create_customers()


