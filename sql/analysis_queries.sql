-- Run against outputs/retail_analysis.db

-- 1. Overall revenue, orders and units
SELECT ROUND(SUM(Revenue), 2) AS total_revenue_gbp,
       COUNT(DISTINCT InvoiceNo) AS total_orders,
       SUM(Quantity) AS units_sold
FROM sales;

-- 2. Monthly revenue and order trend
SELECT Month, ROUND(revenue, 2) AS revenue_gbp, orders, units_sold
FROM monthly_performance
ORDER BY Month;

-- 3. Top 10 countries by revenue
SELECT Country, ROUND(revenue, 2) AS revenue_gbp, orders
FROM country_performance
ORDER BY revenue DESC
LIMIT 10;

-- 4. Average order value by country (at least 100 orders)
SELECT Country,
       ROUND(SUM(Revenue) / COUNT(DISTINCT InvoiceNo), 2) AS avg_order_value_gbp,
       COUNT(DISTINCT InvoiceNo) AS orders
FROM sales
GROUP BY Country
HAVING COUNT(DISTINCT InvoiceNo) >= 100
ORDER BY avg_order_value_gbp DESC;

-- 5. Revenue by weekday
SELECT strftime('%w', InvoiceDate) AS weekday_number,
       ROUND(SUM(Revenue), 2) AS revenue_gbp
FROM sales
GROUP BY strftime('%w', InvoiceDate)
ORDER BY revenue_gbp DESC;

-- 6. Top 10 products by revenue
SELECT StockCode, Description,
       ROUND(SUM(Revenue), 2) AS revenue_gbp,
       SUM(Quantity) AS units_sold
FROM sales
GROUP BY StockCode, Description
ORDER BY revenue_gbp DESC
LIMIT 10;

-- 7. Customer revenue (only rows with a CustomerID)
SELECT CustomerID,
       ROUND(SUM(Revenue), 2) AS customer_revenue_gbp,
       COUNT(DISTINCT InvoiceNo) AS orders
FROM sales
WHERE CustomerID IS NOT NULL
GROUP BY CustomerID
ORDER BY customer_revenue_gbp DESC
LIMIT 10;
