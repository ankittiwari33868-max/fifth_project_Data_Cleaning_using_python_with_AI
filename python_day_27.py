import pandas as pd

# Load data
df = pd.read_csv("50000_data.CSV")

# -----------------------------
# 1. CLEAN TEXT COLUMNS
# -----------------------------
cols_to_clean = ["Customer Name", "Product Category", "Region", "State", "City"]

for col in cols_to_clean:
    df[col] = (
        df[col]
        .astype(str)
        .str.strip()          # remove extra spaces
        .str.title()          # proper formatting
    )

# -----------------------------
# 2. REMOVE DUPLICATES
# -----------------------------
df = df.drop_duplicates(subset=["Customer ID"], keep="first")

# -----------------------------
# 3. ORDER VALUE CATEGORY
# -----------------------------
def categorize(amount):
    if amount >= 10000:
        return "High"
    elif amount >= 5000:
        return "Medium"
    else:
        return "Low"

df["Order_Value_Category"] = df["Amount"].apply(categorize)

# -----------------------------
# 4. SUMMARY REPORTS
# -----------------------------

# Total sales by City
city_summary = (
    df.groupby("City")["Amount"]
    .sum()
    .reset_index()
    .sort_values(by="Amount", ascending=False)
)

# Total sales by Product Category
category_summary = (
    df.groupby("Product Category")["Amount"]
    .sum()
    .reset_index()
    .sort_values(by="Amount", ascending=False)
)

# -----------------------------
# 5. EXPORT FILES
# -----------------------------
df.to_csv("cleaned_sales_data.csv", index=False)
city_summary.to_csv("sales_by_city.csv", index=False)
category_summary.to_csv("sales_by_category.csv", index=False)

# -----------------------------
# DONE
# -----------------------------
print("Pipeline executed successfully ✅")
