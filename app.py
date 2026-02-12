"""
Python to Browser App - Sales Dashboard
Interactive Streamlit dashboard with KPIs and charts.
KPIs and charts update based on the selected date range.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from datetime import datetime

# ---------------- Page Configuration ----------------
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============ CUSTOM CSS FOR MODERN DESIGN ============
st.markdown("""
    <style>
        /* Main backgrounds and colors */
        :root {
            --primary-color: #0066cc;
            --secondary-color: #00d4ff;
            --accent-color: #ff6b6b;
            --success-color: #00c896;
            --warning-color: #ffa500;
            --dark-bg: #0f1419;
            --light-bg: #f8f9fa;
            --card-bg: #ffffff;
            --text-primary: #1a1a1a;
            --text-secondary: #666666;
            --border-color: #e0e0e0;
        }

        /* Scrollbar styling */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
        }
        ::-webkit-scrollbar-thumb {
            background: #0066cc;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #004a94;
        }

        /* Header styling */
        .header-container {
            background: linear-gradient(135deg, #0066cc 0%, #00d4ff 100%);
            padding: 2rem 2.5rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            box-shadow: 0 8px 16px rgba(0, 102, 204, 0.15);
            color: white;
        }

        .header-title {
            font-size: 2.8rem;
            font-weight: 700;
            margin: 0;
            letter-spacing: -0.5px;
        }

        .header-subtitle {
            font-size: 1.1rem;
            opacity: 0.95;
            margin: 0.5rem 0 0 0;
            font-weight: 400;
        }

        /* Card styling */
        .metric-card {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            border: 1px solid #e0e0e0;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
            transition: all 0.3s ease;
            height: 100%;
        }

        .metric-card:hover {
            box-shadow: 0 8px 24px rgba(0, 102, 204, 0.12);
            border-color: #0066cc;
            transform: translateY(-2px);
        }

        .insight-card {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            border-left: 4px solid #0066cc;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
            transition: all 0.3s ease;
        }

        .insight-card.success {
            border-left-color: #00c896;
        }

        .insight-card.warning {
            border-left-color: #ffa500;
        }

        /* Section headers */
        .section-header {
            font-size: 1.6rem;
            font-weight: 700;
            color: #1a1a1a;
            margin: 1.5rem 0 1rem 0;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #0066cc;
            display: inline-block;
        }

        /* Divider */
        .divider {
            height: 1px;
            background: linear-gradient(to right, transparent, #e0e0e0, transparent);
            margin: 1.5rem 0;
            border: none;
        }

        /* Chart container */
        .chart-container {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
            margin-bottom: 1.5rem;
        }

        /* Filter section */
        .filter-container {
            background: linear-gradient(135deg, #f8f9fa 0%, #efefef 100%);
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid #e0e0e0;
            margin-bottom: 1.5rem;
        }

        /* Expander customization */
        .streamlit-expander {
            border-radius: 12px;
            border: 1px solid #e0e0e0;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
        }

        /* Footer */
        .footer-container {
            text-align: center;
            color: #666666;
            font-size: 0.9rem;
            margin-top: 3rem;
            padding-top: 2rem;
            border-top: 1px solid #e0e0e0;
        }

        /* Button styling */
        .stButton > button {
            background: linear-gradient(135deg, #0066cc 0%, #004a94 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.6rem 1.5rem;
            font-weight: 600;
            transition: all 0.3s ease;
        }

        .stButton > button:hover {
            box-shadow: 0 8px 16px rgba(0, 102, 204, 0.4);
            transform: translateY(-2px);
        }

        /* Selectbox and input styling */
        .stSelectbox, .stDateInput {
            border-radius: 8px;
        }

        /* Slider styling */
        .stSlider {
            padding: 0.5rem 0;
        }

        /* Heading adjustments */
        h1, h2, h3 {
            color: #1a1a1a;
        }

        h1 {
            font-weight: 700;
            letter-spacing: -0.5px;
        }

        /* Space between sections */
        [data-testid="stVerticalBlock"] > [style*="flex-direction: column"] > [data-testid="stVerticalBlock"]:has(> .section-header) {
            margin-top: 1.5rem;
        }
    </style>
""", unsafe_allow_html=True)

# ============ HEADER ============
st.markdown("""
    <div class="header-container">
        <h1 class="header-title">💼 Interactive Sales Dashboard</h1>
        <p class="header-subtitle">Real-time insights into your sales performance and market trends</p>
    </div>
""", unsafe_allow_html=True)

# ============ LOAD DATA ============
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

if df.empty:
    st.stop()

# ============ FILTER CONTROLS ============
st.markdown('<hr class="divider">', unsafe_allow_html=True)

col_filter1, col_filter2, col_filter3 = st.columns([3, 1, 1])

with col_filter1:
    st.markdown("#### 📅 Filter by Date Range")
    min_date = df['Date'].min()
    max_date = df['Date'].max()
    start_date, end_date = st.date_input(
        "Select Date Range",
        [min_date, max_date],
        min_value=min_date,
        max_value=max_date,
        label_visibility="collapsed"
    )

with col_filter2:
    st.write("")
    st.write("")
    if st.button("🔄 Reset Dates"):
        start_date, end_date = min_date, max_date
        st.rerun()

with col_filter3:
    st.write("")
    st.write("")
    if st.button("🔃 Refresh Data"):
        st.cache_data.clear()
        st.rerun()

# Filter data
df_filtered = df[(df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))]

if df_filtered.empty:
    st.warning("⚠️ No data in the selected date range.")
    st.stop()

# ============ CALCULATE METRICS ============
total_sales = df_filtered['Sales'].sum()
total_orders = len(df_filtered)
avg_order_value = df_filtered['Sales'].mean()
total_quantity = df_filtered['Quantity Sold'].sum()
top_product = df_filtered.loc[df_filtered['Sales'].idxmax(), 'Product']
top_region = df_filtered.groupby('Region')['Sales'].sum().idxmax()
best_day = df_filtered.loc[df_filtered['Sales'].idxmax(), 'Date'].strftime("%B %d, %Y")
best_day_sales = df_filtered['Sales'].max()
avg_daily_sales = df_filtered.groupby('Date')['Sales'].sum().mean()
total_products_sold = df_filtered['Product'].nunique()

# ============ KEY METRICS ============
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<h2 class="section-header">📊 Key Metrics</h2>', unsafe_allow_html=True)

metric1, metric2, metric3, metric4 = st.columns(4)

with metric1:
    st.markdown("""
        <div class="metric-card">
            <div style="font-size: 0.9rem; color: #666; margin-bottom: 0.5rem;">💰 Total Revenue</div>
            <div style="font-size: 2rem; font-weight: 700; color: #0066cc;">${:,.0f}</div>
            <div style="font-size: 0.8rem; color: #999; margin-top: 0.3rem;">All Orders</div>
        </div>
    """.format(total_sales), unsafe_allow_html=True)

with metric2:
    st.markdown("""
        <div class="metric-card">
            <div style="font-size: 0.9rem; color: #666; margin-bottom: 0.5rem;">📦 Total Orders</div>
            <div style="font-size: 2rem; font-weight: 700; color: #00d4ff;">{:,}</div>
            <div style="font-size: 0.8rem; color: #999; margin-top: 0.3rem;">Transactions</div>
        </div>
    """.format(total_orders), unsafe_allow_html=True)

with metric3:
    st.markdown("""
        <div class="metric-card">
            <div style="font-size: 0.9rem; color: #666; margin-bottom: 0.5rem;">🛒 Avg Order Value</div>
            <div style="font-size: 2rem; font-weight: 700; color: #00c896;">${:,.0f}</div>
            <div style="font-size: 0.8rem; color: #999; margin-top: 0.3rem;">Per Order</div>
        </div>
    """.format(avg_order_value), unsafe_allow_html=True)

with metric4:
    st.markdown("""
        <div class="metric-card">
            <div style="font-size: 0.9rem; color: #666; margin-bottom: 0.5rem;">📊 Total Qty Sold</div>
            <div style="font-size: 2rem; font-weight: 700; color: #ffa500;">{:,}</div>
            <div style="font-size: 0.8rem; color: #999; margin-top: 0.3rem;">Units</div>
        </div>
    """.format(total_quantity), unsafe_allow_html=True)

# ============ INSIGHTS ============
st.markdown('<h2 class="section-header" style="margin-top: 2rem;">✨ Quick Insights</h2>', unsafe_allow_html=True)

insight1, insight2, insight3 = st.columns(3)

with insight1:
    st.markdown(f"""
        <div class="insight-card">
            <div style="font-size: 0.85rem; color: #666; font-weight: 600; margin-bottom: 0.3rem;">🏆 TOP PRODUCT</div>
            <div style="font-size: 1.3rem; color: #0066cc; font-weight: 700;">{top_product}</div>
        </div>
    """, unsafe_allow_html=True)

with insight2:
    st.markdown(f"""
        <div class="insight-card success">
            <div style="font-size: 0.85rem; color: #666; font-weight: 600; margin-bottom: 0.3rem;">🌍 LEADING REGION</div>
            <div style="font-size: 1.3rem; color: #00c896; font-weight: 700;">{top_region}</div>
        </div>
    """, unsafe_allow_html=True)

with insight3:
    st.markdown(f"""
        <div class="insight-card warning">
            <div style="font-size: 0.85rem; color: #666; font-weight: 600; margin-bottom: 0.3rem;">📈 PEAK SALES</div>
            <div style="font-size: 1.2rem; color: #ffa500; font-weight: 700;">${best_day_sales:,.0f}</div>
            <div style="font-size: 0.75rem; color: #999; margin-top: 0.3rem;">{best_day}</div>
        </div>
    """, unsafe_allow_html=True)

# ============ CHARTS SECTION ============
st.markdown('<hr class="divider">', unsafe_allow_html=True)

# Create tabs for different visualizations
tab1, tab2, tab3 = st.tabs(["📊 Category Analysis", "📈 Timeline Trends", "🥧 Distribution"])

# -------- TAB 1: Bar Chart --------
with tab1:
    st.markdown('<h3 class="section-header">Sales by Category</h3>', unsafe_allow_html=True)
    col_controls1, col_controls2, col_controls3 = st.columns(3)
    
    with col_controls1:
        x_option = st.selectbox("Category Type", ["Product", "Region"], key="bar_x")
    with col_controls2:
        y_option = st.selectbox("Metric", ["Sales", "Quantity Sold"], key="bar_y")
    with col_controls3:
        top_n = st.slider("Top Items", min_value=3, max_value=20, value=10, key="top_n")
    
    bar_data = df_filtered.groupby(x_option)[y_option].sum().reset_index()
    bar_data = bar_data.sort_values(by=y_option, ascending=False).head(top_n)
    
    fig_bar = px.bar(
        bar_data,
        x=x_option,
        y=y_option,
        color=y_option,
        title=f"Top {top_n} {x_option} by {y_option}",
        template="plotly_white",
        color_continuous_scale="Blues"
    )
    fig_bar.update_layout(
        height=450,
        showlegend=False,
        font=dict(size=11),
        margin=dict(l=0, r=0, t=40, b=0)
    )
    st.plotly_chart(fig_bar, use_container_width=True, key="bar_chart")

# -------- TAB 2: Line Chart --------
with tab2:
    st.markdown('<h3 class="section-header">Sales Trends Over Time</h3>', unsafe_allow_html=True)
    
    line_data = df_filtered.groupby('Date')['Sales'].sum().reset_index()
    
    fig_line = px.line(
        line_data,
        x='Date',
        y='Sales',
        title=f"Daily Sales Trend ({start_date.strftime('%b %d')} to {end_date.strftime('%b %d')})",
        template="plotly_white"
    )
    fig_line.update_traces(line=dict(color='#0066cc', width=3))
    fig_line.update_layout(
        height=450,
        hovermode='x unified',
        font=dict(size=11),
        margin=dict(l=0, r=0, t=40, b=0)
    )
    st.plotly_chart(fig_line, use_container_width=True, key="line_chart")

# -------- TAB 3: Pie Chart --------
with tab3:
    st.markdown('<h3 class="section-header">Sales Distribution</h3>', unsafe_allow_html=True)
    
    pie_option = st.selectbox("Breakdown by", ["Product", "Region"], key="pie_option")
    pie_data = df_filtered.groupby(pie_option)['Sales'].sum().reset_index()
    
    fig_pie = px.pie(
        pie_data,
        names=pie_option,
        values='Sales',
        title=f"Sales Distribution by {pie_option}",
        template="plotly_white"
    )
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    fig_pie.update_layout(
        height=450,
        font=dict(size=11),
        margin=dict(l=0, r=0, t=40, b=0)
    )
    st.plotly_chart(fig_pie, use_container_width=True, key="pie_chart")

# ============ FOOTER ============
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown("""
    <div class="footer-container">
        <p>📊 <strong>Sales Dashboard</strong> | Built with Streamlit | Data last updated: """ + datetime.now().strftime("%B %d, %Y at %I:%M %p") + """</p>
        <p style="margin-top: 0.5rem; font-size: 0.85rem;">💡 Tip: Update data.xlsx to refresh all charts and metrics instantly</p>
    </div>
""", unsafe_allow_html=True)
