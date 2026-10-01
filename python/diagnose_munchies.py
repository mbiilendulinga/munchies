import mysql.connector
from decimal import Decimal

# ============================================================
# MUNCHIES POWER BI BLANK DIAGNOSTIC
# ============================================================
#
# Purpose:
# Diagnose why Power BI may show a large "(Blank)" category
# when Revenue is analysed by Product Category or Customer Type.
#
# IMPORTANT:
# - Revenue already exists in sales.revenue.
# - We therefore use SUM(s.revenue).
# - We do NOT recalculate revenue.
# - Every test runs independently.
# - If one test fails, the script continues to the next test.
#
# ============================================================


DB_NAME = "munchies"

MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "password"


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def money(value):
    """
    Safely convert a database number into Decimal.
    """
    if value is None:
        return Decimal("0")

    return Decimal(str(value))


def run_query(cursor, query):
    """
    Execute a query and return the result.

    If the query fails, return None instead of stopping
    the entire diagnostic.
    """
    try:
        cursor.execute(query)
        return cursor.fetchall()

    except mysql.connector.Error as e:

        print("\n⚠ TEST QUERY FAILED")
        print(f"MySQL Error {e.errno}: {e.msg}")
        return None

    except Exception as e:

        print("\n⚠ TEST QUERY FAILED")
        print(f"Error: {e}")
        return None


def print_header(number, title):
    """
    Print a consistent test heading.
    """
    print("\n" + "=" * 80)
    print(f"{number}. {title}")
    print("=" * 80)


# ============================================================
# CONNECT TO DATABASE
# ============================================================

try:

    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=DB_NAME
    )

    cursor = conn.cursor(dictionary=True)

except mysql.connector.Error as e:

    print("=" * 80)
    print("MUNCHIES - POWER BI BLANK DIAGNOSTIC")
    print("=" * 80)

    print("\nMYSQL CONNECTION ERROR")
    print(f"MySQL Error {e.errno}: {e.msg}")

    raise SystemExit


# ============================================================
# TITLE
# ============================================================

print("=" * 80)
print("MUNCHIES - POWER BI BLANK DIAGNOSTIC")
print("=" * 80)

print("\nDatabase:")
print(f"  {DB_NAME}")

print("\nPurpose:")
print("  Diagnose Power BI '(Blank)' revenue caused by")
print("  Product / Customer relationship or data issues.")


# ============================================================
# 1. BASIC DATA COUNTS
# ============================================================

print_header(1, "BASIC DATA COUNTS")

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

for table in tables:

    result = run_query(
        cursor,
        f"""
        SELECT COUNT(*) AS row_count
        FROM `{table}`
        """
    )

    if result is not None:

        print(
            f"{table:<25}: "
            f"{result[0]['row_count']:,}"
        )


# ============================================================
# 2. SALES → PRODUCTS MATCHING
# ============================================================

print_header(2, "SALES → PRODUCTS MATCHING")

result = run_query(
    cursor,
    """
    SELECT
        COUNT(*) AS total_sales_rows,

        COUNT(p.product_id) AS matched_sales_rows,

        COUNT(*) - COUNT(p.product_id)
            AS unmatched_sales_rows

    FROM sales s

    LEFT JOIN products p
        ON s.product_id = p.product_id
    """
)

if result is not None:

    row = result[0]

    print(
        f"Total sales rows        : "
        f"{row['total_sales_rows']:,}"
    )

    print(
        f"Matched product rows    : "
        f"{row['matched_sales_rows']:,}"
    )

    print(
        f"UNMATCHED product rows  : "
        f"{row['unmatched_sales_rows']:,}"
    )


# ============================================================
# 3. SALES → CUSTOMERS MATCHING
# ============================================================

print_header(3, "SALES → CUSTOMERS MATCHING")

result = run_query(
    cursor,
    """
    SELECT
        COUNT(*) AS total_sales_rows,

        COUNT(c.customer_id) AS matched_sales_rows,

        COUNT(*) - COUNT(c.customer_id)
            AS unmatched_sales_rows

    FROM sales s

    LEFT JOIN customers c
        ON s.customer_id = c.customer_id
    """
)

if result is not None:

    row = result[0]

    print(
        f"Total sales rows        : "
        f"{row['total_sales_rows']:,}"
    )

    print(
        f"Matched customer rows   : "
        f"{row['matched_sales_rows']:,}"
    )

    print(
        f"UNMATCHED customer rows : "
        f"{row['unmatched_sales_rows']:,}"
    )


# ============================================================
# 4. NULL FOREIGN KEYS
# ============================================================

print_header(4, "NULL FOREIGN KEYS IN SALES")

result = run_query(
    cursor,
    """
    SELECT

        SUM(
            CASE
                WHEN product_id IS NULL
                THEN 1
                ELSE 0
            END
        ) AS null_products,

        SUM(
            CASE
                WHEN customer_id IS NULL
                THEN 1
                ELSE 0
            END
        ) AS null_customers

    FROM sales
    """
)

if result is not None:

    row = result[0]

    print(
        f"NULL product_id  : "
        f"{row['null_products']:,}"
    )

    print(
        f"NULL customer_id : "
        f"{row['null_customers']:,}"
    )


# ============================================================
# 5. TOTAL SALES REVENUE
# ============================================================

print_header(5, "TOTAL SALES REVENUE")

result = run_query(
    cursor,
    """
    SELECT
        COUNT(*) AS sale_count,
        SUM(revenue) AS total_revenue

    FROM sales
    """
)

if result is not None:

    row = result[0]

    total_sales = row["sale_count"]

    total_revenue = money(
        row["total_revenue"]
    )

    print(
        f"Sales rows : "
        f"{total_sales:,}"
    )

    print(
        f"Revenue    : "
        f"{total_revenue:,.2f}"
    )


# ============================================================
# 6. REVENUE BY PRODUCT CATEGORY
# ============================================================

print_header(6, "REVENUE BY PRODUCT CATEGORY")

result = run_query(
    cursor,
    """
    SELECT

        CASE
            WHEN p.product_id IS NULL
                THEN '(NO MATCH)'
            WHEN p.category IS NULL
                THEN '(NULL CATEGORY)'
            WHEN TRIM(p.category) = ''
                THEN '(EMPTY CATEGORY)'
            ELSE p.category
        END AS category,

        COUNT(s.sale_id) AS sale_count,

        SUM(s.revenue) AS total_revenue

    FROM sales s

    LEFT JOIN products p
        ON s.product_id = p.product_id

    GROUP BY
        CASE
            WHEN p.product_id IS NULL
                THEN '(NO MATCH)'
            WHEN p.category IS NULL
                THEN '(NULL CATEGORY)'
            WHEN TRIM(p.category) = ''
                THEN '(EMPTY CATEGORY)'
            ELSE p.category
        END

    ORDER BY total_revenue DESC
    """
)

if result is not None:

    if len(result) == 0:

        print("No results found.")

    else:

        for row in result:

            print(
                f"{str(row['category']):<25}"
                f" Sales: {row['sale_count']:>8,}"
                f" Revenue: "
                f"{money(row['total_revenue']):>15,.2f}"
            )


# ============================================================
# 7. REVENUE BY CUSTOMER TYPE
# ============================================================

print_header(7, "REVENUE BY CUSTOMER TYPE")

result = run_query(
    cursor,
    """
    SELECT

        CASE
            WHEN c.customer_id IS NULL
                THEN '(NO MATCH)'
            WHEN c.customer_type IS NULL
                THEN '(NULL TYPE)'
            WHEN TRIM(c.customer_type) = ''
                THEN '(EMPTY TYPE)'
            ELSE c.customer_type
        END AS customer_type,

        COUNT(s.sale_id) AS sale_count,

        SUM(s.revenue) AS total_revenue

    FROM sales s

    LEFT JOIN customers c
        ON s.customer_id = c.customer_id

    GROUP BY
        CASE
            WHEN c.customer_id IS NULL
                THEN '(NO MATCH)'
            WHEN c.customer_type IS NULL
                THEN '(NULL TYPE)'
            WHEN TRIM(c.customer_type) = ''
                THEN '(EMPTY TYPE)'
            ELSE c.customer_type
        END

    ORDER BY total_revenue DESC
    """
)

if result is not None:

    if len(result) == 0:

        print("No results found.")

    else:

        for row in result:

            print(
                f"{str(row['customer_type']):<25}"
                f" Sales: {row['sale_count']:>8,}"
                f" Revenue: "
                f"{money(row['total_revenue']):>15,.2f}"
            )


# ============================================================
# 8. UNMATCHED PRODUCT IDs
# ============================================================

print_header(8, "UNMATCHED PRODUCT IDs")

result = run_query(
    cursor,
    """
    SELECT

        s.product_id,

        COUNT(*) AS sale_count,

        SUM(s.revenue) AS total_revenue

    FROM sales s

    LEFT JOIN products p
        ON s.product_id = p.product_id

    WHERE p.product_id IS NULL

    GROUP BY s.product_id

    ORDER BY total_revenue DESC
    """
)

if result is not None:

    if not result:

        print("✓ NO UNMATCHED PRODUCT IDs FOUND")

    else:

        print(
            f"Found {len(result):,} unmatched "
            f"Product ID(s):"
        )

        for row in result:

            print(
                f"Product ID: "
                f"{repr(row['product_id'])}"
                f" | Sales: "
                f"{row['sale_count']:,}"
                f" | Revenue: "
                f"{money(row['total_revenue']):,.2f}"
            )


# ============================================================
# 9. UNMATCHED CUSTOMER IDs
# ============================================================

print_header(9, "UNMATCHED CUSTOMER IDs")

result = run_query(
    cursor,
    """
    SELECT

        s.customer_id,

        COUNT(*) AS sale_count,

        SUM(s.revenue) AS total_revenue

    FROM sales s

    LEFT JOIN customers c
        ON s.customer_id = c.customer_id

    WHERE c.customer_id IS NULL

    GROUP BY s.customer_id

    ORDER BY total_revenue DESC
    """
)

if result is not None:

    if not result:

        print("✓ NO UNMATCHED CUSTOMER IDs FOUND")

    else:

        print(
            f"Found {len(result):,} unmatched "
            f"Customer ID(s):"
        )

        for row in result:

            print(
                f"Customer ID: "
                f"{repr(row['customer_id'])}"
                f" | Sales: "
                f"{row['sale_count']:,}"
                f" | Revenue: "
                f"{money(row['total_revenue']):,.2f}"
            )


# ============================================================
# 10. PRODUCT ID FORMAT CHECK
# ============================================================

print_header(10, "PRODUCT ID FORMAT CHECK")

print("\nProducts table:")

result = run_query(
    cursor,
    """
    SELECT product_id
    FROM products
    WHERE product_id <> TRIM(product_id)
    """
)

if result is not None:

    if not result:

        print("  ✓ No leading/trailing spaces")

    else:

        print(
            f"  ⚠ {len(result):,} Product ID(s) "
            f"contain leading/trailing spaces:"
        )

        for row in result:

            print(
                f"    {repr(row['product_id'])}"
            )


print("\nSales table:")

result = run_query(
    cursor,
    """
    SELECT product_id
    FROM sales
    WHERE product_id <> TRIM(product_id)
    """
)

if result is not None:

    if not result:

        print("  ✓ No leading/trailing spaces")

    else:

        print(
            f"  ⚠ {len(result):,} Sales Product ID(s) "
            f"contain leading/trailing spaces:"
        )

        for row in result:

            print(
                f"    {repr(row['product_id'])}"
            )


# ============================================================
# 11. CUSTOMER ID FORMAT CHECK
# ============================================================

print_header(11, "CUSTOMER ID FORMAT CHECK")

print("\nCustomers table:")

result = run_query(
    cursor,
    """
    SELECT customer_id
    FROM customers
    WHERE customer_id <> TRIM(customer_id)
    """
)

if result is not None:

    if not result:

        print("  ✓ No leading/trailing spaces")

    else:

        print(
            f"  ⚠ {len(result):,} Customer ID(s) "
            f"contain leading/trailing spaces:"
        )

        for row in result:

            print(
                f"    {repr(row['customer_id'])}"
            )


print("\nSales table:")

result = run_query(
    cursor,
    """
    SELECT customer_id
    FROM sales
    WHERE customer_id <> TRIM(customer_id)
    """
)

if result is not None:

    if not result:

        print("  ✓ No leading/trailing spaces")

    else:

        print(
            f"  ⚠ {len(result):,} Sales Customer ID(s) "
            f"contain leading/trailing spaces:"
        )

        for row in result:

            print(
                f"    {repr(row['customer_id'])}"
            )


# ============================================================
# 12. PRODUCT CATEGORY QUALITY
# ============================================================

print_header(12, "PRODUCT CATEGORY QUALITY")

result = run_query(
    cursor,
    """
    SELECT

        SUM(
            CASE
                WHEN category IS NULL
                THEN 1
                ELSE 0
            END
        ) AS null_categories,

        SUM(
            CASE
                WHEN category IS NOT NULL
                     AND TRIM(category) = ''
                THEN 1
                ELSE 0
            END
        ) AS empty_categories

    FROM products
    """
)

if result is not None:

    row = result[0]

    print(
        f"NULL categories  : "
        f"{row['null_categories']:,}"
    )

    print(
        f"Empty categories : "
        f"{row['empty_categories']:,}"
    )


# ============================================================
# 13. CUSTOMER TYPE QUALITY
# ============================================================

print_header(13, "CUSTOMER TYPE QUALITY")

result = run_query(
    cursor,
    """
    SELECT

        SUM(
            CASE
                WHEN customer_type IS NULL
                THEN 1
                ELSE 0
            END
        ) AS null_types,

        SUM(
            CASE
                WHEN customer_type IS NOT NULL
                     AND TRIM(customer_type) = ''
                THEN 1
                ELSE 0
            END
        ) AS empty_types

    FROM customers
    """
)

if result is not None:

    row = result[0]

    print(
        f"NULL customer types  : "
        f"{row['null_types']:,}"
    )

    print(
        f"Empty customer types : "
        f"{row['empty_types']:,}"
    )


# ============================================================
# 14. DISTINCT IDs USED IN SALES
# ============================================================

print_header(14, "DISTINCT IDs USED IN SALES")

# Products in Products table
result = run_query(
    cursor,
    """
    SELECT COUNT(*) AS product_count
    FROM products
    """
)

if result is not None:

    product_count = result[0]["product_count"]

else:

    product_count = 0


# Distinct products used in Sales
result = run_query(
    cursor,
    """
    SELECT COUNT(DISTINCT product_id) AS products_used
    FROM sales
    """
)

if result is not None:

    products_used = result[0]["products_used"]

else:

    products_used = 0


# Customers in Customers table
result = run_query(
    cursor,
    """
    SELECT COUNT(*) AS customer_count
    FROM customers
    """
)

if result is not None:

    customer_count = result[0]["customer_count"]

else:

    customer_count = 0


# Distinct customers used in Sales
result = run_query(
    cursor,
    """
    SELECT COUNT(DISTINCT customer_id) AS customers_used
    FROM sales
    """
)

if result is not None:

    customers_used = result[0]["customers_used"]

else:

    customers_used = 0


print(
    f"Products in Products table : "
    f"{product_count:,}"
)

print(
    f"Products used in Sales      : "
    f"{products_used:,}"
)

print()

print(
    f"Customers in Customers table: "
    f"{customer_count:,}"
)

print(
    f"Customers used in Sales     : "
    f"{customers_used:,}"
)


# ============================================================
# 15. CRITICAL POWER BI BLANK TEST
# ============================================================

print_header(15, "CRITICAL POWER BI BLANK TEST")

result = run_query(
    cursor,
    """
    SELECT

        SUM(s.revenue)
            AS total_revenue,

        SUM(
            CASE
                WHEN p.product_id IS NULL
                THEN s.revenue
                ELSE 0
            END
        )
            AS unmatched_product_revenue,

        SUM(
            CASE
                WHEN c.customer_id IS NULL
                THEN s.revenue
                ELSE 0
            END
        )
            AS unmatched_customer_revenue

    FROM sales s

    LEFT JOIN products p
        ON s.product_id = p.product_id

    LEFT JOIN customers c
        ON s.customer_id = c.customer_id
    """
)

if result is not None:

    row = result[0]

    total = money(
        row["total_revenue"]
    )

    unmatched_product = money(
        row["unmatched_product_revenue"]
    )

    unmatched_customer = money(
        row["unmatched_customer_revenue"]
    )

    print(
        f"Total revenue            : "
        f"{total:,.2f}"
    )

    print(
        f"Revenue with NO product  : "
        f"{unmatched_product:,.2f}"
    )

    print(
        f"Revenue with NO customer : "
        f"{unmatched_customer:,.2f}"
    )


# ============================================================
# 16. FINAL DIAGNOSIS
# ============================================================

print_header(16, "FINAL DIAGNOSIS")

# Run the critical test again so this section can make
# a definitive diagnosis.

result = run_query(
    cursor,
    """
    SELECT

        COUNT(*) AS sales_count,

        SUM(s.revenue)
            AS total_revenue,

        SUM(
            CASE
                WHEN p.product_id IS NULL
                THEN 1
                ELSE 0
            END
        )
            AS unmatched_product_rows,

        SUM(
            CASE
                WHEN p.product_id IS NULL
                THEN s.revenue
                ELSE 0
            END
        )
            AS unmatched_product_revenue,

        SUM(
            CASE
                WHEN c.customer_id IS NULL
                THEN 1
                ELSE 0
            END
        )
            AS unmatched_customer_rows,

        SUM(
            CASE
                WHEN c.customer_id IS NULL
                THEN s.revenue
                ELSE 0
            END
        )
            AS unmatched_customer_revenue

    FROM sales s

    LEFT JOIN products p
        ON s.product_id = p.product_id

    LEFT JOIN customers c
        ON s.customer_id = c.customer_id
    """
)

if result is not None:

    row = result[0]

    total_revenue = money(
        row["total_revenue"]
    )

    unmatched_product_revenue = money(
        row["unmatched_product_revenue"]
    )

    unmatched_customer_revenue = money(
        row["unmatched_customer_revenue"]
    )

    unmatched_product_rows = (
        row["unmatched_product_rows"]
    )

    unmatched_customer_rows = (
        row["unmatched_customer_rows"]
    )


    print("\nSALES → PRODUCTS")

    if unmatched_product_rows == 0:

        print(
            "  ✓ Every Sales row matches "
            "a Products record."
        )

        print(
            "  ✓ Product relationship data looks valid."
        )

    else:

        print(
            "  ⚠ UNMATCHED PRODUCT RECORDS FOUND"
        )

        print(
            f"  Unmatched rows   : "
            f"{unmatched_product_rows:,}"
        )

        print(
            f"  Unmatched revenue: "
            f"{unmatched_product_revenue:,.2f}"
        )


    print("\nSALES → CUSTOMERS")

    if unmatched_customer_rows == 0:

        print(
            "  ✓ Every Sales row matches "
            "a Customers record."
        )

        print(
            "  ✓ Customer relationship data looks valid."
        )

    else:

        print(
            "  ⚠ UNMATCHED CUSTOMER RECORDS FOUND"
        )

        print(
            f"  Unmatched rows   : "
            f"{unmatched_customer_rows:,}"
        )

        print(
            f"  Unmatched revenue: "
            f"{unmatched_customer_revenue:,.2f}"
        )


    print("\nOVERALL RESULT")

    if (
        unmatched_product_rows == 0
        and unmatched_customer_rows == 0
    ):

        print(
            "  ✓ MYSQL DATA PASSES THE FOREIGN-KEY TEST."
        )

        print()
        print(
            "  There are no orphaned Sales Product IDs"
        )

        print(
            "  and no orphaned Sales Customer IDs."
        )

        print()
        print(
            "  If Power BI still displays a large"
        )

        print(
            "  '(Blank)' category, investigate the"
        )

        print(
            "  Power BI model/relationships, imported"
        )

        print(
            "  data, or data refresh next."
        )

    else:

        print(
            "  ⚠ MYSQL DATA HAS UNMATCHED SALES."
        )

        print()
        print(
            "  This can legitimately produce"
        )

        print(
            "  '(Blank)' categories in Power BI."
        )


# ============================================================
# CLOSE CONNECTION
# ============================================================

try:
    cursor.close()
except:
    pass

try:
    conn.close()
except:
    pass


# ============================================================
# COMPLETE
# ============================================================

print("\n" + "=" * 80)
print("DIAGNOSTIC COMPLETE")
print("=" * 80)

print("\nAll 16 diagnostic sections have been processed.")
print("Review the results above.")