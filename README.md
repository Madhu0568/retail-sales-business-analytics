<<<<<<< HEAD
# Retail Sales & Business Performance Analytics

A beginner-friendly portfolio project using Python, Pandas, SQLite, SQL and visualisation.

## Dataset
Download the UCI Online Retail dataset:
https://archive.ics.uci.edu/dataset/352/online+retail

Save the Excel file as `Online Retail.xlsx` inside the `data` folder.

Dataset citation: Chen, D. (2015). Online Retail [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5BW33. Licensed CC BY 4.0.

## Run in VS Code
1. Open this folder in VS Code.
2. In the terminal run: `pip install -r requirements.txt`
3. Download and place `Online Retail.xlsx` in `data/`.
4. Run: `python src/analyze_retail.py`

## What the project does
- Inspects missing values and data quality.
- Excludes cancelled invoices and rows with invalid/non-positive quantity or price from the main sales analysis.
- Calculates revenue as Quantity × UnitPrice.
- Analyses monthly sales, countries, products and customers.
- Saves cleaned data and summary tables to CSV and SQLite.
- Generates charts in `outputs/charts/`.

## Important interpretation
This dataset contains sales transaction prices but no product cost information. Therefore, this project calculates **revenue**, not profit. Customer-level analysis excludes transactions with missing CustomerID. The data is historical (December 2010–December 2011).

## SQL
Open `sql/analysis_queries.sql` for example business queries. The Python script creates `outputs/retail_analysis.db` with tables that these queries use.

## Resume wording — only after completing and understanding the project
**Retail Sales & Business Performance Analytics | Python, Pandas, SQL, SQLite, Matplotlib**
- Analysed historical online retail transactions to identify monthly revenue trends, top products, country-level performance and customer purchasing patterns.
- Cleaned transaction data using documented rules for cancellations, invalid quantities/prices and missing customer identifiers.
- Stored analysis-ready data in SQLite and generated business summaries and visualisations using Python and SQL.
=======
# retail-sales-business-analytics
Retail sales analysis using Python, SQL and data visualization
>>>>>>> 3e10008cc0d54ae2c1eda2305eb611db84bb5a52
