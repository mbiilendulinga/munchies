
import mysql.connector
from mysql.connector import Error
from datetime import date, timedelta
import random

DB_NAME = "munchies"
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "password"

TARGET_ROWS = 3126

random.seed(2026)

try:
    connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    cursor = connection.cursor()

    expense_categories = {
        "Raw Materials": {
            "department": "Procurement",
            "amount": (1500, 85000),
            "weight": 18
        },
        "Packaging": {
            "department": "Production",
            "amount": (1000, 45000),
            "weight": 12
        },
        "Utilities": {
            "department": "Operations",
            "amount": (2500, 65000),
            "weight": 10
        },
        "Transport & Logistics": {
            "department": "Logistics",
            "amount": (1200, 38000),
            "weight": 12
        },
        "Equipment Maintenance": {
            "department": "Production",
            "amount": (2500, 75000),
            "weight": 8
        },
        "Factory Supplies": {
            "department": "Production",
            "amount": (500, 18000),
            "weight": 8
        },
        "Quality Control": {
            "department": "Quality Assurance",
            "amount": (800, 22000),
            "weight": 5
        },
        "Salaries & Wages": {
            "department": "Human Resources",
            "amount": (8000, 95000),
            "weight": 8
        },
        "Marketing": {
            "department": "Marketing",
            "amount": (1500, 55000),
            "weight": 6
        },
        "Sales & Distribution": {
            "department": "Sales",
            "amount": (1000, 30000),
            "weight": 6
        },
        "Office & Administration": {
            "department": "Administration",
            "amount": (400, 12000),
            "weight": 5
        },
        "Insurance": {
            "department": "Finance",
            "amount": (3000, 70000),
            "weight": 2
        }
    }

    categories = list(expense_categories.keys())

    weights = [
        expense_categories[category]["weight"]
        for category in categories
    ]

    descriptions = {
        "Raw Materials": [
            "Bulk ingredient purchase",
            "Production ingredient replenishment",
            "Grain procurement",
            "Ingredient supplier payment",
            "Specialty ingredient purchase"
        ],
        "Packaging": [
            "Packaging material purchase",
            "Printed packaging order",
            "Cereal box procurement",
            "Snack pouch procurement",
            "Packaging replenishment"
        ],
        "Utilities": [
            "Electricity bill",
            "Water bill",
            "Factory power consumption",
            "Waste management charges",
            "Utility service payment"
        ],
        "Transport & Logistics": [
            "Fleet fuel expense",
            "Vehicle maintenance",
            "Third-party transport",
            "Distribution transport",
            "Regional delivery logistics"
        ],
        "Equipment Maintenance": [
            "Production line maintenance",
            "Machine repair",
            "Equipment servicing",
            "Preventive maintenance",
            "Replacement machine parts"
        ],
        "Factory Supplies": [
            "Factory consumables",
            "Cleaning supplies",
            "Production safety supplies",
            "Factory tools",
            "Operational consumables"
        ],
        "Quality Control": [
            "Laboratory testing",
            "Product quality testing",
            "Quality inspection supplies",
            "Sample testing",
            "Quality assurance services"
        ],
        "Salaries & Wages": [
            "Monthly payroll",
            "Factory wages",
            "Staff allowances",
            "Overtime payments",
            "Temporary worker wages"
        ],
        "Marketing": [
            "Product promotion",
            "Advertising campaign",
            "In-store promotion",
            "Marketing materials",
            "Brand activation"
        ],
        "Sales & Distribution": [
            "Sales team expenses",
            "Customer promotion",
            "Sales representative expenses",
            "Distribution support",
            "Trade promotion"
        ],
        "Office & Administration": [
            "Office supplies",
            "Stationery purchase",
            "Administrative expenses",
            "Communication expenses",
            "Office maintenance"
        ],
        "Insurance": [
            "Factory insurance",
            "Vehicle insurance",
            "Equipment insurance",
            "Business insurance",
            "Insurance premium"
        ]
    }

    start_date = date(2023, 1, 1)
    end_date = date(2025, 12, 31)

    date_range = (end_date - start_date).days

    rows = []

    for i in range(1, TARGET_ROWS + 1):

        category = random.choices(
            categories,
            weights=weights,
            k=1
        )[0]

        details = expense_categories[category]

        expense_date = start_date + timedelta(
            days=random.randint(0, date_range)
        )

        month = expense_date.month

        amount = random.uniform(
            details["amount"][0],
            details["amount"][1]
        )

        if category == "Utilities":
            amount *= random.uniform(0.90, 1.15)

        elif category == "Salaries & Wages":
            amount *= random.uniform(0.85, 1.10)

        elif category == "Marketing":
            if month in [11, 12]:
                amount *= random.uniform(1.15, 1.45)
            else:
                amount *= random.uniform(0.80, 1.10)

        elif category == "Raw Materials":
            if month in [1, 2]:
                amount *= random.uniform(0.90, 1.00)

        elif category == "Transport & Logistics":
            amount *= random.uniform(0.90, 1.20)

        amount = round(
            amount / 10
        ) * 10

        if amount < details["amount"][0]:
            amount = details["amount"][0]

        payment_status = random.choices(
            [
                "Paid",
                "Pending",
                "Partially Paid",
                "Overdue"
            ],
            weights=[86, 6, 5, 3],
            k=1
        )[0]

        expense_id = f"EXP{i:05d}"

        rows.append((
            expense_id,
            expense_date,
            category,
            details["department"],
            amount,
            random.choice(
                descriptions[category]
            ),
            payment_status
        ))

        if len(rows) >= 500:
            cursor.executemany("""
                INSERT INTO expenses (
                    expense_id,
                    expense_date,
                    expense_category,
                    department,
                    amount,
                    description,
                    payment_status
                )
                VALUES (
                    %s, %s, %s, %s, %s, %s, %s
                )
            """, rows)

            connection.commit()

            print(
                f"Inserted {len(rows)} expense records"
            )

            rows = []

    if rows:
        cursor.executemany("""
            INSERT INTO expenses (
                expense_id,
                expense_date,
                expense_category,
                department,
                amount,
                description,
                payment_status
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s
            )
        """, rows)

        connection.commit()

        print(
            f"Inserted {len(rows)} expense records"
        )

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM expenses
    """)

    result = cursor.fetchone()

    print()
    print("Expense generation completed.")
    print(f"Total expense records: {result[0]}")

    cursor.close()
    connection.close()

except Error as e:
    print(f"MySQL Error: {e}")

except Exception as e:
    print(f"Error: {e}")

