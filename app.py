import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Audit Sistem Absensi",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard Audit Sistem Informasi Absensi")
st.subheader("PT Karya Busana Muria")
st.caption("Audit Sistem Informasi menggunakan Kerangka Kerja COBIT 5")

st.info(
    "Hasil penilaian berdasarkan skenario studi kasus hipotetis."
)

# MEMBACA DATA EXCEL
df = pd.read_excel(
    "Hasil_Audit_Sistem_Absensi.xlsx",
    sheet_name="Data Audit"
)

# MENGHITUNG HASIL AUDIT
total_pertanyaan = len(df)
total_ya = (df["Jawaban"] == "Ya").sum()
total_tidak = (df["Jawaban"] == "Tidak").sum()
total_na = (df["Jawaban"] == "N/A").sum()

persentase = (
    total_ya / (total_pertanyaan - total_na)
) * 100

# RINGKASAN AUDIT
st.header("Ringkasan Hasil Penilaian Audit")

kolom1, kolom2, kolom3, kolom4 = st.columns(4)

kolom1.metric("Total Pertanyaan", total_pertanyaan)
kolom2.metric("Jawaban Ya", total_ya)
kolom3.metric("Jawaban Tidak", total_tidak)
kolom4.metric("Kepatuhan", f"{persentase:.2f}%")
