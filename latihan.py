import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import pickle
import plotly.express as px
from PIL import Image
from babel.numbers import format_currency

px.defaults.template = 'plotly_dark'
px.defaults.color_continuous_scale = 'greens'

# Buka gambar
img = Image.open('assets/shopping.png')
st.sidebar.image(img)

# import data
with open('data.pickle','rb') as f:
    data = pickle.load(f)

with open('rfm.pickle','rb') as g:
    rfm = pickle.load(g)


## BAGIAN FILTER

# Input tanggal
date_min = data['order_date'].min()
date_max = data['order_date'].max()
start_date, end_date = st.sidebar.date_input(
    label='Rentang Waktu',
    min_value=date_min,
    max_value=date_max,
    value=[date_min, date_max]
)

# Input kategori
categories = ['All Categories'] + list(data['product_category_name_english'].value_counts().keys().sort_values())
category = st.sidebar.selectbox(label='Kategori', options=categories)

# Input negara bagian
states = ['All States'] + list(data['customer_state'].value_counts().keys().sort_values())
state = st.sidebar.selectbox(label='Negara Bagian', options=states)

# Filter tanggal
outputs = data[(data['order_date'] >= start_date) & (data['order_date'] <= end_date)]

# Filter kategori
if category != "All Categories":
    outputs = outputs[outputs['product_category_name_english'] == category]

# Filter negara bagian
if state != "All States":
    outputs = outputs[outputs['customer_state'] == state]


## visualisasi data

st.header('Dashboard Penjualan E-Commerce :shopping_bags:')

# Hitung total orders
total_orders = outputs.shape[0]

# Format total orders dengan "ribu" jika ribuan
if total_orders >= 1000:
    formatted_orders = f"{total_orders / 1000:.2f} ribu"
else:
    formatted_orders = f"{total_orders:.2f}"

# Hitung total revenue
total_revenue_value = outputs['price'].sum()

# Format total revenue dengan "juta" jika jutaan
if total_revenue_value >= 1_000_000:
    formatted_revenue = f"BRL{total_revenue_value / 1_000_000:.2f} juta"
else:
    formatted_revenue = format_currency(total_revenue_value, "BRL", locale="es_CO")

# Tampilan di Streamlit
col1, col2 = st.columns(2)

with col1:
    st.metric("Total Orders", value=formatted_orders)

with col2:
    st.metric("Total Revenue", value=formatted_revenue)

st.subheader('Capaian Penjualan')
st.write("Visualisasi capaian penjualan berdasarkan harian, status, wilayah, dan produk.")

# Mengubah 'order_date' menjadi format datetime
outputs['order_date'] = pd.to_datetime(outputs['order_date'], errors='coerce')

# Membuat kolom 'month_year' untuk agregasi per bulan
outputs['month_year'] = outputs['order_date'].dt.to_period('M').dt.to_timestamp()

# Visualiasi trend penjualan
trend = outputs[outputs['month_year'] < '2018-09-01'].groupby('month_year')['price'].sum().reset_index()
fig = px.line(trend, x='month_year', y='price',title='Trend Penjualan Perbulan', labels={'month_year': 'Bulan-Tahun', 'price': 'Total Penjualan'})
fig.update_traces(line=dict(color='green'))
st.plotly_chart(fig)

# komposisi status pesanan
status_counts = outputs['order_status'].value_counts().reset_index()
status_counts.columns = ['order_status', 'count']

fig = px.pie(
    status_counts,
    values='count',  # Jumlah
    names='order_status',  # Label
    title='Distribusi Status Pesanan',
    labels={'order_status': 'Status Pesanan'},
    hole=0.3,  # Opsional: Membuat donut chart
    width=500,
    height=500,
    color_discrete_sequence=['green', 'yellow', 'red']
)

# Menampilkan persentase pada setiap irisan
fig.update_traces(textinfo='percent+label')
# Menghilangkan legend
fig.update_layout(showlegend=False)
# Memutar lingkaran
fig.update_traces(rotation=90)  
st.plotly_chart(fig)

# kota dengan penjualan tertinggi
city_sales = outputs.groupby('customer_city')['price'].sum().nlargest(10).sort_values()
fig = px.bar(city_sales, color=city_sales, orientation='h', title='10 Kota dengan Penjualan Terbesar', labels={"customer_city": "kota asal", "value": "total penjualan"})
st.plotly_chart(fig)

# produk dengan penjualan tertinggi
prod_sales = outputs.groupby('product_category_name_english')['price'].sum().nlargest(10).sort_values()
fig = px.bar(prod_sales, color=prod_sales, orientation='h', title='10 Produk dengan Penjualan Terbesar', labels={"product_category_name_english": "kategori produk", "value": "total penjualan"})
st.plotly_chart(fig)


## Visualisasi RFM

st.subheader("Top 5 Customers Based on RFM Parameters")
st.write("Visualisasi 5 pelanggan terbaik berdasarkan Recency, Frequency, dan Monetary.")

# Fungsi untuk mendapatkan top 5 pelanggan
def get_top_5(rfm, column, ascending=True):
    return rfm.nsmallest(5, column) if ascending else rfm.nlargest(5, column).reset_index()

# Parameter RFM
parameters = {
    "Recency": {"ascending": True},
    "Frequency": {"ascending": False},
    "Monetary": {"ascending": False}
}

# Plot untuk setiap parameter
for param, config in parameters.items():
    top_5 = get_top_5(rfm, param, config["ascending"])
    fig = px.bar(
        top_5,
        x=param,          # Parameter (Recency, Frequency, atau Monetary) sebagai x-axis
        y="customer_id",  # Gunakan customer_id sebagai y-axis
        text=param,
        title=f"Top 5 Customers by {param}",
        labels={"customer_id": "Customer ID", param: param},
        color="customer_id",
        orientation='h'   # Bar chart horizontal
    )
    fig.update_traces(texttemplate='%{text}', textposition='inside')
    fig.update_layout(xaxis_title=param, yaxis_title="Customer ID", showlegend=False)
    st.plotly_chart(fig)