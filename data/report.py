import mysql.connector
from mysql.connector import Error
from decimal import Decimal

DB_NAME = "munchies"
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "password"


def fmt(value):
    if value is None:
        return "NULL"
    if isinstance(value, Decimal):
        return f"{float(value):,.2f}"
    if isinstance(value, float):
        return f"{value:,.2f}"
    if isinstance(value, int):
        return f"{value:,}"
    return str(value)


def run_query(cursor, title, query):
    print(f"\n{'=' * 70}")
    print(title)
    print('=' * 70)

    cursor.execute(query)
    rows = cursor.fetchall()

    if not rows:
        print("No results.")
        return

    columns = [desc[0] for desc in cursor.description]

    print(" | ".join(columns))
    print("-" * 70)

    for row in rows:
        print(" | ".join(fmt(value) for value in row))


def main():
    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=DB_NAME
        )

        cursor = connection.cursor()

        output = []

        def capture(title, query):
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            output.append("\n" + "=" * 80)
            output.append(title)
            output.append("=" * 80)

            if not rows:
                output.append("No results.")
                return

            output.append(" | ".join(columns))
            output.append("-" * 80)

            for row in rows:
                output.append(" | ".join(fmt(value) for value in row))

        output.append("MUNCHIES POWER BI REPORT DATA")
        output.append("=" * 80)
        output.append("Database: munchies")
        output.append("Purpose: Supporting data for Power BI documentation and GitHub project files.")

        # ============================================================
        # 1. DATABASE OVERVIEW
        # ============================================================

        capture(
            "DATABASE TABLES AND ROW COUNTS",
            """
            SELECT 'products' AS table_name, COUNT(*) AS row_count FROM products
            UNION ALL
            SELECT 'customers', COUNT(*) FROM customers
            UNION ALL
            SELECT 'suppliers', COUNT(*) FROM suppliers
            UNION ALL
            SELECT 'raw_materials', COUNT(*) FROM raw_materials
            UNION ALL
            SELECT 'purchases', COUNT(*) FROM purchases
            UNION ALL
            SELECT 'production', COUNT(*) FROM production
            UNION ALL
            SELECT 'bill_of_materials', COUNT(*) FROM bill_of_materials
            UNION ALL
            SELECT 'inventory', COUNT(*) FROM inventory
            UNION ALL
            SELECT 'sales', COUNT(*) FROM sales
            UNION ALL
            SELECT 'deliveries', COUNT(*) FROM deliveries
            UNION ALL
            SELECT 'quality_returns', COUNT(*) FROM quality_returns
            UNION ALL
            SELECT 'expenses', COUNT(*) FROM expenses
            """
        )

        capture(
            "OVERALL DATE RANGE",
            """
            SELECT
                MIN(min_date) AS earliest_date,
                MAX(max_date) AS latest_date
            FROM (
                SELECT MIN(sale_date) AS min_date, MAX(sale_date) AS max_date FROM sales
                UNION ALL
                SELECT MIN(production_date), MAX(production_date) FROM production
                UNION ALL
                SELECT MIN(snapshot_date), MAX(snapshot_date) FROM inventory
                UNION ALL
                SELECT MIN(order_date), MAX(order_date) FROM purchases
                UNION ALL
                SELECT MIN(event_date), MAX(event_date) FROM quality_returns
                UNION ALL
                SELECT MIN(expense_date), MAX(expense_date) FROM expenses
                UNION ALL
                SELECT MIN(shipment_date), MAX(shipment_date) FROM deliveries
            ) dates
            """
        )

        # ============================================================
        # 2. EXECUTIVE SUMMARY
        # ============================================================

        capture(
            "EXECUTIVE SUMMARY KPIs",
            """
            SELECT
                (SELECT SUM(revenue) FROM sales) AS total_revenue,
                (SELECT SUM(cost) FROM sales) AS total_cost,
                (SELECT SUM(profit) FROM sales) AS total_profit,
                (SELECT
                    CASE
                        WHEN SUM(revenue) = 0 THEN 0
                        ELSE SUM(profit) / SUM(revenue) * 100
                    END
                 FROM sales) AS overall_profit_margin,
                (SELECT SUM(quantity) FROM sales) AS units_sold,
                (SELECT COUNT(DISTINCT customer_id) FROM sales) AS active_buying_customers,
                (SELECT COUNT(DISTINCT product_id) FROM sales) AS products_sold
            """
        )

        capture(
            "REVENUE BY SALES CHANNEL",
            """
            SELECT
                sales_channel,
                SUM(revenue) AS revenue,
                SUM(profit) AS profit,
                CASE
                    WHEN SUM(revenue) = 0 THEN 0
                    ELSE SUM(profit) / SUM(revenue) * 100
                END AS profit_margin
            FROM sales
            GROUP BY sales_channel
            ORDER BY revenue DESC
            """
        )

        capture(
            "PROFIT BY CATEGORY",
            """
            SELECT
                p.category,
                SUM(s.revenue) AS revenue,
                SUM(s.cost) AS cost,
                SUM(s.profit) AS profit,
                CASE
                    WHEN SUM(s.revenue) = 0 THEN 0
                    ELSE SUM(s.profit) / SUM(s.revenue) * 100
                END AS profit_margin
            FROM sales s
            JOIN products p ON s.product_id = p.product_id
            GROUP BY p.category
            ORDER BY profit DESC
            """
        )

        capture(
            "REVENUE VS PROFIT BY YEAR",
            """
            SELECT
                YEAR(sale_date) AS year,
                SUM(revenue) AS revenue,
                SUM(profit) AS profit,
                SUM(cost) AS cost
            FROM sales
            GROUP BY YEAR(sale_date)
            ORDER BY year
            """
        )

        capture(
            "REVENUE TREND",
            """
            SELECT
                YEAR(sale_date) AS year,
                MONTH(sale_date) AS month,
                DATE_FORMAT(sale_date, '%Y-%m') AS period,
                SUM(revenue) AS revenue
            FROM sales
            GROUP BY YEAR(sale_date), MONTH(sale_date), DATE_FORMAT(sale_date, '%Y-%m')
            ORDER BY year, month
            """
        )

        # ============================================================
        # 3. SALES AND PROFITABILITY
        # ============================================================

        capture(
            "MONTHLY REVENUE",
            """
            SELECT
                DATE_FORMAT(sale_date, '%Y-%m') AS month,
                SUM(revenue) AS revenue
            FROM sales
            GROUP BY DATE_FORMAT(sale_date, '%Y-%m')
            ORDER BY month
            """
        )

        capture(
            "TOTAL REVENUE BY CUSTOMER TYPE",
            """
            SELECT
                c.customer_type,
                SUM(s.revenue) AS revenue,
                SUM(s.profit) AS profit
            FROM sales s
            JOIN customers c ON s.customer_id = c.customer_id
            GROUP BY c.customer_type
            ORDER BY revenue DESC
            """
        )

        capture(
            "PROFIT MARGIN BY CATEGORY",
            """
            SELECT
                p.category,
                SUM(s.revenue) AS revenue,
                SUM(s.profit) AS profit,
                CASE
                    WHEN SUM(s.revenue) = 0 THEN 0
                    ELSE SUM(s.profit) / SUM(s.revenue) * 100
                END AS profit_margin
            FROM sales s
            JOIN products p ON s.product_id = p.product_id
            GROUP BY p.category
            ORDER BY profit_margin DESC
            """
        )

        capture(
            "TOTAL REVENUE BY PRODUCT",
            """
            SELECT
                p.product_name,
                SUM(s.revenue) AS revenue
            FROM sales s
            JOIN products p ON s.product_id = p.product_id
            GROUP BY p.product_id, p.product_name
            ORDER BY revenue DESC
            """
        )

        capture(
            "SALES PROFIT BY MONTH",
            """
            SELECT
                DATE_FORMAT(sale_date, '%Y-%m') AS month,
                SUM(revenue) AS revenue,
                SUM(profit) AS profit
            FROM sales
            GROUP BY DATE_FORMAT(sale_date, '%Y-%m')
            ORDER BY month
            """
        )

        capture(
            "TOTAL PROFIT BY SUBCATEGORY",
            """
            SELECT
                COALESCE(p.subcategory, 'Unclassified') AS subcategory,
                SUM(s.profit) AS profit,
                SUM(s.revenue) AS revenue
            FROM sales s
            JOIN products p ON s.product_id = p.product_id
            GROUP BY p.subcategory
            ORDER BY profit DESC
            """
        )

        # ============================================================
        # 4. PRODUCT PERFORMANCE
        # ============================================================

        capture(
            "PRODUCT PERFORMANCE",
            """
            SELECT
                p.product_name,
                p.category,
                COALESCE(p.subcategory, 'Unclassified') AS subcategory,
                SUM(s.quantity) AS units_sold,
                SUM(s.revenue) AS revenue,
                SUM(s.cost) AS cost_of_goods,
                SUM(s.profit) AS gross_profit,
                CASE
                    WHEN SUM(s.revenue) = 0 THEN 0
                    ELSE SUM(s.profit) / SUM(s.revenue) * 100
                END AS profit_margin
            FROM sales s
            JOIN products p ON s.product_id = p.product_id
            GROUP BY p.product_id, p.product_name, p.category, p.subcategory
            ORDER BY revenue DESC
            """
        )

        capture(
            "REVENUE BY CATEGORY AND SUBCATEGORY",
            """
            SELECT
                p.category,
                COALESCE(p.subcategory, 'Unclassified') AS subcategory,
                SUM(s.revenue) AS revenue,
                SUM(s.profit) AS profit
            FROM sales s
            JOIN products p ON s.product_id = p.product_id
            GROUP BY p.category, p.subcategory
            ORDER BY p.category, revenue DESC
            """
        )

        # ============================================================
        # 5. CUSTOMER ANALYTICS
        # ============================================================

        capture(
            "CUSTOMER REVENUE ANALYSIS",
            """
            SELECT
                c.customer_type,
                COUNT(DISTINCT c.customer_id) AS customers,
                SUM(s.revenue) AS revenue,
                SUM(s.profit) AS profit,
                SUM(s.quantity) AS units_sold
            FROM customers c
            JOIN sales s ON c.customer_id = s.customer_id
            GROUP BY c.customer_type
            ORDER BY revenue DESC
            """
        )

        capture(
            "REVENUE BY CITY",
            """
            SELECT
                c.city,
                SUM(s.revenue) AS revenue,
                SUM(s.profit) AS profit,
                COUNT(DISTINCT c.customer_id) AS customers
            FROM sales s
            JOIN customers c ON s.customer_id = c.customer_id
            GROUP BY c.city
            ORDER BY revenue DESC
            """
        )

        capture(
            "REVENUE BY REGION",
            """
            SELECT
                c.region,
                SUM(s.revenue) AS revenue,
                SUM(s.profit) AS profit,
                COUNT(DISTINCT c.customer_id) AS customers
            FROM sales s
            JOIN customers c ON s.customer_id = c.customer_id
            GROUP BY c.region
            ORDER BY revenue DESC
            """
        )

        capture(
            "CUSTOMER REVENUE DISTRIBUTION",
            """
            SELECT
                c.customer_id,
                c.customer_name,
                c.customer_type,
                c.city,
                c.region,
                SUM(s.revenue) AS revenue,
                SUM(s.profit) AS profit
            FROM customers c
            JOIN sales s ON c.customer_id = s.customer_id
            GROUP BY
                c.customer_id,
                c.customer_name,
                c.customer_type,
                c.city,
                c.region
            ORDER BY revenue DESC
            """
        )

        # ============================================================
        # 6. PRODUCTION PERFORMANCE
        # ============================================================

        capture(
            "PLANNED VS ACTUAL PRODUCTION BY YEAR",
            """
            SELECT
                YEAR(production_date) AS year,
                SUM(planned_quantity) AS planned_production,
                SUM(produced_quantity) AS actual_production,
                SUM(produced_quantity) - SUM(planned_quantity) AS production_variance,
                CASE
                    WHEN SUM(planned_quantity) = 0 THEN 0
                    ELSE SUM(produced_quantity) / SUM(planned_quantity) * 100
                END AS production_achievement_rate
            FROM production
            GROUP BY YEAR(production_date)
            ORDER BY year
            """
        )

        capture(
            "ACTUAL PRODUCTION BY FACTORY",
            """
            SELECT
                factory_name,
                SUM(produced_quantity) AS actual_production,
                SUM(planned_quantity) AS planned_production,
                SUM(rejected_quantity) AS rejected_units,
                SUM(downtime_hours) AS downtime_hours,
                SUM(production_cost) AS production_cost
            FROM production
            GROUP BY factory_name
            ORDER BY actual_production DESC
            """
        )

        capture(
            "DOWNTIME TREND",
            """
            SELECT
                YEAR(production_date) AS year,
                MONTH(production_date) AS month,
                DATE_FORMAT(production_date, '%Y-%m') AS period,
                SUM(downtime_hours) AS downtime_hours
            FROM production
            GROUP BY
                YEAR(production_date),
                MONTH(production_date),
                DATE_FORMAT(production_date, '%Y-%m')
            ORDER BY year, month
            """
        )

        capture(
            "ACTUAL PRODUCTION BY PRODUCT",
            """
            SELECT
                p.product_name,
                p.category,
                SUM(pr.produced_quantity) AS actual_production,
                SUM(pr.planned_quantity) AS planned_production,
                SUM(pr.rejected_quantity) AS rejected_units
            FROM production pr
            JOIN products p ON pr.product_id = p.product_id
            GROUP BY p.product_id, p.product_name, p.category
            ORDER BY actual_production DESC
            """
        )

        capture(
            "REJECTION RATE BY PRODUCT",
            """
            SELECT
                p.product_name,
                SUM(pr.produced_quantity) AS produced_quantity,
                SUM(pr.rejected_quantity) AS rejected_quantity,
                CASE
                    WHEN SUM(pr.produced_quantity) = 0 THEN 0
                    ELSE SUM(pr.rejected_quantity) / SUM(pr.produced_quantity) * 100
                END AS rejection_rate
            FROM production pr
            JOIN products p ON pr.product_id = p.product_id
            GROUP BY p.product_id, p.product_name
            ORDER BY rejection_rate DESC
            """
        )

        capture(
            "PRODUCTION COST",
            """
            SELECT
                YEAR(production_date) AS year,
                SUM(production_cost) AS production_cost,
                SUM(produced_quantity) AS produced_quantity,
                CASE
                    WHEN SUM(produced_quantity) = 0 THEN 0
                    ELSE SUM(production_cost) / SUM(produced_quantity)
                END AS cost_per_unit
            FROM production
            GROUP BY YEAR(production_date)
            ORDER BY year
            """
        )

        # ============================================================
        # 7. INVENTORY MANAGEMENT
        # ============================================================

        capture(
            "STOCK VALUE BY WAREHOUSE",
            """
            SELECT
                warehouse_name,
                warehouse_type,
                warehouse_city,
                SUM(stock_value) AS stock_value,
                SUM(closing_stock) AS closing_stock,
                SUM(damaged_units) AS damaged_units
            FROM inventory
            GROUP BY warehouse_name, warehouse_type, warehouse_city
            ORDER BY stock_value DESC
            """
        )

        capture(
            "WAREHOUSE BY PRODUCT",
            """
            SELECT
                warehouse_name,
                p.product_name,
                SUM(i.closing_stock) AS closing_stock,
                SUM(i.stock_value) AS stock_value,
                SUM(i.damaged_units) AS damaged_units
            FROM inventory i
            JOIN products p ON i.product_id = p.product_id
            GROUP BY warehouse_name, p.product_id, p.product_name
            ORDER BY warehouse_name, stock_value DESC
            """
        )

        capture(
            "CLOSING STOCK TREND",
            """
            SELECT
                YEAR(snapshot_date) AS year,
                MONTH(snapshot_date) AS month,
                DATE_FORMAT(snapshot_date, '%Y-%m') AS period,
                SUM(closing_stock) AS closing_stock,
                SUM(stock_value) AS stock_value,
                SUM(damaged_units) AS damaged_units
            FROM inventory
            GROUP BY
                YEAR(snapshot_date),
                MONTH(snapshot_date),
                DATE_FORMAT(snapshot_date, '%Y-%m')
            ORDER BY year, month
            """
        )

        capture(
            "DAMAGED UNITS BY PRODUCT",
            """
            SELECT
                p.product_name,
                SUM(i.damaged_units) AS damaged_units,
                SUM(i.closing_stock) AS closing_stock,
                CASE
                    WHEN SUM(i.closing_stock) = 0 THEN 0
                    ELSE SUM(i.damaged_units) / SUM(i.closing_stock) * 100
                END AS damage_rate
            FROM inventory i
            JOIN products p ON i.product_id = p.product_id
            GROUP BY p.product_id, p.product_name
            ORDER BY damaged_units DESC
            """
        )

        capture(
            "STOCK VALUE BY PRODUCT",
            """
            SELECT
                p.product_name,
                p.category,
                SUM(i.stock_value) AS stock_value,
                SUM(i.closing_stock) AS closing_stock
            FROM inventory i
            JOIN products p ON i.product_id = p.product_id
            GROUP BY p.product_id, p.product_name, p.category
            ORDER BY stock_value DESC
            """
        )

        # ============================================================
        # 8. SUPPLY CHAIN AND DELIVERIES
        # ============================================================

        capture(
            "PURCHASE VALUE OVER TIME",
            """
            SELECT
                YEAR(order_date) AS year,
                MONTH(order_date) AS month,
                DATE_FORMAT(order_date, '%Y-%m') AS period,
                SUM(total_cost) AS purchase_value
            FROM purchases
            GROUP BY
                YEAR(order_date),
                MONTH(order_date),
                DATE_FORMAT(order_date, '%Y-%m')
            ORDER BY year, month
            """
        )

        capture(
            "SUPPLIER SPENDING",
            """
            SELECT
                s.supplier_name,
                s.supplier_type,
                SUM(p.total_cost) AS supplier_spending,
                SUM(p.quantity_received) AS quantity_received
            FROM purchases p
            JOIN suppliers s ON p.supplier_id = s.supplier_id
            GROUP BY s.supplier_id, s.supplier_name, s.supplier_type
            ORDER BY supplier_spending DESC
            """
        )

        capture(
            "DELIVERY STATUS",
            """
            SELECT
                delivery_status,
                COUNT(*) AS deliveries,
                SUM(quantity_shipped) AS quantity_shipped,
                SUM(delivery_cost) AS delivery_cost
            FROM deliveries
            GROUP BY delivery_status
            ORDER BY deliveries DESC
            """
        )

        capture(
            "DELIVERY SUCCESS RATE BY YEAR",
            """
            SELECT
                YEAR(shipment_date) AS year,
                COUNT(*) AS total_deliveries,
                SUM(
                    CASE
                        WHEN LOWER(delivery_status) IN ('delivered', 'successful', 'completed')
                        THEN 1 ELSE 0
                    END
                ) AS successful_deliveries,
                CASE
                    WHEN COUNT(*) = 0 THEN 0
                    ELSE
                        SUM(
                            CASE
                                WHEN LOWER(delivery_status) IN ('delivered', 'successful', 'completed')
                                THEN 1 ELSE 0
                            END
                        ) / COUNT(*) * 100
                END AS delivery_success_rate
            FROM deliveries
            GROUP BY YEAR(shipment_date)
            ORDER BY year
            """
        )

        capture(
            "PURCHASES BY MATERIAL CATEGORY",
            """
            SELECT
                rm.material_category,
                SUM(p.total_cost) AS purchase_value,
                SUM(p.quantity_ordered) AS quantity_ordered,
                SUM(p.quantity_received) AS quantity_received
            FROM purchases p
            JOIN raw_materials rm ON p.material_id = rm.material_id
            GROUP BY rm.material_category
            ORDER BY purchase_value DESC
            """
        )

        capture(
            "DELIVERY DISTANCE OVER TIME",
            """
            SELECT
                YEAR(shipment_date) AS year,
                MONTH(shipment_date) AS month,
                DATE_FORMAT(shipment_date, '%Y-%m') AS period,
                SUM(distance_km) AS total_distance_km,
                AVG(distance_km) AS average_distance_km
            FROM deliveries
            GROUP BY
                YEAR(shipment_date),
                MONTH(shipment_date),
                DATE_FORMAT(shipment_date, '%Y-%m')
            ORDER BY year, month
            """
        )

        capture(
            "DELIVERY STATUS BY YEAR",
            """
            SELECT
                YEAR(shipment_date) AS year,
                delivery_status,
                COUNT(*) AS deliveries
            FROM deliveries
            GROUP BY YEAR(shipment_date), delivery_status
            ORDER BY year, deliveries DESC
            """
        )

        # ============================================================
        # 9. QUALITY AND EXPENSES
        # ============================================================

        capture(
            "QUALITY EVENTS BY TYPE",
            """
            SELECT
                event_type,
                COUNT(*) AS events,
                SUM(quantity) AS affected_quantity
            FROM quality_returns
            GROUP BY event_type
            ORDER BY events DESC
            """
        )

        capture(
            "QUALITY EVENTS BY PRODUCT",
            """
            SELECT
                p.product_name,
                COUNT(*) AS quality_events,
                SUM(q.quantity) AS affected_quantity
            FROM quality_returns q
            JOIN products p ON q.product_id = p.product_id
            GROUP BY p.product_id, p.product_name
            ORDER BY quality_events DESC
            """
        )

        capture(
            "EXPENSES OVER TIME",
            """
            SELECT
                YEAR(expense_date) AS year,
                MONTH(expense_date) AS month,
                DATE_FORMAT(expense_date, '%Y-%m') AS period,
                SUM(amount) AS expenses
            FROM expenses
            GROUP BY
                YEAR(expense_date),
                MONTH(expense_date),
                DATE_FORMAT(expense_date, '%Y-%m')
            ORDER BY year, month
            """
        )

        capture(
            "QUALITY EVENTS OVER TIME",
            """
            SELECT
                YEAR(event_date) AS year,
                MONTH(event_date) AS month,
                DATE_FORMAT(event_date, '%Y-%m') AS period,
                COUNT(*) AS quality_events,
                SUM(quantity) AS affected_quantity
            FROM quality_returns
            GROUP BY
                YEAR(event_date),
                MONTH(event_date),
                DATE_FORMAT(event_date, '%Y-%m')
            ORDER BY year, month
            """
        )

        capture(
            "EXPENSES BY CATEGORY",
            """
            SELECT
                expense_category,
                SUM(amount) AS expenses,
                COUNT(*) AS transactions
            FROM expenses
            GROUP BY expense_category
            ORDER BY expenses DESC
            """
        )

        capture(
            "EXPENSES BY DEPARTMENT",
            """
            SELECT
                COALESCE(department, 'Unassigned') AS department,
                SUM(amount) AS expenses,
                COUNT(*) AS transactions
            FROM expenses
            GROUP BY department
            ORDER BY expenses DESC
            """
        )

        # ============================================================
        # 10. DATA QUALITY / DOCUMENTATION
        # ============================================================

        capture(
            "PRODUCT DATA QUALITY",
            """
            SELECT
                COUNT(*) AS total_products,
                SUM(CASE WHEN product_name IS NULL OR product_name = '' THEN 1 ELSE 0 END) AS missing_product_names,
                SUM(CASE WHEN category IS NULL OR category = '' THEN 1 ELSE 0 END) AS missing_categories,
                SUM(CASE WHEN unit_price IS NULL THEN 1 ELSE 0 END) AS missing_prices,
                SUM(CASE WHEN standard_cost IS NULL THEN 1 ELSE 0 END) AS missing_standard_costs
            FROM products
            """
        )

        capture(
            "CUSTOMER DATA QUALITY",
            """
            SELECT
                COUNT(*) AS total_customers,
                SUM(CASE WHEN customer_name IS NULL OR customer_name = '' THEN 1 ELSE 0 END) AS missing_names,
                SUM(CASE WHEN customer_type IS NULL OR customer_type = '' THEN 1 ELSE 0 END) AS missing_customer_types,
                SUM(CASE WHEN city IS NULL OR city = '' THEN 1 ELSE 0 END) AS missing_cities,
                SUM(CASE WHEN region IS NULL OR region = '' THEN 1 ELSE 0 END) AS missing_regions
            FROM customers
            """
        )

        capture(
            "SALES DATA QUALITY",
            """
            SELECT
                COUNT(*) AS sales_rows,
                SUM(CASE WHEN revenue IS NULL THEN 1 ELSE 0 END) AS missing_revenue,
                SUM(CASE WHEN cost IS NULL THEN 1 ELSE 0 END) AS missing_cost,
                SUM(CASE WHEN profit IS NULL THEN 1 ELSE 0 END) AS missing_profit,
                SUM(CASE WHEN customer_id IS NULL THEN 1 ELSE 0 END) AS missing_customer_id,
                SUM(CASE WHEN product_id IS NULL THEN 1 ELSE 0 END) AS missing_product_id
            FROM sales
            """
        )

        capture(
            "REFERENTIAL INTEGRITY CHECK",
            """
            SELECT
                'sales -> customers' AS relationship,
                COUNT(*) AS orphan_records
            FROM sales s
            LEFT JOIN customers c ON s.customer_id = c.customer_id
            WHERE c.customer_id IS NULL

            UNION ALL

            SELECT
                'sales -> products',
                COUNT(*)
            FROM sales s
            LEFT JOIN products p ON s.product_id = p.product_id
            WHERE p.product_id IS NULL

            UNION ALL

            SELECT
                'production -> products',
                COUNT(*)
            FROM production pr
            LEFT JOIN products p ON pr.product_id = p.product_id
            WHERE p.product_id IS NULL

            UNION ALL

            SELECT
                'inventory -> products',
                COUNT(*)
            FROM inventory i
            LEFT JOIN products p ON i.product_id = p.product_id
            WHERE p.product_id IS NULL

            UNION ALL

            SELECT
                'purchases -> suppliers',
                COUNT(*)
            FROM purchases pu
            LEFT JOIN suppliers s ON pu.supplier_id = s.supplier_id
            WHERE s.supplier_id IS NULL

            UNION ALL

            SELECT
                'purchases -> raw_materials',
                COUNT(*)
            FROM purchases pu
            LEFT JOIN raw_materials rm ON pu.material_id = rm.material_id
            WHERE rm.material_id IS NULL

            UNION ALL

            SELECT
                'deliveries -> sales',
                COUNT(*)
            FROM deliveries d
            LEFT JOIN sales s ON d.sale_id = s.sale_id
            WHERE s.sale_id IS NULL
            """
        )

        # ============================================================
        # 11. DATASET SCALE FOR DOCUMENTATION
        # ============================================================

        capture(
            "DATASET SCALE SUMMARY",
            """
            SELECT
                (SELECT COUNT(*) FROM products) AS products,
                (SELECT COUNT(*) FROM customers) AS customers,
                (SELECT COUNT(*) FROM suppliers) AS suppliers,
                (SELECT COUNT(*) FROM raw_materials) AS raw_materials,
                (SELECT COUNT(*) FROM purchases) AS purchases,
                (SELECT COUNT(*) FROM production) AS production_records,
                (SELECT COUNT(*) FROM bill_of_materials) AS bom_records,
                (SELECT COUNT(*) FROM inventory) AS inventory_records,
                (SELECT COUNT(*) FROM sales) AS sales_records,
                (SELECT COUNT(*) FROM deliveries) AS delivery_records,
                (SELECT COUNT(*) FROM quality_returns) AS quality_records,
                (SELECT COUNT(*) FROM expenses) AS expense_records
            """
        )

        # ============================================================
        # WRITE FILE
        # ============================================================

        with open("munchies_report_data.txt", "w", encoding="utf-8") as file:
            file.write("\n".join(output))

        print("\n" + "=" * 70)
        print("MUNCHIES REPORT EXTRACTION COMPLETE")
        print("=" * 70)
        print("\nCreated:")
        print("  munchies_report_data.txt")
        print("\nSend me that file and I will use it to build:")
        print("  1. Overview")
        print("  2. Data")
        print("  3. Challenges")
        print("  4. Walkthrough")
        print("  5. Key Takeaways")
        print("  6. README.md")
        print("  7. Insights.md")

    except Error as e:
        print(f"\nMySQL Error: {e}")

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    main()