import streamlit as st
from database import add_payment, get_orders, get_payments
from utils import format_currency

st.title("To'lovlar")

# Add new payment
st.header("Yangi to'lov")
orders_df = get_orders()

with st.form("new_payment"):
    order = st.selectbox("Buyurtmani tanlang",
                        options=orders_df['id'].tolist(),
                        index=None)
    
    if order:
        selected_order = orders_df[orders_df['id'] == order].iloc[0]
        st.write(f"Mijoz: {selected_order['customer_name']}")
        st.write(f"Buyurtma narxi: {format_currency(selected_order['total_price'])}")
    
    amount = st.number_input("To'lov miqdori", min_value=0.0)
    
    if st.form_submit_button("To'lov qo'shish"):
        if order and amount > 0:
            add_payment(order, amount)
            st.success("To'lov muvaffaqiyatli qo'shildi!")
        else:
            st.error("Barcha maydonlarni to'ldiring!")

# Display payments
st.header("To'lovlar tarixi")
payments_df = get_payments()
if not payments_df.empty:
    st.dataframe(payments_df)
else:
    st.info("Hozircha to'lovlar mavjud emas")

# Display debts
st.header("Qarzdorlik")
if not orders_df.empty and not payments_df.empty:
    debts = orders_df.merge(
        payments_df.groupby('order_id')['amount'].sum().reset_index(),
        left_on='id',
        right_on='order_id',
        how='left'
    )
    debts['debt'] = debts['total_price'] - debts['amount'].fillna(0)
    debts = debts[debts['debt'] > 0]
    
    if not debts.empty:
        st.dataframe(debts[['customer_name', 'total_price', 'amount', 'debt']])
    else:
        st.success("Qarzdor mijozlar yo'q!")
