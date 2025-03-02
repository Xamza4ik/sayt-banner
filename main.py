import streamlit as st
from database import init_db

st.set_page_config(
    page_title="Mijozlar va buyurtmalar tizimi",
    page_icon="📊",
    layout="wide"
)

# Initialize database
init_db()

st.title("Mijozlar va buyurtmalar tizimi")

st.markdown("""
### Asosiy imkoniyatlar:
- 👥 Mijozlar ma'lumotlarini boshqarish
- 📦 Buyurtmalarni qayd etish
- 💰 To'lovlarni nazorat qilish
- 📊 Hisobotlarni ko'rish

Kerakli bo'limni chap paneldan tanlang.
""")

st.sidebar.title("Navigatsiya")
