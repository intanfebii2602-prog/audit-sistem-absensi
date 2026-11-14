import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# KONFIGURASI HALAMAN
st.set_page_config(
    page_title="Audit Sistem Absensi",
    page_icon="📊",
    layout="wide"
)

# JUDUL APLIKASI
st.title("📊 Dashboard Audit Sistem Informasi Absensi")
st.subheader("PT Karya Busana Muria")
st.caption("Audit Sistem Informasi menggunakan Kerangka Kerja COBIT 5")

st.info(
    "Dashboard ini menyajikan hasil penilaian berdasarkan "
    "skenario studi kasus hipotetis."
)

st.write("Selamat datang di aplikasi audit sistem informasi absensi.")
