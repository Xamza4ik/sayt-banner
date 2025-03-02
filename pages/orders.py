import streamlit as st
from database import add_order, get_customers, get_orders
from utils import format_currency, calculate_banner_dimensions, calculate_banner_price

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
        # Banner o'lchamlari
        st.subheader("Banner o'lchamlari")
        banner_width = st.number_input("Banner eni (metr)", min_value=0.0, step=0.1)
        banner_height = st.number_input("Banner bo'yi (metr)", min_value=0.0, step=0.1)
        banner_price_per_meter = st.number_input("Banner 1 kv.m narxi (so'm)", min_value=0.0, step=1000.0)

    with col2:
        st.subheader("Qo'shimcha xizmatlar")
        delivery_price = st.number_input("Yetkazib berish narxi (so'm)", min_value=0.0, step=1000.0)
        delivery_status = st.selectbox("Yetkazib berish holati",
                                     ["Kutilmoqda", "Yetkazilmoqda", "Yetkazildi"])
        installation_status = st.selectbox("O'rnatish holati",
                                         ["Kutilmoqda", "Jarayonda", "O'rnatildi"])

    # Calculate banner dimensions and price
    banner_area, banner_dimensions = calculate_banner_dimensions(banner_width, banner_height)
    banner_price = calculate_banner_price(banner_area, banner_price_per_meter)
    total_price = banner_price + delivery_price

    # Show price breakdown
    st.subheader("Narxlar tafsiloti:")
    col3, col4 = st.columns(2)

    with col3:
        st.write("Banner tafsilotlari:")
        st.write(f"📏 O'lchami: {banner_dimensions} metr")
        st.write(f"📐 Maydoni: {banner_area:.2f} kv.metr")
        st.write(f"💰 1 kv.m narxi: {format_currency(banner_price_per_meter)}")

    with col4:
        st.write("Narxlar:")
        st.write(f"🎨 Banner narxi: {format_currency(banner_price)}")
        st.write(f"🚚 Yetkazib berish: {format_currency(delivery_price)}")
        st.write(f"💵 Jami: {format_currency(total_price)}")

    if st.form_submit_button("Buyurtma qo'shish"):
        if customer and banner_width > 0 and banner_height > 0 and banner_price_per_meter > 0:
            try:
                customer_id = int(customers_df[customers_df['name'] == customer]['id'].iloc[0])
                add_order(
                    customer_id=customer_id,
                    square_meters=banner_area,
                    price_per_meter=banner_price_per_meter,
                    banner_dimensions=banner_dimensions,
                    delivery_status=delivery_status,
                    installation_status=installation_status,
                    banner_price=banner_price,
                    delivery_price=delivery_price
                )
                st.success("Buyurtma muvaffaqiyatli qo'shildi!")
            except Exception as e:
                st.error(f"Xatolik yuz berdi: {str(e)}")
        else:
            st.error("Barcha maydonlarni to'ldiring!")

# Display orders
st.header("Buyurtmalar ro'yxati")
orders_df = get_orders()
if not orders_df.empty:
    # Format the display columns
    display_df = orders_df.copy()

    # Format currency columns
    currency_columns = ['banner_price', 'delivery_price', 'total_price']
    for col in currency_columns:
        if col in display_df.columns:
            display_df[col] = display_df[col].apply(format_currency)

    # Select and rename columns for display
    display_df = display_df[[
        'customer_name', 'banner_dimensions', 'banner_price',
        'delivery_price', 'total_price', 'delivery_status',
        'installation_status', 'order_date'
    ]]

    display_df.columns = [
        'Mijoz', 'Banner o\'lchamlari', 'Banner narxi',
        'Yetkazish narxi', 'Jami narx', 'Yetkazish holati',
        'O\'rnatish holati', 'Sana'
    ]

    st.dataframe(display_df)
else:
    st.info("Hozircha buyurtmalar mavjud emas")