from pathlib import Path
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "Online Retail.xlsx"
OUTPUT_DIR = ROOT / "outputs"
CHART_DIR = OUTPUT_DIR / "charts"

OUTPUT_DIR.mkdir(exist_ok=True)
CHART_DIR.mkdir(parents=True, exist_ok=True)


def main():
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found at {DATA_FILE}. Download 'Online Retail.xlsx' "
            "from the UCI link in README.md and put it in the data folder."
        )

    print("Loading dataset...")
    raw = pd.read_excel(DATA_FILE)
    raw.columns = [str(c).strip().replace(" ", "") for c in raw.columns]

    required = {
        "InvoiceNo", "StockCode", "Description", "Quantity",
        "InvoiceDate", "UnitPrice", "CustomerID", "Country"
    }
    missing = required - set(raw.columns)
    if missing:
        raise ValueError(f"Dataset is missing expected columns: {sorted(missing)}")

    print("\n--- RAW DATA ---")
    print(f"Rows: {len(raw):,}; columns: {len(raw.columns)}")
    print(raw.isna().sum().sort_values(ascending=False))

    df = raw.copy()
    df["InvoiceNo"] = df["InvoiceNo"].astype(str)
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")
    df["Revenue"] = df["Quantity"] * df["UnitPrice"]

    # Explicit business rule: exclude cancellations and invalid sales rows.
    sales = df[
        df["InvoiceDate"].notna()
        & ~df["InvoiceNo"].str.upper().str.startswith("C")
        & (df["Quantity"] > 0)
        & (df["UnitPrice"] > 0)
    ].copy()

    sales["Month"] = sales["InvoiceDate"].dt.to_period("M").astype(str)
    sales["Weekday"] = sales["InvoiceDate"].dt.day_name()

    print("\n--- CLEANING SUMMARY ---")
    print(f"Raw rows: {len(raw):,}")
    print(f"Valid sales rows retained: {len(sales):,}")
    print(f"Rows excluded: {len(raw) - len(sales):,}")

    kpis = pd.DataFrame([{
        "transaction_lines": len(sales),
        "unique_invoices": sales["InvoiceNo"].nunique(),
        "unique_products": sales["StockCode"].nunique(),
        "unique_countries": sales["Country"].nunique(),
        "unique_customers_with_id": sales["CustomerID"].nunique(),
        "units_sold": int(sales["Quantity"].sum()),
        "total_revenue_gbp": round(sales["Revenue"].sum(), 2),
        "average_order_value_gbp": round(
            sales.groupby("InvoiceNo")["Revenue"].sum().mean(), 2
        )
    }])
    kpis.to_csv(OUTPUT_DIR / "business_kpis.csv", index=False)

    monthly = (sales.groupby("Month", as_index=False)
               .agg(revenue=("Revenue", "sum"),
                    orders=("InvoiceNo", "nunique"),
                    units_sold=("Quantity", "sum")))
    monthly.to_csv(OUTPUT_DIR / "monthly_performance.csv", index=False)

    country = (sales.groupby("Country", as_index=False)
               .agg(revenue=("Revenue", "sum"),
                    orders=("InvoiceNo", "nunique"),
                    units_sold=("Quantity", "sum"))
               .sort_values("revenue", ascending=False))
    country.to_csv(OUTPUT_DIR / "country_performance.csv", index=False)

    products = (sales.groupby(["StockCode", "Description"], dropna=False, as_index=False)
                .agg(units_sold=("Quantity", "sum"),
                     revenue=("Revenue", "sum"))
                .sort_values("revenue", ascending=False))
    products.head(20).to_csv(OUTPUT_DIR / "top_20_products.csv", index=False)

    customer_rows = sales.dropna(subset=["CustomerID"])
    customers = (customer_rows.groupby("CustomerID", as_index=False)
                 .agg(revenue=("Revenue", "sum"),
                      orders=("InvoiceNo", "nunique"),
                      units=("Quantity", "sum"))
                 .sort_values("revenue", ascending=False))
    customers.head(20).to_csv(OUTPUT_DIR / "top_20_customers.csv", index=False)

    db_path = OUTPUT_DIR / "retail_analysis.db"
    with sqlite3.connect(db_path) as conn:
        sales.to_sql("sales", conn, if_exists="replace", index=False)
        monthly.to_sql("monthly_performance", conn, if_exists="replace", index=False)
        country.to_sql("country_performance", conn, if_exists="replace", index=False)

    sns.set_theme(style="whitegrid")

    plt.figure(figsize=(11, 5))
    sns.lineplot(data=monthly, x="Month", y="revenue", marker="o")
    plt.title("Monthly Revenue Trend")
    plt.xlabel("Month")
    plt.ylabel("Revenue (£)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(CHART_DIR / "monthly_revenue.png", dpi=160)
    plt.close()

    top_countries = country.head(10).sort_values("revenue")
    plt.figure(figsize=(10, 6))
    sns.barplot(data=top_countries, x="revenue", y="Country")
    plt.title("Top 10 Countries by Revenue")
    plt.xlabel("Revenue (£)")
    plt.ylabel("Country")
    plt.tight_layout()
    plt.savefig(CHART_DIR / "top_countries.png", dpi=160)
    plt.close()

    top_products = products.head(10).copy()
    top_products["Product"] = top_products["Description"].fillna("Unknown").str.slice(0, 38)
    top_products = top_products.sort_values("revenue")
    plt.figure(figsize=(10, 6))
    sns.barplot(data=top_products, x="revenue", y="Product")
    plt.title("Top 10 Products by Revenue")
    plt.xlabel("Revenue (£)")
    plt.ylabel("Product")
    plt.tight_layout()
    plt.savefig(CHART_DIR / "top_products.png", dpi=160)
    plt.close()

    print("\n--- BUSINESS KPIs ---")
    print(kpis.to_string(index=False))
    print("\n--- TOP 5 COUNTRIES ---")
    print(country.head(5).to_string(index=False))
    print(f"\nFinished. Results saved in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
