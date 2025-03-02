import streamlit as st
from database import add_order, get_customers, get_orders
from utils import calculate_price, format_currency

st.title("Buyurtmalar")

# Add new order
st.header("Yangi buyurtma")
customers_df = get_customers()

with st.form("new_order"):
    customer = st.selectbox("Mijozni tanlang", 
                           options=customers_df['name'].tolist(),
                           index=None)
    
    col1, col2 = st.columns(2)
    with col1:
        square_meters = st.number_input("Kvadrat metr", min_value=0.0)
        price_per_meter = st.number_input("1 kv.m narxi", min_value=0.0)
    
    with col2:
        banner_dimensions = st.text_input("Banner o'lchamlari (MxN)")
        delivery_status = st.selectbox("Yetkazib berish holati",
                                     ["Kutilmoqda", "Yetkazilmoqda", "Yetkazildi"])
        installation_status = st.selectbox("O'rnatish holati",
                                         ["Kutilmoqda", "Jarayonda", "O'rnatildi"])
    
    total_price = calculate_price(square_meters, price_per_meter)
    st.write(f"Jami narx: {format_currency(total_price)}")
    
    if st.form_submit_button("Buyurtma qo'shish"):
        if customer and square_meters > 0 and price_per_meter > 0:
            customer_id = customers_df[customers_df['name'] == customer]['id'].iloc[0]
            add_order(customer_id, square_meters, price_per_meter,
                     banner_dimensions, delivery_status, installation_status)
            st.success("Buyurtma muvaffaqiyatli qo'shildi!")
        else:
            st.error("Barcha maydonlarni to'ldiring!")

# Display orders
st.header("Buyurtmalar ro'yxati")
orders_df = get_orders()
if not orders_df.empty:
    st.dataframe(orders_df)
else:
    st.info("Hozircha buyurtmalar mavjud emas")
