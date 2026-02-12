"""
Python to Browser App - Sales Dashboard
Interactive Streamlit dashboard with KPIs and charts.
KPIs and charts update based on the selected date range.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ---------------- Page Configuration ----------------
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="💼",
    layout="wide"
)

st.title("💼 Interactive Sales Dashboard")
st.caption("Analyze your sales data dynamically with filters and charts")
st.markdown("---")

# ---------------- Load Data ----------------
excel_file = Path("data.xlsx")

@st.cache_data
def load_data(file_path):
    try:
        df = pd.read_excel(file_path)
        df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')
        df['Quantity Sold'] = pd.to_numeric(df['Quantity Sold'], errors='coerce')
        df = df.dropna(subset=['Product', 'Sales', 'Quantity Sold', 'Date', 'Region'])
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        return df
    except FileNotFoundError:
        st.error("❌ data.xlsx not found! Place it in the same folder as app.py")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        return pd.DataFrame()

df = load_data(excel_file)

# ---------------- Reload Button ----------------
if st.button("🔄 Reload Data"):
    st.cache_data.clear()
    st.experimental_rerun()

if df.empty:
    st.stop()

# ---------------- Raw Data Table ----------------
st.markdown("---")
st.subheader("📋 Raw Sales Data")
st.dataframe(df, use_container_width=True, height=300)

# ---------------- Date Range Filter (Above KPIs) ----------------
st.markdown("---")
st.subheader("📅 Select Date Range")  # Updated title

min_date = df['Date'].min()
max_date = df['Date'].max()
start_date, end_date = st.date_input(
    "Select Date Range",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Filter data for KPIs and charts
df_filtered = df[(df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))]

if df_filtered.empty:
    st.warning("⚠️ No data in the selected date range.")
    st.stop()

# ---------------- KPIs ----------------
st.markdown("---")
st.subheader("📌 Key Performance Indicators (Filtered)")

total_sales = df_filtered['Sales'].sum()
avg_sales = df_filtered['Sales'].mean()
max_sales = df_filtered['Sales'].max()
top_product = df_filtered.loc[df_filtered['Sales'].idxmax(), 'Product']

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Total Sales", f"{total_sales:,.2f}")
kpi2.metric("Average Sale", f"{avg_sales:,.2f}")
kpi3.metric("Highest Sale", f"{max_sales:,.2f}")
kpi4.metric("Top Product", top_product)

# ---------------- Bar Chart ----------------
st.markdown("---")
st.subheader("📊 Sales by Category")

x_option = st.selectbox("X-axis (Category)", ["Product", "Region"], key="bar_x")
y_option = st.selectbox("Y-axis (Metric)", ["Sales", "Quantity Sold"], key="bar_y")
top_n = st.slider("Show Top Products", min_value=3, max_value=20, value=10, key="top_n")

bar_data = df_filtered.groupby(x_option)[y_option].sum().reset_index()
bar_data = bar_data.sort_values(by=y_option, ascending=False).head(top_n)

fig_bar = px.bar(
    bar_data,
    x=x_option,
    y=y_option,
    color=y_option,
    title=f"Top {top_n} {x_option} by {y_option}",
    template="plotly_white"
)
st.plotly_chart(fig_bar, use_container_width=True)

# ---------------- Line Chart ----------------
st.markdown("---")
st.subheader("📈 Sales Over Time (Daily)")

line_data = df_filtered.groupby('Date')['Sales'].sum().reset_index()

fig_line = px.line(
    line_data,
    x='Date',
    y='Sales',
    title=f"Daily Sales Trend ({start_date} to {end_date})",
    template="plotly_white"
)
st.plotly_chart(fig_line, use_container_width=True)

# ---------------- Pie Chart ----------------
st.markdown("---")
st.subheader("🥧 Sales Distribution")

pie_option = st.selectbox("Breakdown for Pie Chart", ["Product", "Region"], key="pie_option")
pie_data = df_filtered.groupby(pie_option)['Sales'].sum().reset_index()

fig_pie = px.pie(
    pie_data,
    names=pie_option,
    values='Sales',
    title=f"Sales Distribution by {pie_option} ({start_date} to {end_date})",
    template="plotly_white"
)
st.plotly_chart(fig_pie, use_container_width=True)

# ---------------- Footer ----------------
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "<p>Built with Streamlit 🎈 | Modify data.xlsx to update the dashboard</p>"
    "</div>",
    unsafe_allow_html=True
)
