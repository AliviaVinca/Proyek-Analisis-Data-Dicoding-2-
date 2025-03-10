import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Judul Dashboard
st.title("Analisis Penggunaan Sepeda (Bike Sharing)")
st.write("Dashboard ini menampilkan analisis penggunaan sepeda berdasarkan tren musiman, kondisi cuaca, dan pola penggunaan pada hari weekend.")

day_df = pd.read_csv('main_data.csv') 
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
day_df['month'] = day_df['dteday'].dt.month

# Sidebar Filter Waktu
st.sidebar.header("Filter Waktu")
start_date, end_date = st.sidebar.date_input("Pilih Rentang Tanggal:", 
                                             [day_df['dteday'].min(), day_df['dteday'].max()])
filtered_df = day_df[(day_df['dteday'] >= pd.to_datetime(start_date)) & 
                      (day_df['dteday'] <= pd.to_datetime(end_date))]


# Fungsi untuk visualisasi tren jumlah pengguna sepeda per hari
def plot_daily_trend(df):
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df, x="dteday", y="cnt", color="blue")
    plt.title("Tren Pengguna Sepeda Harian", fontsize=14)
    plt.xlabel("Tanggal", fontsize=12)
    plt.ylabel("Jumlah Pengguna Sepeda", fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True)
    st.pyplot(plt)

season_counts = day_df.groupby("season")["cnt"].mean().sort_values(ascending=False)
# Fungsi untuk visualisasi jumlah pengguna berdasarkan musim
def plot_seasonal_distribution(season_counts):
    season_labels = ["Winter", "Spring", "Summer", "Fall"]
    
    plt.figure(figsize=(8, 5))
    sns.barplot(x=season_labels, y=season_counts.values, palette="coolwarm")
    plt.title("Rata-rata Pengguna Sepeda per Musim", fontsize=14)
    plt.xlabel("Musim", fontsize=12)
    plt.ylabel("Rata-rata Jumlah Pengguna", fontsize=12)
    plt.grid(axis="y")
    st.pyplot(plt)


# Tampilkan Visualisasi Tren Pengguna Sepeda Harian
st.subheader("Tren Pengguna Sepeda Harian Berdasarkan Rentang Waktu")
plot_daily_trend(filtered_df)

# Insight dari tren pengguna sepeda
st.markdown("**Insight:** Penggunaan sepeda sangat dipengaruhi oleh musim dan cuaca. Pada musim panas dan gugur, jumlah pengguna sepeda lebih tinggi dibandingkan musim dingin.")

# Tampilkan Visualisasi Pengguna Sepeda Berdasarkan Musim
st.subheader("Distribusi Pengguna Sepeda Berdasarkan Musim")
plot_seasonal_distribution(season_counts)

# Insight dari distribusi musim
st.markdown("**Insight:** Rata-rata pengguna sepeda tertinggi terjadi di musim dingin, sedangkan musim gugur memiliki jumlah pengguna yang lebih rendah.")
st.markdown("""
Dari pertanyaan pertama yaitu : Bagaimana pola rata-rata pengguna sepeda per hari dalam setahun terakhir? (Tren musiman)

Dapat disimpulkan bahwa penggunaan sepeda sangat dipengaruhi oleh musim, dengan puncak penggunaan pada bulan-bulan dengan cuaca hangat.
""")

# Fungsi untuk menampilkan distribusi jumlah pengguna berdasarkan kondisi cuaca
# Definisikan season dalam bentuk dictionary
season_mapping = {
    1: "Musim Salju",
    2: "Musim Semi",
    3: "Musim Panas",
    4: "Musim Gugur"
}

day_df["season_label"] = day_df["season"].map(season_mapping)

# Sidebar Filter Musim
st.sidebar.header("Filter Musim")
season_options = ["Semua Musim"] + list(season_mapping.values())
selected_season = st.sidebar.selectbox("Pilih Musim:", options=season_options)

# Filter Data Berdasarkan Musim
df_season_filtered = day_df.copy()
if selected_season != "Semua Musim":
    selected_season_num = {v: k for k, v in season_mapping.items()}[selected_season]
    df_season_filtered = day_df[day_df['season'] == selected_season_num]

# Sidebar Filter Kondisi Cuaca
weather_labels = {
    1: "Cerah/Sedikit Berawan",
    2: "Berawan/Mendung",
    3: "Hujan/Salju Ringan"
}

day_df["weather_label"] = day_df["weathersit"].map(weather_labels)
weather_options = ["Semua Kondisi Cuaca"] + list(weather_labels.values())
selected_weather = st.sidebar.selectbox("Pilih Kondisi Cuaca:", options=weather_options)

# Filter Data Berdasarkan Kondisi Cuaca
df_weather_filtered = df_season_filtered.copy()
if selected_weather != "Semua Kondisi Cuaca":
    selected_weather_num = {v: k for k, v in weather_labels.items()}[selected_weather]
    df_weather_filtered = df_season_filtered[df_season_filtered['weathersit'] == selected_weather_num]

# Fungsi untuk menampilkan distribusi jumlah pengguna berdasarkan kondisi cuaca
def plot_weather_distribution(df):
    weather_distribution = df.groupby('weathersit')['cnt'].mean().sort_values(ascending=False)
    
    # Ubah indeks menjadi label yang lebih mudah dibaca
    weather_distribution.index = weather_distribution.index.map(weather_labels)
    
    # Visualisasi
    plt.figure(figsize=(8, 5))
    sns.barplot(x=weather_distribution.index, y=weather_distribution.values, palette="coolwarm")
    plt.title("Distribusi Jumlah Pengguna Sepeda Berdasarkan Kondisi Cuaca", fontsize=12)
    plt.xlabel("Kondisi Cuaca", fontsize=10)
    plt.ylabel("Rata-rata Jumlah Pengguna", fontsize=10)
    plt.xticks(rotation=15)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    st.pyplot(plt)

# Tampilkan Visualisasi
st.subheader("Distribusi Jumlah Pengguna Sepeda Berdasarkan Kondisi Cuaca")
plot_weather_distribution(df_weather_filtered)

# Insight tambahan
st.markdown("""
Dari pertanyaan kedua yaitu : Bagaimana distribusi rata-rata pengguna sepeda berdasarkan kondisi cuaca yang berbeda?

Dapat disimpulkan bahwa kondisi cuaca cerah mendorong penggunaan sepeda yang lebih tinggi, sementara cuaca buruk menjadi penghalang.
""")

# Fungsi untuk visualisasi penggunaan sepeda pada weekday dan weekend

def plot_weekday_weekend_usage(filtered_df):
    latest_date = filtered_df['dteday'].max()
    six_months_ago = latest_date - pd.DateOffset(months=6)
    df_last_six_months = filtered_df[filtered_df['dteday'] >= six_months_ago]
    df_last_six_months['is_weekend'] = df_last_six_months['weekday'].apply(lambda x: 1 if x in [5, 6] else 0)
    weekend_usage = df_last_six_months[df_last_six_months['is_weekend'] == 1]['cnt']
    weekday_usage = df_last_six_months[df_last_six_months['is_weekend'] == 0]['cnt']
    
    # Visualisasi 1: Perbandingan penggunaan weekend vs weekday
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=['Weekend', 'Weekday'], y=[weekend_usage.mean(), weekday_usage.mean()], ax=ax, palette="coolwarm")
    ax.set_title('Perbandingan Rata-rata Penggunaan Sepeda: Weekend vs Weekday')
    ax.set_ylabel('Rata-rata Pengguna Sepeda')
    st.pyplot(fig)
    
    # Visualisasi 2: Tren penggunaan sepeda pada weekend
    fig, ax = plt.subplots(figsize=(10, 6))
    df_weekend = df_last_six_months[df_last_six_months['is_weekend'] == 1]
    sns.lineplot(x=df_weekend['dteday'], y=df_weekend['cnt'], ax=ax)
    ax.set_title('Tren Penggunaan Sepeda pada Weekend (Enam Bulan Terakhir)')
    ax.set_xlabel('Tanggal')
    ax.set_ylabel('Jumlah Pengguna Sepeda')
    st.pyplot(fig)

# Tampilkan Visualisasi
st.subheader("Visualisasi Penggunaan Sepeda pada Weekday dan Weekend")
plot_weekday_weekend_usage(filtered_df)
st.markdown("""
Dari pertanyaan ketiga yaitu : Bagaimana pola penggunaan sepeda pada akhir pekan dalam enam bulan terakhir?

Dapat disimpulkan bahwa penggunaan sepeda pada hari weekend lebih tinggi dibandingkan hari weekday, terutama pada bulan-bulan dengan cuaca yang baik.
""")

st.markdown("© 2025 Alivia Vinca Kustaryono. All Rights Reserved.")


