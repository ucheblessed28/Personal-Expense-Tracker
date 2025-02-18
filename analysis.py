import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to the database
conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

# Query the database
query = "SELECT date, category, amount FROM expenses GROUP BY category"
df = pd.read_sql(query, conn)

# Check if the DataFrame is empty
if df.empty:
    print("⚠️ No data found in the 'expenses' table.")
else:
    # Convert date column to datetime format
    df["date"] = pd.to_datetime(df["date"])

    # Group by category and calculate total amount spent
    category_summary = df.groupby("category")["amount"].sum()

    # Print summary
    print("\n📊 Expense Summary: ")
    print(category_summary)

    # Plot the data
    plt.figure(figsize=(10, 6))
    category_summary.plot(kind="bar", color="skyblue")
    plt.title("Total Expenses by Category")
    plt.xlabel("Category")
    plt.ylabel("Total Amount Spent")
    plt.xticks(rotation=45)
    plt.show()

def export_to_csv():
    df.to_csv("expenses_report.csv", index=False)
    print("\n✅ Expenses exported to 'expenses_report.csv' successfully!")

export_to_csv()

conn.close()