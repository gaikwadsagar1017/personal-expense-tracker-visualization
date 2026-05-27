import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Personal Expense Tracker",
    page_icon="💸",
    layout="wide"
)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("💸 Personal Expense Tracker Dashboard")
st.markdown("Analyze and visualize personal financial expenses.")

# ---------------------------------------------------
# FILE UPLOAD
# ---------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload Expense CSV File",
    type=["csv"]
)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    # ---------------------------------------------------
    # DATA CLEANING
    # ---------------------------------------------------

    df.drop_duplicates(inplace=True)

    df['Date'] = pd.to_datetime(df['Date'])

    df['Month'] = df['Date'].dt.month_name()

    # ---------------------------------------------------
    # SIDEBAR FILTERS
    # ---------------------------------------------------

    st.sidebar.header("Filters")

    categories = st.sidebar.multiselect(
        "Select Categories",
        options=df['Category'].unique(),
        default=df['Category'].unique()
    )

    payment_methods = st.sidebar.multiselect(
        "Select Payment Methods",
        options=df['Payment_Method'].unique(),
        default=df['Payment_Method'].unique()
    )

    filtered_df = df[
        (df['Category'].isin(categories)) &
        (df['Payment_Method'].isin(payment_methods))
    ]

    # ---------------------------------------------------
    # KPI METRICS
    # ---------------------------------------------------

    total_spending = filtered_df['Amount'].sum()

    average_spending = filtered_df['Amount'].mean()

    highest_category = (
        filtered_df.groupby('Category')['Amount']
        .sum()
        .idxmax()
    )

    total_transactions = len(filtered_df)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Spending", f"₹{total_spending:,.2f}")

    col2.metric("Average Spending", f"₹{average_spending:,.2f}")

    col3.metric("Top Category", highest_category)

    col4.metric("Transactions", total_transactions)

    st.divider()

    # ---------------------------------------------------
    # CATEGORY-WISE ANALYSIS
    # ---------------------------------------------------

    st.subheader("📊 Category-wise Spending")

    category_analysis = (
        filtered_df.groupby('Category')['Amount']
        .sum()
        .sort_values(ascending=False)
    )

    fig1, ax1 = plt.subplots(figsize=(10, 5))

    sns.barplot(
        x=category_analysis.index,
        y=category_analysis.values,
        ax=ax1
    )

    ax1.set_xlabel("Category")
    ax1.set_ylabel("Amount")
    ax1.set_title("Category-wise Spending")

    st.pyplot(fig1)

    # ---------------------------------------------------
    # MONTHLY TREND
    # ---------------------------------------------------

    st.subheader("📈 Monthly Spending Trend")

    monthly_analysis = (
        filtered_df.groupby('Month')['Amount']
        .sum()
    )

    fig2, ax2 = plt.subplots(figsize=(10, 5))

    ax2.plot(
        monthly_analysis.index,
        monthly_analysis.values,
        marker='o'
    )

    ax2.set_xlabel("Month")
    ax2.set_ylabel("Amount")
    ax2.set_title("Monthly Spending Trend")

    plt.xticks(rotation=45)

    st.pyplot(fig2)

    # ---------------------------------------------------
    # PAYMENT METHOD ANALYSIS
    # ---------------------------------------------------

    st.subheader("💳 Payment Method Distribution")

    payment_analysis = (
        filtered_df.groupby('Payment_Method')['Amount']
        .sum()
    )

    fig3, ax3 = plt.subplots(figsize=(8, 8))

    ax3.pie(
        payment_analysis.values,
        labels=payment_analysis.index,
        autopct='%1.1f%%'
    )

    ax3.set_title("Payment Method Usage")

    st.pyplot(fig3)

    # ---------------------------------------------------
    # DAILY SPENDING TREND
    # ---------------------------------------------------

    st.subheader("📅 Daily Spending Trend")

    daily_spending = (
        filtered_df.groupby('Date')['Amount']
        .sum()
    )

    fig4, ax4 = plt.subplots(figsize=(12, 5))

    ax4.plot(
        daily_spending.index,
        daily_spending.values
    )

    ax4.set_xlabel("Date")
    ax4.set_ylabel("Amount")
    ax4.set_title("Daily Spending")

    st.pyplot(fig4)

    # ---------------------------------------------------
    # DATA PREVIEW
    # ---------------------------------------------------

    st.subheader("🗂 Expense Data Preview")

    st.dataframe(filtered_df)

    # ---------------------------------------------------
    # DOWNLOAD REPORT
    # ---------------------------------------------------

    csv = filtered_df.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="📥 Download Filtered Report",
        data=csv,
        file_name='filtered_expense_report.csv',
        mime='text/csv'
    )

else:
    st.info("Please upload an expense CSV file.")