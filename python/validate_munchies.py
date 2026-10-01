
import mysql.connector
from mysql.connector import Error

DB_NAME = "munchies"
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "password"

try:
    connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    cursor = connection.cursor()

    print("=" * 70)
    print("MUNCHIES DATABASE VALIDATION")
    print("=" * 70)

    tables = [
        "products",
        "customers",
        "suppliers",
        "raw_materials",
        "purchases",
        "production",
        "bill_of_materials",
        "inventory",
        "sales",
        "deliveries",
        "quality_returns",
        "expenses"
    ]

    print()
    print("1. ROW COUNTS")
    print("-" * 70)

    for table in tables:
        cursor.execute(
            f"SELECT COUNT(*) FROM {table}"
        )

        count = cursor.fetchone()[0]

        print(f"{table:<25} {count:>10,}")

    print()
    print("2. DUPLICATE PRIMARY KEYS")
    print("-" * 70)

    primary_keys = {
        "products": "product_id",
        "customers": "customer_id",
        "suppliers": "supplier_id",
        "raw_materials": "material_id",
        "purchases": "purchase_id",
        "production": "production_id",
        "bill_of_materials": "bom_id",
        "inventory": "inventory_id",
        "sales": "sale_id",
        "deliveries": "delivery_id",
        "quality_returns": "quality_return_id",
        "expenses": "expense_id"
    }

    for table, primary_key in primary_keys.items():
        cursor.execute(f"""
            SELECT COUNT(*)
            FROM {table}
        """)

        total = cursor.fetchone()[0]

        cursor.execute(f"""
            SELECT COUNT(DISTINCT {primary_key})
            FROM {table}
        """)

        unique = cursor.fetchone()[0]

        duplicates = total - unique

        status = "PASS" if duplicates == 0 else "FAIL"

        print(
            f"{table:<25} "
            f"{status:<6} "
            f"duplicates: {duplicates}"
        )

    print()
    print("3. FOREIGN KEY CHECKS")
    print("-" * 70)

    foreign_key_checks = [
        (
            "purchases → suppliers",
            """
            SELECT COUNT(*)
            FROM purchases p
            LEFT JOIN suppliers s
                ON p.supplier_id = s.supplier_id
            WHERE s.supplier_id IS NULL
            """
        ),
        (
            "purchases → raw_materials",
            """
            SELECT COUNT(*)
            FROM purchases p
            LEFT JOIN raw_materials r
                ON p.material_id = r.material_id
            WHERE r.material_id IS NULL
            """
        ),
        (
            "production → products",
            """
            SELECT COUNT(*)
            FROM production p
            LEFT JOIN products pr
                ON p.product_id = pr.product_id
            WHERE pr.product_id IS NULL
            """
        ),
        (
            "BOM → products",
            """
            SELECT COUNT(*)
            FROM bill_of_materials b
            LEFT JOIN products p
                ON b.product_id = p.product_id
            WHERE p.product_id IS NULL
            """
        ),
        (
            "BOM → raw_materials",
            """
            SELECT COUNT(*)
            FROM bill_of_materials b
            LEFT JOIN raw_materials r
                ON b.material_id = r.material_id
            WHERE r.material_id IS NULL
            """
        ),
        (
            "inventory → products",
            """
            SELECT COUNT(*)
            FROM inventory i
            LEFT JOIN products p
                ON i.product_id = p.product_id
            WHERE p.product_id IS NULL
            """
        ),
        (
            "sales → customers",
            """
            SELECT COUNT(*)
            FROM sales s
            LEFT JOIN customers c
                ON s.customer_id = c.customer_id
            WHERE c.customer_id IS NULL
            """
        ),
        (
            "sales → products",
            """
            SELECT COUNT(*)
            FROM sales s
            LEFT JOIN products p
                ON s.product_id = p.product_id
            WHERE p.product_id IS NULL
            """
        ),
        (
            "deliveries → sales",
            """
            SELECT COUNT(*)
            FROM deliveries d
            LEFT JOIN sales s
                ON d.sale_id = s.sale_id
            WHERE s.sale_id IS NULL
            """
        ),
        (
            "deliveries → customers",
            """
            SELECT COUNT(*)
            FROM deliveries d
            LEFT JOIN customers c
                ON d.customer_id = c.customer_id
            WHERE c.customer_id IS NULL
            """
        ),
        (
            "deliveries → products",
            """
            SELECT COUNT(*)
            FROM deliveries d
            LEFT JOIN products p
                ON d.product_id = p.product_id
            WHERE p.product_id IS NULL
            """
        ),
        (
            "returns → products",
            """
            SELECT COUNT(*)
            FROM quality_returns q
            LEFT JOIN products p
                ON q.product_id = p.product_id
            WHERE p.product_id IS NULL
            """
        ),
        (
            "returns → customers",
            """
            SELECT COUNT(*)
            FROM quality_returns q
            LEFT JOIN customers c
                ON q.customer_id = c.customer_id
            WHERE q.customer_id IS NOT NULL
              AND c.customer_id IS NULL
            """
        )
    ]

    for name, query in foreign_key_checks:
        cursor.execute(query)

        broken = cursor.fetchone()[0]

        status = "PASS" if broken == 0 else "FAIL"

        print(
            f"{name:<30} "
            f"{status:<6} "
            f"broken: {broken}"
        )

    print()
    print("4. IMPORTANT NULL CHECKS")
    print("-" * 70)

    null_checks = [
        ("products.product_name", "products", "product_name"),
        ("products.unit_price", "products", "unit_price"),
        ("customers.customer_name", "customers", "customer_name"),
        ("suppliers.supplier_name", "suppliers", "supplier_name"),
        ("raw_materials.material_name", "raw_materials", "material_name"),
        ("sales.sale_date", "sales", "sale_date"),
        ("sales.quantity", "sales", "quantity"),
        ("sales.revenue", "sales", "revenue"),
        ("production.production_date", "production", "production_date"),
        ("inventory.snapshot_date", "inventory", "snapshot_date"),
        ("expenses.expense_date", "expenses", "expense_date"),
        ("expenses.amount", "expenses", "amount")
    ]

    for name, table, column in null_checks:
        cursor.execute(f"""
            SELECT COUNT(*)
            FROM {table}
            WHERE {column} IS NULL
        """)

        nulls = cursor.fetchone()[0]

        status = "PASS" if nulls == 0 else "CHECK"

        print(
            f"{name:<35} "
            f"{status:<7} "
            f"nulls: {nulls}"
        )

    print()
    print("5. NEGATIVE VALUE CHECKS")
    print("-" * 70)

    negative_checks = [
        (
            "Purchases quantity",
            "SELECT COUNT(*) FROM purchases WHERE quantity_ordered < 0"
        ),
        (
            "Purchases cost",
            "SELECT COUNT(*) FROM purchases WHERE total_cost < 0"
        ),
        (
            "Production planned",
            "SELECT COUNT(*) FROM production WHERE planned_quantity < 0"
        ),
        (
            "Production produced",
            "SELECT COUNT(*) FROM production WHERE produced_quantity < 0"
        ),
        (
            "Inventory closing",
            "SELECT COUNT(*) FROM inventory WHERE closing_stock < 0"
        ),
        (
            "Sales quantity",
            "SELECT COUNT(*) FROM sales WHERE quantity < 0"
        ),
        (
            "Sales revenue",
            "SELECT COUNT(*) FROM sales WHERE revenue < 0"
        ),
        (
            "Sales cost",
            "SELECT COUNT(*) FROM sales WHERE cost < 0"
        ),
        (
            "Expenses amount",
            "SELECT COUNT(*) FROM expenses WHERE amount < 0"
        ),
        (
            "Returns quantity",
            "SELECT COUNT(*) FROM quality_returns WHERE quantity < 0"
        )
    ]

    for name, query in negative_checks:
        cursor.execute(query)

        count = cursor.fetchone()[0]

        status = "PASS" if count == 0 else "FAIL"

        print(
            f"{name:<30} "
            f"{status:<6} "
            f"negative: {count}"
        )

    print()
    print("6. SALES CALCULATIONS")
    print("-" * 70)

    cursor.execute("""
        SELECT COUNT(*)
        FROM sales
        WHERE invoice_status != 'Cancelled'
          AND ABS(
              revenue -
              ((quantity * unit_price) - discount)
          ) > 0.05
    """)

    sales_revenue_errors = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM sales
        WHERE ABS(
            profit - (revenue - cost)
        ) > 0.05
    """)

    sales_profit_errors = cursor.fetchone()[0]

    print(
        f"Revenue calculation errors: {sales_revenue_errors}"
    )

    print(
        f"Profit calculation errors:  {sales_profit_errors}"
    )

    print()
    print("7. INVENTORY CALCULATIONS")
    print("-" * 70)

    cursor.execute("""
        SELECT COUNT(*)
        FROM inventory
        WHERE ABS(
            closing_stock -
            GREATEST(
                opening_stock +
                production_received -
                units_sold -
                damaged_units,
                0
            )
        ) > 0.05
    """)

    inventory_errors = cursor.fetchone()[0]

    print(
        f"Inventory calculation errors: {inventory_errors}"
    )

    print()
    print("8. PRODUCTION CHECKS")
    print("-" * 70)

    cursor.execute("""
        SELECT COUNT(*)
        FROM production
        WHERE rejected_quantity > produced_quantity
    """)

    production_errors = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM production
        WHERE production_status = 'Cancelled'
          AND produced_quantity != 0
    """)

    cancelled_errors = cursor.fetchone()[0]

    print(
        f"Rejected > produced:       {production_errors}"
    )

    print(
        f"Cancelled with production: {cancelled_errors}"
    )

    print()
    print("9. DELIVERY DATE CHECKS")
    print("-" * 70)

    cursor.execute("""
        SELECT COUNT(*)
        FROM deliveries
        WHERE delivery_date IS NOT NULL
          AND delivery_date < shipment_date
    """)

    delivery_date_errors = cursor.fetchone()[0]

    print(
        f"Delivery before shipment: {delivery_date_errors}"
    )

    print()
    print("10. DATE RANGE CHECKS")
    print("-" * 70)

    date_checks = [
        (
            "Sales outside 2023-2025",
            """
            SELECT COUNT(*)
            FROM sales
            WHERE sale_date < '2023-01-01'
               OR sale_date > '2025-12-31'
            """
        ),
        (
            "Production outside 2023-2025",
            """
            SELECT COUNT(*)
            FROM production
            WHERE production_date < '2023-01-01'
               OR production_date > '2025-12-31'
            """
        ),
        (
            "Inventory outside 2023-2025",
            """
            SELECT COUNT(*)
            FROM inventory
            WHERE snapshot_date < '2023-01-01'
               OR snapshot_date > '2025-12-31'
            """
        ),
        (
            "Expenses outside 2023-2025",
            """
            SELECT COUNT(*)
            FROM expenses
            WHERE expense_date < '2023-01-01'
               OR expense_date > '2025-12-31'
            """
        )
    ]

    for name, query in date_checks:
        cursor.execute(query)

        count = cursor.fetchone()[0]

        status = "PASS" if count == 0 else "FAIL"

        print(
            f"{name:<35} "
            f"{status:<6} "
            f"invalid: {count}"
        )

    print()
    print("11. BUSINESS TOTALS")
    print("-" * 70)

    cursor.execute("""
        SELECT
            ROUND(SUM(revenue), 2),
            ROUND(SUM(cost), 2),
            ROUND(SUM(profit), 2),
            SUM(quantity)
        FROM sales
        WHERE invoice_status != 'Cancelled'
    """)

    revenue, cost, profit, units_sold = cursor.fetchone()

    print(f"Sales revenue:       K{revenue:,.2f}")
    print(f"Sales cost:          K{cost:,.2f}")
    print(f"Sales profit:        K{profit:,.2f}")
    print(f"Units sold:          {units_sold:,.0f}")

    cursor.execute("""
        SELECT
            ROUND(SUM(total_cost), 2)
        FROM purchases
        WHERE status IN ('Received', 'Partially Received')
    """)

    purchases_total = cursor.fetchone()[0]

    print(f"Purchase value:      K{purchases_total:,.2f}")

    cursor.execute("""
        SELECT
            ROUND(SUM(production_cost), 2)
        FROM production
    """)

    production_cost = cursor.fetchone()[0]

    print(f"Production cost:     K{production_cost:,.2f}")

    cursor.execute("""
        SELECT
            ROUND(SUM(amount), 2)
        FROM expenses
    """)

    expenses_total = cursor.fetchone()[0]

    print(f"Expenses:            K{expenses_total:,.2f}")

    cursor.execute("""
        SELECT
            ROUND(SUM(delivery_cost), 2)
        FROM deliveries
    """)

    delivery_cost = cursor.fetchone()[0]

    print(f"Delivery costs:      K{delivery_cost:,.2f}")

    print()
    print("=" * 70)
    print("VALIDATION COMPLETE")
    print("=" * 70)

    cursor.close()
    connection.close()

except Error as e:
    print(f"MySQL Error: {e}")

except Exception as e:
    print(f"Error: {e}")

