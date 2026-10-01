CREATE DATABASE IF NOT EXISTS munchies;

USE munchies;


-- =========================================================
-- 1. PRODUCTS
-- =========================================================

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
);


-- =========================================================
-- 2. CUSTOMERS / B2B BUYERS
-- =========================================================

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
);


-- =========================================================
-- 3. SUPPLIERS
-- =========================================================

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
);


-- =========================================================
-- 4. RAW MATERIALS
-- =========================================================

CREATE TABLE IF NOT EXISTS raw_materials (
    material_id VARCHAR(20) PRIMARY KEY,
    material_name VARCHAR(150) NOT NULL,
    material_category VARCHAR(80) NOT NULL,
    unit_of_measure VARCHAR(30) NOT NULL,
    standard_cost DECIMAL(15,4) NOT NULL,
    reorder_level DECIMAL(15,2) DEFAULT 0,
    material_status VARCHAR(30) DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- =========================================================
-- 5. PURCHASES
-- =========================================================

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
);


-- =========================================================
-- 6. PRODUCTION
-- =========================================================

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
);


-- =========================================================
-- 7. BILL OF MATERIALS
-- =========================================================

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
);


-- =========================================================
-- 8. INVENTORY
-- =========================================================

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
);


-- =========================================================
-- 9. SALES
-- =========================================================

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
);


-- =========================================================
-- 10. DELIVERIES
-- =========================================================

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
);


-- =========================================================
-- 11. QUALITY & RETURNS
-- =========================================================

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
);


-- =========================================================
-- 12. EXPENSES
-- =========================================================

CREATE TABLE IF NOT EXISTS expenses (
    expense_id VARCHAR(30) PRIMARY KEY,
    expense_date DATE NOT NULL,

    expense_category VARCHAR(100) NOT NULL,
    department VARCHAR(100),

    amount DECIMAL(15,2) NOT NULL,
    description VARCHAR(255),

    payment_status VARCHAR(30) DEFAULT 'Paid'
);


-- =========================================================
-- INDEXES
-- =========================================================

-- Purchases

CREATE INDEX IF NOT EXISTS idx_purchases_order_date
ON purchases(order_date);

CREATE INDEX IF NOT EXISTS idx_purchases_supplier
ON purchases(supplier_id);

CREATE INDEX IF NOT EXISTS idx_purchases_material
ON purchases(material_id);


-- Production

CREATE INDEX IF NOT EXISTS idx_production_date
ON production(production_date);

CREATE INDEX IF NOT EXISTS idx_production_product
ON production(product_id);


-- Bill of Materials

CREATE INDEX IF NOT EXISTS idx_bom_product
ON bill_of_materials(product_id);

CREATE INDEX IF NOT EXISTS idx_bom_material
ON bill_of_materials(material_id);


-- Inventory

CREATE INDEX IF NOT EXISTS idx_inventory_date
ON inventory(snapshot_date);

CREATE INDEX IF NOT EXISTS idx_inventory_product
ON inventory(product_id);


-- Sales

CREATE INDEX IF NOT EXISTS idx_sales_date
ON sales(sale_date);

CREATE INDEX IF NOT EXISTS idx_sales_customer
ON sales(customer_id);

CREATE INDEX IF NOT EXISTS idx_sales_product
ON sales(product_id);


-- Deliveries

CREATE INDEX IF NOT EXISTS idx_deliveries_shipment_date
ON deliveries(shipment_date);

CREATE INDEX IF NOT EXISTS idx_deliveries_sale
ON deliveries(sale_id);

CREATE INDEX IF NOT EXISTS idx_deliveries_customer
ON deliveries(customer_id);

CREATE INDEX IF NOT EXISTS idx_deliveries_product
ON deliveries(product_id);


-- Quality & Returns

CREATE INDEX IF NOT EXISTS idx_quality_returns_date
ON quality_returns(event_date);

CREATE INDEX IF NOT EXISTS idx_quality_returns_product
ON quality_returns(product_id);

CREATE INDEX IF NOT EXISTS idx_quality_returns_customer
ON quality_returns(customer_id);


-- Expenses

CREATE INDEX IF NOT EXISTS idx_expenses_date
ON expenses(expense_date);