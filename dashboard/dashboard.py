import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Judul Dashboard
st.title("Dashboard Analisis Rental Sepeda")

# Load dataset
@st.cache_data  # Cache data untuk mempercepat loading
def load_data():
    data = pd.read_csv("dashboard/main_data.csv")
    data['dteday'] = pd.to_datetime(data['dteday'])  # Pastikan kolom tanggal dalam format datetime
    return data

day_df = load_data()

# Sidebar untuk filter
st.sidebar.header("Filter Data")

# Date Picker untuk memilih rentang tanggal
date_range = st.sidebar.date_input(
    "Pilih Rentang Tanggal",
    value=(day_df['dteday'].min().date(), day_df['dteday'].max().date()),  # Default: rentang penuh
    min_value=day_df['dteday'].min().date(),
    max_value=day_df['dteday'].max().date()
)

# Filter data berdasarkan rentang tanggal
filtered_data = day_df[
    (day_df['dteday'].dt.date >= date_range[0]) &
    (day_df['dteday'].dt.date <= date_range[1])
]

# Section 1: Overview
st.header("Overview Data")
st.write(f"Menampilkan data rental sepeda untuk rentang tanggal {date_range[0]} hingga {date_range[1]}.")
st.dataframe(filtered_data.head())

# Section 2: Persentase Kontribusi Pengguna Kasual vs Terdaftar
st.header("Kontribusi Pengguna Kasual vs Terdaftar")
total_casual = filtered_data['casual'].sum()
total_registered = filtered_data['registered'].sum()
total_cnt = total_casual + total_registered

percentage_casual = (total_casual / total_cnt) * 100
percentage_registered = (total_registered / total_cnt) * 100

# Visualisasi Pie Chart
fig, ax = plt.subplots(figsize=(6, 6))
labels = ['Pengguna Kasual', 'Pengguna Terdaftar']
sizes = [percentage_casual, percentage_registered]
colors = ['#ff9999', '#66b3ff']
explode = (0.1, 0)
ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
ax.axis('equal')  # Memastikan pie chart berbentuk lingkaran sempurna
st.pyplot(fig)

# Section 3: Pengaruh Cuaca terhadap Penyewaan Sepeda
st.header("Pengaruh Cuaca terhadap Penyewaan Sepeda")
weather_summary = filtered_data.groupby('weathersit')[['casual', 'registered']].sum().reset_index()
weather_summary['weather_label'] = weather_summary['weathersit'].map({
    1: 'Cerah/Jelas',
    2: 'Berkabut/Berawan',
    3: 'Hujan Ringan/Salju',
    4: 'Cuaca Buruk'
})

# Reshape data untuk clustered bar chart
weather_melted = weather_summary.melt(
    id_vars=['weathersit', 'weather_label'], 
    value_vars=['casual', 'registered'],
    var_name='user_type', 
    value_name='total_rentals'
)

# Visualisasi Clustered Bar Chart
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=weather_melted, x='weather_label', y='total_rentals', hue='user_type', palette='Blues_d', ax=ax)
ax.set_title("Pengaruh Cuaca terhadap Jumlah Penyewaan Sepeda")
ax.set_xlabel("Kondisi Cuaca")
ax.set_ylabel("Total Penyewaan Sepeda")
st.pyplot(fig)

# Section 4: Hari Kerja vs Akhir Pekan
st.header("Perbandingan Hari Kerja vs Akhir Pekan")
workingday_summary = filtered_data.groupby('workingday')[['casual', 'registered']].sum().reset_index()
workingday_summary['workingday_label'] = workingday_summary['workingday'].map({0: 'Akhir Pekan/Hari Libur', 1: 'Hari Kerja'})

# Reshape data untuk clustered bar chart
workingday_melted = workingday_summary.melt(
    id_vars=['workingday', 'workingday_label'], 
    value_vars=['casual', 'registered'],
    var_name='user_type', 
    value_name='total_rentals'
)

# Visualisasi Clustered Bar Chart
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=workingday_melted, x='workingday_label', y='total_rentals', hue='user_type', palette='Blues_d', ax=ax)
ax.set_title("Perbandingan Penggunaan Sepeda Antara Hari Kerja dan Akhir Pekan")
ax.set_xlabel("Kategori Hari")
ax.set_ylabel("Total Penyewaan Sepeda")
st.pyplot(fig)