import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta

def calculate_price(square_meters, price_per_meter):
    return square_meters * price_per_meter

def calculate_banner_dimensions(width, height):
    """Banner o'lchamlarini hisoblash"""
    area = float(width) * float(height)  # Maydonni float sifatida hisoblash
    dimensions = f"{width}x{height}"  # O'lchamlarni saqlash
    return area, dimensions

def calculate_banner_price(banner_area, price_per_meter):
    """Banner narxini hisoblash"""
    return float(banner_area) * float(price_per_meter)  # Narxni float sifatida hisoblash

def format_currency(amount):
    """Pulni formatlash"""
    if amount is None:
        return "0.00 so'm"
    return f"{float(amount):,.2f} so'm"

def create_daily_revenue_chart(payments_df):
    daily_revenue = payments_df.groupby('payment_date')['amount'].sum().reset_index()
    fig = px.line(daily_revenue, x='payment_date', y='amount',
                  title='Kunlik tushum',
                  labels={'payment_date': 'Sana', 'amount': 'Tushum'})
    return fig

def calculate_debt(orders_df, payments_df):
    total_orders = orders_df['total_price'].sum()
    total_payments = payments_df['amount'].sum()
    return total_orders - total_payments

def get_date_range():
    today = datetime.now().date()
    start_date = today - timedelta(days=30)
    return start_date, today