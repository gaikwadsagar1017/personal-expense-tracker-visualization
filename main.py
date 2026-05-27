import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import random
import os

# ----------------------------------------
# CREATE FOLDERS
# ----------------------------------------

os.makedirs("data", exist_ok=True)
os.makedirs("outputs", exist_ok=True)
os.makedirs("reports", exist_ok=True)

# ----------------------------------------
# CREATE SYNTHETIC DATASET
# ----------------------------------------

categories = [
    "Food",
    "Travel",
    "Shopping",
    "Bills",
    "Entertainment",
    "Health"
]

payment_methods = [
    "Cash",
    "UPI",
    "Credit Card",
    "Debit Card"
]

data = []

for i in range(200):
    data.append({
        "Date": pd.Timestamp('2025-01-01') + pd.Timedelta(days=random.randint(0, 120)),
        "Category": random.choice(categories),
        "Amount": random.randint(100, 5000),
        "Payment_Method": random.choice(payment_methods),
        "Description": f"Expense {i+1}"
    })

df = pd.DataFrame(data)

# ----------------------------------------
# SAVE DATASET
# ----------------------------------------

dataset_path = "data/expense_data.csv"

df.to_csv(dataset_path, index=False)

print("Dataset Created Successfully")
print(f"Dataset Saved At: {dataset_path}")

# ----------------------------------------
# LOAD DATA
# ----------------------------------------

df = pd.read_csv(dataset_path)

# ----------------------------------------
# DATA CLEANING
# ----------------------------------------

df.drop_duplicates(inplace=True)

df['Date'] = pd.to_datetime(df['Date'])

df['Month'] = df['Date'].dt.month_name()

# ----------------------------------------
# CATEGORY-WISE ANALYSIS
# ----------------------------------------

category_analysis = df.groupby('Category')['Amount'].sum()

print("\nCategory-wise Spending:\n")
print(category_analysis)

# ----------------------------------------
# MONTHLY ANALYSIS
# ----------------------------------------

monthly_analysis = df.groupby('Month')['Amount'].sum()

print("\nMonthly Spending:\n")
print(monthly_analysis)

# ----------------------------------------
# PAYMENT METHOD ANALYSIS
# ----------------------------------------

payment_analysis = df.groupby('Payment_Method')['Amount'].sum()

print("\nPayment Method Analysis:\n")
print(payment_analysis)

# ----------------------------------------
# HIGHEST SPENDING CATEGORY
# ----------------------------------------

highest_category = category_analysis.idxmax()

print(f"\nHighest Spending Category: {highest_category}")

# ----------------------------------------
# AVERAGE DAILY SPENDING
# ----------------------------------------

average_daily_spending = df['Amount'].mean()

print(f"\nAverage Daily Spending: ₹{average_daily_spending:.2f}")

# ----------------------------------------
# TOTAL SPENDING
# ----------------------------------------

total_spending = df['Amount'].sum()

print(f"\nTotal Spending: ₹{total_spending}")

# ----------------------------------------
# VISUALIZATION
# ----------------------------------------

sns.set_style("whitegrid")

# ----------------------------------------
# CATEGORY-WISE BAR CHART
# ----------------------------------------

plt.figure(figsize=(10, 5))

category_analysis.plot(kind='bar')

plt.title("Category-wise Spending")
plt.xlabel("Category")
plt.ylabel("Amount")

plt.tight_layout()

category_chart_path = "outputs/category_bar_chart.png"

plt.savefig(category_chart_path)

plt.show()

print(f"\nCategory Chart Saved At: {category_chart_path}")

# ----------------------------------------
# MONTHLY SPENDING LINE CHART
# ----------------------------------------

plt.figure(figsize=(10, 5))

monthly_analysis.plot(kind='line', marker='o')

plt.title("Monthly Spending Trend")
plt.xlabel("Month")
plt.ylabel("Amount")

plt.tight_layout()

monthly_chart_path = "outputs/monthly_line_chart.png"

plt.savefig(monthly_chart_path)

plt.show()

print(f"Monthly Trend Chart Saved At: {monthly_chart_path}")

# ----------------------------------------
# PAYMENT METHOD PIE CHART
# ----------------------------------------

plt.figure(figsize=(8, 8))

payment_analysis.plot(kind='pie', autopct='%1.1f%%')

plt.title("Payment Method Distribution")
plt.ylabel("")

plt.tight_layout()

payment_chart_path = "outputs/payment_pie_chart.png"

plt.savefig(payment_chart_path)

plt.show()

print(f"Payment Method Chart Saved At: {payment_chart_path}")

# ----------------------------------------
# DAILY SPENDING TREND CHART
# ----------------------------------------

daily_spending = df.groupby('Date')['Amount'].sum()

plt.figure(figsize=(12, 5))

daily_spending.plot()

plt.title("Daily Spending Trend")
plt.xlabel("Date")
plt.ylabel("Amount")

plt.tight_layout()

daily_chart_path = "outputs/daily_spending_chart.png"

plt.savefig(daily_chart_path)

plt.show()

print(f"Daily Spending Chart Saved At: {daily_chart_path}")

# ----------------------------------------
# REPORT GENERATION
# ----------------------------------------

report = {
    "Total Spending": [total_spending],
    "Average Daily Spending": [average_daily_spending],
    "Highest Spending Category": [highest_category]
}

report_df = pd.DataFrame(report)

report_path = "reports/expense_summary_report.csv"

report_df.to_csv(report_path, index=False)

print("\nReport Generated Successfully")
print(f"Report Saved At: {report_path}")