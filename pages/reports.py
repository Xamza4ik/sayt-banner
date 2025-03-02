import streamlit as st
import plotly.express as px
from database import get_orders, get_payments
from utils import create_daily_revenue_chart, calculate_debt, get_date_range
from datetime import datetime

st.title("Hisobotlar")

# Date range selector
start_date, end_date = get_date_range()
date_range = st.date_input(
    "Vaqt oralig'ini tanlang",
    value=(start_date, end_date),
    max_value=datetime.now().date()
)

if len(date_range) == 2:
    start_date, end_date = date_range
    
    # Get data
    orders_df = get_orders()
    payments_df = get_payments()
    
    # Filter by date range
    orders_df = orders_df[
        (orders_df['order_date'] >= start_date.strftime('%Y-%m-%d')) &
        (orders_df['order_date'] <= end_date.strftime('%Y-%m-%d'))
    ]
    payments_df = payments_df[
        (payments_df['payment_date'] >= start_date.strftime('%Y-%m-%d')) &
        (payments_df['payment_date'] <= end_date.strftime('%Y-%m-%d'))
    ]
    
    # Daily revenue
    st.header("Kunlik tushum")
    revenue_chart = create_daily_revenue_chart(payments_df)
    st.plotly_chart(revenue_chart)
    
    # Summary statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Jami buyurtmalar", len(orders_df))
        st.metric("Jami summa", f"{orders_df['total_price'].sum():,.2f}")
    
    with col2:
        st.metric("Jami to'lovlar", len(payments_df))
        st.metric("To'langan summa", f"{payments_df['amount'].sum():,.2f}")
    
    with col3:
        total_debt = calculate_debt(orders_df, payments_df)
        st.metric("Umumiy qarzdorlik", f"{total_debt:,.2f}")
    
    # Orders by status
    st.header("Buyurtmalar holati")
    status_df = orders_df['delivery_status'].value_counts()
    fig = px.pie(values=status_df.values, names=status_df.index,
                 title="Yetkazib berish holati")
    st.plotly_chart(fig)
