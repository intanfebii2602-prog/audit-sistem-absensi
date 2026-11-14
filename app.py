
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =====================================
# 1. KONFIGURASI HALAMAN
# =====================================

st.set_page_config(
    page_title="Audit Sistem Absensi",
    page_icon="📊",
    layout="wide"
)

# =====================================
# 2. JUDUL APLIKASI
# =====================================

st.title("📊 Dashboard Audit Sistem Informasi Absensi")
st.subheader("PT Karya Busana Muria")
st.caption("Audit Sistem Informasi menggunakan Kerangka Kerja COBIT 5")

st.info(
    "Hasil penilaian berdasarkan skenario studi kasus hipotetis."
)

# =====================================
# 3. MEMBACA DATA EXCEL
# =====================================

df = pd.read_excel(
    "Hasil_Audit_Sistem_Absensi.xlsx",
    sheet_name="Data Audit"
)

# =====================================
# 4. MENGHITUNG HASIL AUDIT
# =====================================

total_pertanyaan = len(df)
total_ya = (df["Jawaban"] == "Ya").sum()
total_tidak = (df["Jawaban"] == "Tidak").sum()
total_na = (df["Jawaban"] == "N/A").sum()

persentase = (
    total_ya / (total_pertanyaan - total_na)
) * 100

# =====================================
# 5. RINGKASAN HASIL AUDIT
# =====================================

st.header("Ringkasan Hasil Penilaian Audit")

kolom1, kolom2, kolom3, kolom4 = st.columns(4)

kolom1.metric("Total Pertanyaan", total_pertanyaan)
kolom2.metric("Jawaban Ya", total_ya)
kolom3.metric("Jawaban Tidak", total_tidak)
kolom4.metric("Kepatuhan", f"{persentase:.2f}%")

# =====================================
# 6. REKAPITULASI PER DOMAIN COBIT 5
# =====================================

st.header("Rekapitulasi Hasil Audit per Domain")

rekap = pd.crosstab(
    df["Domain"],
    df["Jawaban"]
)

for jawaban in ["Ya", "Tidak", "N/A"]:
    if jawaban not in rekap.columns:
        rekap[jawaban] = 0

rekap = rekap[["Ya", "Tidak", "N/A"]]

urutan = ["APO", "BAI", "DSS", "EDM", "MEA"]
rekap = rekap.reindex(urutan, fill_value=0)

rekap["Total Pertanyaan"] = (
    rekap["Ya"] + rekap["Tidak"] + rekap["N/A"]
)

rekap["Persentase Kepatuhan"] = (
    rekap["Ya"] /
    (rekap["Total Pertanyaan"] - rekap["N/A"])
) * 100

rekap_tampil = rekap.copy()

rekap_tampil["Persentase Kepatuhan"] = (
    rekap_tampil["Persentase Kepatuhan"]
    .map(lambda x: f"{x:.2f}%")
)

st.dataframe(
    rekap_tampil,
    use_container_width=True
)

# =====================================
# 7. GRAFIK KEPATUHAN
# =====================================

st.header("Grafik Persentase Kepatuhan")

fig, ax = plt.subplots(figsize=(10, 5))

ax.bar(
    rekap.index,
    rekap["Persentase Kepatuhan"]
)

ax.set_xlabel("Domain COBIT 5")
ax.set_ylabel("Persentase Kepatuhan (%)")
ax.set_ylim(0, 100)

ax.set_title(
    "Persentase Kepatuhan Audit per Domain"
)

for i, nilai in enumerate(
    rekap["Persentase Kepatuhan"]
):
    ax.text(
        i,
        nilai + 2,
        f"{nilai:.2f}%",
        ha="center"
    )

ax.grid(
    axis="y",
    linestyle="--",
    alpha=0.5
)

st.pyplot(fig)

# =====================================
# 8. DAFTAR TEMUAN AUDIT
# =====================================

st.header("Identifikasi Temuan Audit")

temuan = df[df["Jawaban"] == "Tidak"].copy()

st.write(f"Jumlah temuan audit: {len(temuan)}")

st.dataframe(
    temuan[
        [
            "Domain",
            "Kode Proses",
            "Pertanyaan Audit",
            "Catatan Auditor"
        ]
    ],
    use_container_width=True
)

# =====================================
# 9. RISIKO DAN REKOMENDASI
# =====================================

st.header("Risiko dan Rekomendasi Perbaikan")

df_temuan = pd.read_excel(
    "Hasil_Audit_Sistem_Absensi.xlsx",
    sheet_name="Temuan Audit"
)

st.dataframe(
    df_temuan[
        [
            "Domain",
            "Kode Proses",
            "Risiko",
            "Rekomendasi"
        ]
    ],
    use_container_width=True
)

# =====================================
# 10. KESIMPULAN
# =====================================

st.header("Kesimpulan Penilaian Audit")

st.write(
    f"Berdasarkan {total_pertanyaan} pertanyaan audit, "
    f"terdapat {total_ya} jawaban Ya dan "
    f"{total_tidak} jawaban Tidak."
)

st.write(
    f"Persentase kepatuhan berdasarkan skenario studi kasus "
    f"adalah {persentase:.2f}%."
)

if persentase >= 80:
    st.success("Kategori penilaian: Baik")
elif persentase >= 60:
    st.info("Kategori penilaian: Cukup")
else:
    st.warning("Kategori penilaian: Perlu Perbaikan")

st.caption(
    "Catatan: Data merupakan skenario studi kasus hipotetis "
    "dan bukan hasil audit lapangan."
)

