import streamlit as st
import pandas as pd
from supabase import create_client
from dotenv import load_dotenv
import os
import plotly.express as px

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="Supabase KPI Dashboard", layout="wide")
st.title("📊 Customer & Order Analytics (Supabase Views)")


def load_view(view_name):
    """Load a view from Supabase using the REST API"""
    response = supabase.table(view_name).select("*").execute()
    return pd.DataFrame(response.data)


# ---------------------------
# Load all KPI views
# ---------------------------
df_repeat = load_view("vw_repeat_customers")
df_month = load_view("vw_monthly_order_trends")
df_region = load_view("vw_regional_revenue")
df_top = load_view("vw_top_spenders_last_30")


# ---------------------------
# KPI CARDS
# ---------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Repeat Customers", len(df_repeat))
col2.metric("Months", len(df_month))
col3.metric("Regions", df_region['region'].nunique())
col4.metric("Top Spenders (30 Days)", len(df_top))

st.divider()


# ---------------------------
# Monthly Trends
# ---------------------------
st.subheader("📆 Monthly Order Trends")

left, right = st.columns([1,1])

with left:
    st.dataframe(df_month, use_container_width=True)

with right:
    fig_month = px.line(
        df_month, x="month", y="total_orders",
        title="Monthly Orders"
    )
    st.plotly_chart(fig_month, use_container_width=True)

st.divider()

# ---------------------------
# Regional Revenue
# ---------------------------
st.subheader("🌍 Regional Revenue")

left, right = st.columns([1,1])

with left:
    st.dataframe(df_region, use_container_width=True)

with right:
    fig_region = px.bar(
        df_region, x="region", y="revenue",
        title="Revenue by Region"
    )
    st.plotly_chart(fig_region, use_container_width=True)
st.divider()
# ---------------------------
# Repeat Customers
# ---------------------------
st.subheader("🔁 Repeat Customers Analysis")

left, right = st.columns([1, 1])   # 50% / 50% width

with left:
    st.markdown("### 📄 Customer Table")
    st.dataframe(df_repeat, height=500, use_container_width=True)

with right:
    st.markdown("### 📈 Orders Count Chart")
    fig = px.bar(
        df_repeat,
        x="customer_name",
        y="orders_count",
        title="Repeat Customer Orders",
        labels={"customer_name": "Customer", "orders_count": "Orders"},
    )
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# ---------------------------
# Top Spenders
# ---------------------------
st.subheader("💰 Top Customers (Last 30 Days)")
st.dataframe(df_top, use_container_width=True)
