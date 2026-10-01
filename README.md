 Munchies | Business Operational Analysis

POWER BI : https://www.mbiile.com/projects/munchies/

A Power BI and MySQL business intelligence project analysing the performance of a fictional cereal and snack manufacturer.

The project brings together sales, customers, products, production, inventory, procurement, deliveries, quality and expenses into a single analytical model.

> Note: Munchies is a fictional business and the dataset is synthetic. The project was created for portfolio and demonstration purposes.

 Project Overview

The analysis covers January 2023 to December 2025, using three complete years of data. The underlying database contains some partial 2026 records, which are excluded from the main year-on-year analysis.

The objective was to answer questions such as:

 How has revenue changed over time?
 Which channels, products and customer groups generate the most revenue?
 How does reported profitability vary across products and categories?
 Is production keeping pace with planned output?
 How are inventory levels changing?
 How is delivery performance changing as sales volume increases?
 Which quality issues occur most frequently?
 Where is business expenditure concentrated?

 Dataset

The MySQL database contains 12 related tables:

| Table             | Records |
| ----------------- | ------: |
| Products          |      17 |
| Customers         |     127 |
| Suppliers         |      42 |
| Raw Materials     |      61 |
| Purchases         |   4,137 |
| Production        |  11,173 |
| Bill of Materials |      89 |
| Inventory         |  22,718 |
| Sales             |  78,143 |
| Deliveries        |  31,684 |
| Quality Returns   |   1,847 |
| Expenses          |   3,126 |

Total records: 181,836

 Power BI Report

The Power BI report contains eight pages:

1. Executive Summary — Overall business performance and headline KPIs
2. Sales & Profitability — Revenue, channels, categories and reported profitability
3. Product Performance — SKU-level revenue, units, cost and margins
4. Customer Analytics — Customer types, individual accounts and geography
5. Production Performance — Planned vs actual production, factories and downtime
6. Inventory Management — Stock levels, warehouses and products
7. Supply Chain & Deliveries — Purchases, suppliers, delivery status and distance
8. Quality & Expenses — Quality events and expenditure

 Selected Findings

Revenue increased from approximately ZMW 363.0M in 2023 to ZMW 799.6M in 2025.

Revenue growth was:

 2024: 40.2%
 2025: 57.2%

Direct Sales was the largest sales channel, generating approximately ZMW 836.8M.

Cereal products generated approximately ZMW 1.34B, representing the majority of recorded revenue.

Production achievement remained close to 95% of plan in each year from 2023 to 2025.

Annual delivery success remained close to 90% throughout the complete reporting period.

Lusaka and Copperbelt were the two largest regions by revenue, generating approximately 62.5% combined.

 Data Model

The model links transactional data to common product, customer, supplier and raw-material information.

Key relationships include:

 Sales → Products
 Sales → Customers
 Production → Products
 Inventory → Products
 Purchases → Suppliers
 Purchases → Raw Materials
 Deliveries → Sales

Referential integrity checks on these relationships returned zero orphan records.

 Tools

 MySQL — Database and relational data storage
 Python — Data generation, validation and supporting analysis
 Power BI — Data modelling, DAX and interactive reporting
 Git / GitHub — Version control and project documentation

 Data Quality

Basic completeness and referential integrity checks were performed on the dataset.

The product, customer and sales tables contained no missing key fields in the validation checks performed.

One modelling consideration is the inventory table, which contains repeated stock observations. Cumulative sums of snapshot values should therefore not be interpreted as a point-in-time inventory balance.

The dataset also contains partial 2026 records. The main analysis is restricted to the complete 2023–2025 period.

The reported profit field should also be reconciled with the revenue and cost fields before being used as a formal accounting measure.

 Project Structure

```text
munchies/
│
├── data/
├── python/
├── sql/
├── powerbi/
├── README.md
└── insights.md
```

 Portfolio Context

This project was built to demonstrate practical skills in:

 Relational database design
 SQL
 Data validation
 Data modelling
 DAX
 Power BI
 Business analysis
 Data storytelling
 Git and GitHub

 Author

Mbiile Ndulinga

Business Administration with Economics | Data & Business Analytics

GitHub: `mbiilendulinga`
