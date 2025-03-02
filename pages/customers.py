import streamlit as st
from database import add_customer, get_customers

st.title("Mijozlar")

# Add new customer
st.header("Yangi mijoz qo'shish")
with st.form("new_customer"):
    name = st.text_input("Mijoz ismi")
    phone = st.text_input("Telefon raqami")
    workplace = st.text_input("Ish joyi")
    
    if st.form_submit_button("Qo'shish"):
        if name and phone:
            add_customer(name, phone, workplace)
            st.success("Mijoz muvaffaqiyatli qo'shildi!")
        else:
            st.error("Ism va telefon raqami kiritilishi shart!")

# Display customers
st.header("Mijozlar ro'yxati")
customers_df = get_customers()
if not customers_df.empty:
    st.dataframe(customers_df)
else:
    st.info("Hozircha mijozlar mavjud emas")
