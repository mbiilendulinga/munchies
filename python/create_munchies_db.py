import mysql.connector
from mysql.connector import Error


DB_NAME = "munchies"

# Change these to your MySQL credentials
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "password"


def create_database():
    connection = None
    cursor = None

    try:
        # Connect to MySQL server without selecting a database
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD
        )

        cursor = connection.cursor()

        # ---------------------------------------------------------
        # CREATE DATABASE
        # ---------------------------------------------------------
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`"
        )

        print(f"Database '{DB_NAME}' created successfully.")

        # Select database
        cursor.execute(f"USE `{DB_NAME}`")

        # ---------------------------------------------------------
        # 1. PRODUCTS
        # ---------------------------------------------------------
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                product_id VARCHAR(20) PRIMARY KEY,
                product_name VARCHAR(150) NOT NULL,
                category VARCHAR(50) NOT NULL,
                subcategory VARCHAR(80),
                brand VARCHAR(100) DEFAULT 'Munchies',
                pack_size_g DECIMAL(10,2),
                unit_of_measure VARCHAR(30) DEFAULT 'Pack',
                unit_price DECIMAL(15,2) NOT NULL,
                standard_cost DECIMAL(15,2) NOT NULL,
                launch_date DATE,
                product_status VARCHAR(30) DEFAULT 'Active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # ---------------------------------------------------------
        # 2. CUSTOMERS / B2B BUYERS
        # ---------------------------------------------------------
        # These represent organizations Munchies sells to,
        # not individual end consumers.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                customer_id VARCHAR(20) PRIMARY KEY,
                customer_name VARCHAR(150) NOT NULL,
                customer_type VARCHAR(50) NOT NULL,
                city VARCHAR(100),
                region VARCHAR(100),
                country VARCHAR(100) DEFAULT 'Zambia',
                credit_limit DECIMAL(15,2) DEFAULT 0,
                payment_terms_days INT DEFAULT 30,
                customer_since DATE,
                status VARCHAR(30) DEFAULT 'Active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # ---------------------------------------------------------
        # 3. SUPPLIERS
        # ---------------------------------------------------------
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS suppliers (
                supplier_id VARCHAR(20) PRIMARY KEY,
                supplier_name VARCHAR(150) NOT NULL,
                supplier_type VARCHAR(80),
                city VARCHAR(100),
                region VARCHAR(100),
                country VARCHAR(100) DEFAULT 'Zambia',
                payment_terms_days INT DEFAULT 30,
                supplier_since DATE,
                status VARCHAR(30) DEFAULT 'Active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # ---------------------------------------------------------
        # 4. RAW MATERIALS
        # ---------------------------------------------------------
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS raw_materials (
                material_id VARCHAR(20) PRIMARY KEY,
                material_name VARCHAR(150) NOT NULL,
                material_category VARCHAR(80) NOT NULL,
                unit_of_measure VARCHAR(30) NOT NULL,
                standard_cost DECIMAL(15,4) NOT NULL,
                reorder_level DECIMAL(15,2) DEFAULT 0,
                material_status VARCHAR(30) DEFAULT 'Active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # ---------------------------------------------------------
        # 5. PURCHASES
        # ---------------------------------------------------------
        # Consolidated procurement table containing purchase order,
        # receipt information and cost.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS purchases (
                purchase_id VARCHAR(30) PRIMARY KEY,
                supplier_id VARCHAR(20) NOT NULL,
                material_id VARCHAR(20) NOT NULL,

                order_date DATE NOT NULL,
                expected_date DATE,
                actual_receipt_date DATE,

                quantity_ordered DECIMAL(15,2) NOT NULL,
                quantity_received DECIMAL(15,2) DEFAULT 0,

                unit_cost DECIMAL(15,4) NOT NULL,
                total_cost DECIMAL(15,2) NOT NULL,

                status VARCHAR(30) DEFAULT 'Pending',

                FOREIGN KEY (supplier_id)
                    REFERENCES suppliers(supplier_id),

                FOREIGN KEY (material_id)
                    REFERENCES raw_materials(material_id)
            )
        """)

        # ---------------------------------------------------------
        # 6. PRODUCTION
        # ---------------------------------------------------------
        # Factory and production-line details are kept as attributes
        # here rather than creating extra dimension tables.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS production (
                production_id VARCHAR(30) PRIMARY KEY,
                production_date DATE NOT NULL,
                product_id VARCHAR(20) NOT NULL,

                factory_name VARCHAR(150),
                factory_city VARCHAR(100),
                production_line VARCHAR(100),

                planned_quantity DECIMAL(15,2) NOT NULL,
                produced_quantity DECIMAL(15,2) NOT NULL,
                rejected_quantity DECIMAL(15,2) DEFAULT 0,

                production_cost DECIMAL(15,2) DEFAULT 0,
                downtime_hours DECIMAL(10,2) DEFAULT 0,

                production_status VARCHAR(30) DEFAULT 'Completed',

                FOREIGN KEY (product_id)
                    REFERENCES products(product_id)
            )
        """)

        # ---------------------------------------------------------
        # 7. BILL OF MATERIALS
        # ---------------------------------------------------------
        # Bridge table between finished products and raw materials.
        # A product can require many materials and a material can be
        # used in many products.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bill_of_materials (
                bom_id VARCHAR(30) PRIMARY KEY,
                product_id VARCHAR(20) NOT NULL,
                material_id VARCHAR(20) NOT NULL,

                quantity_required DECIMAL(15,4) NOT NULL,
                unit_of_measure VARCHAR(30) NOT NULL,

                effective_date DATE,
                status VARCHAR(30) DEFAULT 'Active',

                FOREIGN KEY (product_id)
                    REFERENCES products(product_id),

                FOREIGN KEY (material_id)
                    REFERENCES raw_materials(material_id),

                UNIQUE KEY uq_product_material (product_id, material_id)
            )
        """)

        # ---------------------------------------------------------
        # 8. INVENTORY
        # ---------------------------------------------------------
        # Periodic inventory snapshot by product and warehouse.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                inventory_id VARCHAR(30) PRIMARY KEY,
                snapshot_date DATE NOT NULL,
                product_id VARCHAR(20) NOT NULL,

                warehouse_name VARCHAR(150) NOT NULL,
                warehouse_type VARCHAR(50),
                warehouse_city VARCHAR(100),

                opening_stock DECIMAL(15,2) DEFAULT 0,
                production_received DECIMAL(15,2) DEFAULT 0,
                units_sold DECIMAL(15,2) DEFAULT 0,
                damaged_units DECIMAL(15,2) DEFAULT 0,
                closing_stock DECIMAL(15,2) DEFAULT 0,

                stock_value DECIMAL(15,2) DEFAULT 0,

                FOREIGN KEY (product_id)
                    REFERENCES products(product_id)
            )
        """)

        # ---------------------------------------------------------
        # 9. SALES
        # ---------------------------------------------------------
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                sale_id VARCHAR(30) PRIMARY KEY,
                sale_date DATE NOT NULL,

                customer_id VARCHAR(20) NOT NULL,
                product_id VARCHAR(20) NOT NULL,

                quantity DECIMAL(15,2) NOT NULL,
                unit_price DECIMAL(15,2) NOT NULL,
                discount DECIMAL(15,2) DEFAULT 0,

                revenue DECIMAL(15,2) NOT NULL,
                cost DECIMAL(15,2) NOT NULL,
                profit DECIMAL(15,2) NOT NULL,

                sales_channel VARCHAR(50),
                sales_rep VARCHAR(100),

                invoice_status VARCHAR(30) DEFAULT 'Paid',

                FOREIGN KEY (customer_id)
                    REFERENCES customers(customer_id),

                FOREIGN KEY (product_id)
                    REFERENCES products(product_id)
            )
        """)

        # ---------------------------------------------------------
        # 10. DELIVERIES
        # ---------------------------------------------------------
        # Shipment date and delivery date are kept separately because
        # they represent different operational events.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS deliveries (
                delivery_id VARCHAR(30) PRIMARY KEY,

                sale_id VARCHAR(30) NOT NULL,
                customer_id VARCHAR(20) NOT NULL,
                product_id VARCHAR(20) NOT NULL,

                shipment_date DATE NOT NULL,
                delivery_date DATE,

                quantity_shipped DECIMAL(15,2) NOT NULL,

                delivery_status VARCHAR(30),

                delivery_cost DECIMAL(15,2) DEFAULT 0,
                distance_km DECIMAL(10,2) DEFAULT 0,

                FOREIGN KEY (sale_id)
                    REFERENCES sales(sale_id),

                FOREIGN KEY (customer_id)
                    REFERENCES customers(customer_id),

                FOREIGN KEY (product_id)
                    REFERENCES products(product_id)
            )
        """)

        # ---------------------------------------------------------
        # 11. QUALITY & RETURNS
        # ---------------------------------------------------------
        # Combined table for production defects and customer returns.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS quality_returns (
                quality_return_id VARCHAR(30) PRIMARY KEY,
                event_date DATE NOT NULL,

                product_id VARCHAR(20) NOT NULL,
                customer_id VARCHAR(20),

                event_type VARCHAR(40) NOT NULL,
                quantity DECIMAL(15,2) NOT NULL,

                reason VARCHAR(150),
                factory_name VARCHAR(150),

                status VARCHAR(30) DEFAULT 'Open',

                FOREIGN KEY (product_id)
                    REFERENCES products(product_id),

                FOREIGN KEY (customer_id)
                    REFERENCES customers(customer_id)
            )
        """)

        # ---------------------------------------------------------
        # 12. EXPENSES
        # ---------------------------------------------------------
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                expense_id VARCHAR(30) PRIMARY KEY,
                expense_date DATE NOT NULL,

                expense_category VARCHAR(100) NOT NULL,
                department VARCHAR(100),

                amount DECIMAL(15,2) NOT NULL,
                description VARCHAR(255),

                payment_status VARCHAR(30) DEFAULT 'Paid'
            )
        """)

        # ---------------------------------------------------------
        # INDEXES
        # ---------------------------------------------------------
        indexes = [
            # Purchases
            """
            CREATE INDEX idx_purchases_order_date
            ON purchases(order_date)
            """,
            """
            CREATE INDEX idx_purchases_supplier
            ON purchases(supplier_id)
            """,
            """
            CREATE INDEX idx_purchases_material
            ON purchases(material_id)
            """,

            # Production
            """
            CREATE INDEX idx_production_date
            ON production(production_date)
            """,
            """
            CREATE INDEX idx_production_product
            ON production(product_id)
            """,

            # Bill of Materials
            """
            CREATE INDEX idx_bom_product
            ON bill_of_materials(product_id)
            """,
            """
            CREATE INDEX idx_bom_material
            ON bill_of_materials(material_id)
            """,

            # Inventory
            """
            CREATE INDEX idx_inventory_date
            ON inventory(snapshot_date)
            """,
            """
            CREATE INDEX idx_inventory_product
            ON inventory(product_id)
            """,

            # Sales
            """
            CREATE INDEX idx_sales_date
            ON sales(sale_date)
            """,
            """
            CREATE INDEX idx_sales_customer
            ON sales(customer_id)
            """,
            """
            CREATE INDEX idx_sales_product
            ON sales(product_id)
            """,

            # Deliveries
            """
            CREATE INDEX idx_deliveries_shipment_date
            ON deliveries(shipment_date)
            """,
            """
            CREATE INDEX idx_deliveries_sale
            ON deliveries(sale_id)
            """,
            """
            CREATE INDEX idx_deliveries_customer
            ON deliveries(customer_id)
            """,
            """
            CREATE INDEX idx_deliveries_product
            ON deliveries(product_id)
            """,

            # Quality & Returns
            """
            CREATE INDEX idx_quality_returns_date
            ON quality_returns(event_date)
            """,
            """
            CREATE INDEX idx_quality_returns_product
            ON quality_returns(product_id)
            """,
            """
            CREATE INDEX idx_quality_returns_customer
            ON quality_returns(customer_id)
            """,

            # Expenses
            """
            CREATE INDEX idx_expenses_date
            ON expenses(expense_date)
            """
        ]

        for index_sql in indexes:
            try:
                cursor.execute(index_sql)

            except mysql.connector.Error as e:
                # Ignore "index already exists" errors
                if e.errno != 1061:
                    raise

        connection.commit()

        # ---------------------------------------------------------
        # SUCCESS MESSAGE
        # ---------------------------------------------------------
        print("\n" + "=" * 60)
        print("MUNCHIES DATABASE CREATED SUCCESSFULLY")
        print("=" * 60)

        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        print(f"\nTables created: {len(tables)}\n")

        for table in tables:
            print(f"  ✓ {table[0]}")

        # ---------------------------------------------------------
        # KEY RELATIONSHIPS
        # ---------------------------------------------------------
        print("\nKey relationships:")

        print("  products ────────────► sales")
        print("  products ────────────► production")
        print("  products ────────────► inventory")
        print("  products ────────────► bill_of_materials")
        print("  products ────────────► deliveries")
        print("  products ────────────► quality_returns")

        print("  customers ───────────► sales")
        print("  customers ───────────► deliveries")
        print("  customers ───────────► quality_returns")

        print("  suppliers ───────────► purchases")

        print("  raw_materials ───────► purchases")
        print("  raw_materials ───────► bill_of_materials")

        print("  sales ───────────────► deliveries")

        print("\nDate fields:")
        print("  products.launch_date")
        print("  customers.customer_since")
        print("  suppliers.supplier_since")
        print("  purchases.order_date")
        print("  purchases.expected_date")
        print("  purchases.actual_receipt_date")
        print("  production.production_date")
        print("  bill_of_materials.effective_date")
        print("  inventory.snapshot_date")
        print("  sales.sale_date")
        print("  deliveries.shipment_date")
        print("  deliveries.delivery_date")
        print("  quality_returns.event_date")
        print("  expenses.expense_date")

        print("\nDatabase is ready for data generation.")

    except Error as e:
        print(f"\nMySQL Error: {e}")

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    create_database()