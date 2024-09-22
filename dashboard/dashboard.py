
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

main_data = pd.read_csv("main_data.csv", sep=";")
main_data['dteday'] = pd.to_datetime(main_data['dteday'], format="%d/%m/%Y")
min_date = main_data["dteday"].min()
max_date = main_data["dteday"].max()

# Hitung total peminjaman sepeda per tahun
total_peminjaman_2011 = main_data[main_data['yr'] == 0]['cnt'].sum()
total_peminjaman_2012 = main_data[main_data['yr'] == 1]['cnt'].sum()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://i.pinimg.com/originals/ca/65/54/ca655453eb79fe8db19601dfcf53ed95.jpg")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date, value=[min_date, max_date]
    )

# Mapping untuk musim
musim_mapping = {
    1: 'Spring',
    2: 'Summer',
    3: 'Fall',
    4: 'Winter'
}

# Ubah kolom 'season' menjadi musim
main_data['season'] = main_data['season'].map(musim_mapping)

# Fungsi untuk menghitung total peminjaman sepeda per tahun
def total_peminjaman_pertahun(filtered_data):
    return total_peminjaman_2011, total_peminjaman_2012

# Visualisasi kedua barchart bersebelahan
def plot_barcharts(start_date, end_date, total_peminjaman_2011, total_peminjaman_2012):
    # Konversi start_date dan end_date menjadi string
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    # Filter data berdasarkan rentang tanggal yang dipilih
    filtered_data = main_data[(main_data['dteday'] >= start_date_str) & (main_data['dteday'] <= end_date_str)]

    # Hitung total peminjaman sepeda per tahun
    total_peminjaman_2011, total_peminjaman_2012 = total_peminjaman_pertahun(filtered_data)

    # Plot barchart untuk musim
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))

    # Barchart untuk musim
    peminjaman_per_musim = filtered_data.groupby('season')['cnt'].sum()
    peminjaman_per_musim.plot(kind='bar', ax=ax[0])
    ax[0].set_title('Jumlah Peminjaman Sepeda Berdasarkan Musim')
    ax[0].set_xlabel('Musim')
    ax[0].set_ylabel('Jumlah Peminjaman Sepeda')
    ax[0].tick_params(axis='x', rotation=45)

    # Barchart untuk hari kerja
    peminjaman_per_hari_kerja = filtered_data.groupby('workingday')['cnt'].sum()
    peminjaman_per_hari_kerja.plot(kind='bar', ax=ax[1])
    ax[1].set_title('Jumlah Peminjaman Sepeda Berdasarkan Hari Kerja')
    ax[1].set_xlabel('Hari Kerja')
    ax[1].set_ylabel('Jumlah Peminjaman Sepeda')
    ax[1].set_xticklabels(['Tidak', 'Ya'])  # Mengubah label menjadi 'Tidak' dan 'Ya'

    # Adjust layout
    plt.tight_layout()

    return fig

# Hitung total peminjaman sepeda dan total pengguna casual/register per tahun
total_peminjaman_2011 = main_data[main_data['yr'] == 0]['cnt'].sum()
total_peminjaman_2012 = main_data[main_data['yr'] == 1]['cnt'].sum()
total_casual_2011 = main_data[(main_data['yr'] == 0)]['casual'].sum()
total_casual_2012 = main_data[(main_data['yr'] == 1)]['casual'].sum()
total_registered_2011 = main_data[(main_data['yr'] == 0)]['registered'].sum()
total_registered_2012 = main_data[(main_data['yr'] == 1)]['registered'].sum()

# Menampilkan dashboard
def main():
    st.markdown("<h1 style='text-align: center; color: white;'>Dashboard Peminjaman Sepeda</h1>", unsafe_allow_html=True)
    fig = plot_barcharts(start_date, end_date, total_peminjaman_2011, total_peminjaman_2012)
    
    # Tampilkan total peminjaman sepeda per tahun
    col1, col2= st.columns(2)
    with col1:
        st.metric("**Peminjaman Sepeda Tahun 2011**", value=total_peminjaman_2011)
    with col2:
        st.metric("**Peminjaman Sepeda Tahun 2012**", value=total_peminjaman_2012)
        
    
    st.subheader('Barchart Peminjaman Sepeda Berdasarkan Musim dan Hari Kerja')
    
    # Tampilkan barchart dan total peminjaman sepeda per tahun
    st.pyplot(fig)
    col3, col4, col5, col6 = st.columns(4)
    with col3:
        st.metric("**Casual Tahun 2011**", value=total_casual_2011)
    with col4:
        st.metric("**Casual Tahun 2012**", value=total_casual_2012)
    with col5:
        st.metric("**Registered Tahun 2011**", value=total_registered_2011)
    with col6:
        st.metric("**Registered Tahun 2012**", value=total_registered_2012)


if __name__ == "__main__":
    main()
