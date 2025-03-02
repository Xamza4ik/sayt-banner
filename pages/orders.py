import streamlit as st
from database import add_order, get_customers, get_orders
from utils import calculate_price, format_currency, calculate_banner_dimensions, calculate_banner_price

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

        # Banner o'lchamlari
        banner_width = st.number_input("Banner eni (metr)", min_value=0.0)
        banner_height = st.number_input("Banner bo'yi (metr)", min_value=0.0)
        banner_price_per_meter = st.number_input("Banner 1 kv.m narxi", min_value=0.0)

    with col2:
        delivery_price = st.number_input("Yetkazib berish narxi", min_value=0.0)
        delivery_status = st.selectbox("Yetkazib berish holati",
                                     ["Kutilmoqda", "Yetkazilmoqda", "Yetkazildi"])
        installation_status = st.selectbox("O'rnatish holati",
                                         ["Kutilmoqda", "Jarayonda", "O'rnatildi"])

    # Calculate banner dimensions and price
    banner_area, banner_dimensions = calculate_banner_dimensions(banner_width, banner_height)
    banner_price = calculate_banner_price(banner_area, banner_price_per_meter)

    # Calculate total price
    material_price = calculate_price(square_meters, price_per_meter)
    total_price = float(material_price) + float(banner_price) + float(delivery_price)

    # Show price breakdown
    st.write("Narxlar tafsiloti:")
    st.write(f"Material narxi: {format_currency(material_price)}")
    st.write(f"Banner o'lchami: {banner_dimensions} metr")
    st.write(f"Banner maydoni: {banner_area:.2f} kv.metr")
    st.write(f"Banner narxi: {format_currency(banner_price)}")
    st.write(f"Yetkazib berish: {format_currency(delivery_price)}")
    st.write(f"Jami narx: {format_currency(total_price)}")

    if st.form_submit_button("Buyurtma qo'shish"):
        if customer and square_meters > 0 and price_per_meter > 0:
            customer_id = customers_df[customers_df['name'] == customer]['id'].iloc[0]
            add_order(
                customer_id=customer_id,
                square_meters=square_meters,
                price_per_meter=price_per_meter,
                banner_dimensions=banner_dimensions,
                delivery_status=delivery_status,
                installation_status=installation_status,
                banner_price=banner_price,
                delivery_price=delivery_price
            )
            st.success("Buyurtma muvaffaqiyatli qo'shildi!")
        else:
            st.error("Barcha maydonlarni to'ldiring!")

# Display orders
st.header("Buyurtmalar ro'yxati")
orders_df = get_orders()
if not orders_df.empty:
    # Format the display columns
    display_df = orders_df.copy()
    display_df['total_price'] = display_df['total_price'].apply(format_currency)
    display_df['price_per_meter'] = display_df['price_per_meter'].apply(format_currency)
    display_df = display_df[[
        'customer_name', 'square_meters', 'price_per_meter', 
        'banner_dimensions', 'total_price', 'delivery_status', 
        'installation_status', 'order_date'
    ]]

    # Rename columns for better display
    display_df.columns = [
        'Mijoz', 'Kvadrat metr', 'Metr narxi', 
        'Banner o\'lchamlari', 'Jami narx', 
        'Yetkazish holati', 'O\'rnatish holati', 'Sana'
    ]

    st.dataframe(display_df)
else:
    st.info("Hozircha buyurtmalar mavjud emas")