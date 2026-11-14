
import streamlit as st
import pandas as pd
import requests
import altair as alt

# =====================================
# KONFIGURASI
# =====================================

URL_APPS_SCRIPT = "https://script.google.com/macros/s/AKfycbwspcBN9nBRCITZCeI9maCjPfhRjR3L1zRYmoxg_d3OeVcAlXDt-LmIyfQ9keLN0NBhrQ/exec"

st.set_page_config(
    page_title="Form Audit Sistem Absensi",
    page_icon="📋",
    layout="wide"
)

# =====================================
# DATA PERTANYAAN AUDIT
# =====================================

pertanyaan = [
    ("EDM", "EDM01", "Apakah manajemen menetapkan kebijakan tata kelola yang mencakup penggunaan sistem absensi, serta mengevaluasinya secara berkala?"),
    ("EDM", "EDM01", "Apakah peran dan kewenangan persetujuan atas koreksi data kehadiran, perubahan jadwal shift, dan persetujuan lembur, cuti, dan izin telah ditetapkan secara tertulis?"),
    ("EDM", "EDM02", "Apakah manajemen mengevaluasi manfaat sistem terhadap tujuan perusahaan, misalnya akurasi data kehadiran, berkurangnya kecurangan absensi, dan efisiensi rekap oleh HRD?"),
    ("EDM", "EDM03", "Apakah manajemen menetapkan batas risiko yang dapat diterima terkait kesalahan data kehadiran, manipulasi absensi, dan kebocoran data pribadi dan biometrik karyawan?"),
    ("EDM", "EDM04", "Apakah tersedia sumber daya yang memadai (staf HRD dan TI, perangkat absensi, anggaran lisensi dan pemeliharaan) untuk mengelola sistem?"),
    ("EDM", "EDM05", "Apakah laporan kehadiran, keterlambatan, lembur, dan ketidakhadiran disampaikan secara berkala kepada direksi, dan apakah aturan penilaian kehadiran dapat dijelaskan secara transparan kepada karyawan?"),

    ("APO", "APO01", "Apakah perusahaan memiliki SOP tertulis untuk absensi, lembur, cuti, izin, dan koreksi kehadiran, termasuk ketentuan batas waktu penutupan periode (cut-off)?"),
    ("APO", "APO01", "Apakah SOP tersebut telah disosialisasikan kepada HRD, supervisor lini, dan karyawan yang berkepentingan?"),
    ("APO", "APO06", "Apakah kebutuhan pengelolaan sistem (lisensi, pemeliharaan, perangkat absensi) dimuat dalam rencana kerja dan anggaran, serta realisasinya dipantau?"),
    ("APO", "APO07", "Apakah staf HRD dan administrator sistem absensi memperoleh pelatihan yang sesuai, dan apakah tersedia pengganti ketika petugas berhalangan?"),
    ("APO", "APO12", "Apakah risiko seperti titip absen, data karyawan tidak aktif yang masih tercatat, dan kesalahan rekap lembur telah diidentifikasi dan didokumentasikan?"),
    ("APO", "APO13", "Apakah terdapat kebijakan tertulis mengenai keamanan informasi dan pelindungan data pribadi karyawan, termasuk data biometrik?"),

    ("BAI", "BAI02", "Apakah kebutuhan pengguna (HRD, Produksi, Payroll) dan ketentuan jam kerja (jadwal shift, toleransi keterlambatan, lembur, cuti) diidentifikasi dan didokumentasikan sebagai aturan sistem?"),
    ("BAI", "BAI03", "Apakah aturan shift, toleransi keterlambatan, dan perhitungan jam kerja pada sistem divalidasi, misalnya dengan mencocokkan hasil rekap sistem dengan catatan manual pada sampel karyawan, sebelum digunakan?"),
    ("BAI", "BAI06", "Apakah setiap perubahan konfigurasi (aturan jam kerja, jadwal shift, hak akses perangkat) diajukan, disetujui secara tertulis oleh pihak berwenang, dan tercatat dalam log perubahan?"),
    ("BAI", "BAI07", "Apakah perubahan atau versi baru sistem diuji dan diterima oleh pengguna sebelum dipakai pada periode kehadiran berjalan, serta hasil pengujiannya didokumentasikan?"),
    ("BAI", "BAI08", "Apakah tersedia panduan atau dokumentasi kerja sistem yang dapat diakses oleh petugas yang membutuhkan?"),
    ("BAI", "BAI09", "Apakah perusahaan memiliki daftar aset pendukung (mesin absensi, server, lisensi aplikasi) beserta penanggung jawab dan memperbaruinya secara berkala?"),

    ("DSS", "DSS01", "Apakah kegiatan rutin absensi (pencatatan harian, rekap kehadiran, koreksi, penutupan periode) dilaksanakan sesuai prosedur dan jadwal yang ditetapkan?"),
    ("DSS", "DSS02", "Apakah gangguan (mesin absensi rusak, kegagalan sinkronisasi data) dan keluhan karyawan atas catatan kehadirannya dicatat dan diselesaikan melalui prosedur yang jelas?"),
    ("DSS", "DSS03", "Apakah penyebab gangguan atau kesalahan yang berulang dianalisis dan ditindaklanjuti agar tidak terulang?"),
    ("DSS", "DSS04", "Apakah data absensi dicadangkan secara berkala, dan apakah prosedur pemulihan data pernah diuji?"),
    ("DSS", "DSS05", "Apakah akses ke sistem dibatasi berdasarkan peran, memakai akun individual dan kata sandi yang terkelola, serta akun karyawan yang keluar atau pindah tugas segera dinonaktifkan?"),
    ("DSS", "DSS06", "Apakah terdapat pemisahan tugas antara pihak yang mengelola data induk karyawan, melakukan koreksi kehadiran, dan menyetujui koreksi, serta rekonsiliasi data absensi dengan data karyawan aktif?"),

    ("MEA", "MEA01", "Apakah perusahaan menetapkan indikator kinerja proses, misalnya tingkat kehadiran, jumlah koreksi manual, ketepatan rekap, dan waktu penyelesaian koreksi, serta memantaunya secara berkala?"),
    ("MEA", "MEA01", "Apakah capaian tingkat kehadiran dan jam lembur dibandingkan dengan target atau batas kebijakan, dan penyimpangannya dianalisis serta dilaporkan kepada manajemen?"),
    ("MEA", "MEA02", "Apakah dilakukan pemeriksaan berkala atas kesesuaian data mesin absensi, data induk karyawan, dan data lembur dan cuti, termasuk verifikasi keberadaan fisik karyawan pada sampel?"),
    ("MEA", "MEA02", "Apakah terdapat audit internal atau fungsi sejenis yang menilai pengendalian pada proses absensi?"),
    ("MEA", "MEA02", "Apakah kelemahan pengendalian yang ditemukan dari pemeriksaan internal maupun eksternal ditindaklanjuti dan statusnya dipantau?"),
    ("MEA", "MEA03", "Apakah perusahaan memantau kepatuhan terhadap ketentuan eksternal, misalnya ketentuan ketenagakerjaan (jam kerja, lembur, cuti) serta pelindungan data pribadi?")
]

# =====================================
# HEADER APLIKASI
# =====================================

st.title("📋 Formulir Audit Sistem Informasi Absensi")
st.subheader("PT Karya Busana Muria")
st.caption("Audit Sistem Informasi menggunakan Kerangka Kerja COBIT 5")

st.info(
    "Formulir ini merupakan simulasi akademik berdasarkan perusahaan "
    "fiktif PT Karya Busana Muria. Jawaban responden digunakan untuk "
    "keperluan pembelajaran dan tidak menggambarkan hasil audit nyata."
)

st.markdown("### Petunjuk Pengisian")

st.write(
    "Baca setiap pertanyaan dan pilih jawaban berdasarkan informasi "
    "skenario studi kasus yang diberikan dalam tugas."
)

st.write("- Ya: pengendalian diterapkan dan didukung informasi dalam skenario.")
st.write("- Tidak: pengendalian tidak diterapkan atau tidak didukung informasi dalam skenario.")
st.write("- N/A: pertanyaan tidak relevan dengan kondisi objek simulasi.")

st.divider()

# =====================================
# FORMULIR RESPONDEN
# =====================================

with st.form("form_audit"):

    st.markdown("### Identitas Responden")
    nama = st.text_input("Nama responden (opsional)")

    jawaban = []
    domain_sebelumnya = ""

    for nomor, (domain, kode, teks) in enumerate(pertanyaan, start=1):

        if domain != domain_sebelumnya:
            st.markdown(f"### Domain {domain}")
            domain_sebelumnya = domain

        st.markdown(f"**{nomor}. {kode}**")
        st.write(teks)

        pilihan = st.selectbox(
            "Pilih jawaban",
            ["Pilih jawaban", "Ya", "Tidak", "N/A"],
            key=f"jawaban_{nomor}"
        )

        jawaban.append(pilihan)
        st.divider()

    dikirim = st.form_submit_button(
        "Kirim Jawaban Audit",
        use_container_width=True
    )

# =====================================
# PROSES PENGIRIMAN
# =====================================

if dikirim:

    if "Pilih jawaban" in jawaban:
        st.error("Masih ada pertanyaan yang belum dijawab.")

    else:

        data_kirim = {
            "nama": nama.strip() if nama.strip() else "Anonim",
            "jawaban": jawaban
        }

        try:

            with st.spinner("Mengirim jawaban ke Google Sheets..."):

                hasil = requests.post(
                    URL_APPS_SCRIPT,
                    json=data_kirim,
                    timeout=30
                )

            if hasil.status_code == 200:

                try:
                    hasil_json = hasil.json()
                except Exception:
                    hasil_json = {}

                if hasil_json.get("status") == "success":
                    st.success("Jawaban berhasil dikirim dan disimpan!")
                else:
                    st.error("Jawaban belum dapat dipastikan tersimpan.")
                    st.write(hasil.text)

            else:
                st.error(f"Pengiriman gagal. Kode: {hasil.status_code}")

        except Exception as e:
            st.error(f"Terjadi kesalahan saat mengirim jawaban: {e}")

# =====================================
# DASHBOARD HASIL RESPONDEN
# =====================================

st.divider()
st.title("📊 Dashboard Hasil Audit Sistem Absensi")

try:

    response = requests.get(
        URL_APPS_SCRIPT,
        timeout=30
    )

    response.raise_for_status()
    hasil_data = response.json()

    if hasil_data.get("status") == "success":

        headers = hasil_data.get("headers", [])
        rows = hasil_data.get("rows", [])

        if rows:

            df_responden = pd.DataFrame(
                rows,
                columns=headers
            )

            # Nomor urut tabel responden dimulai dari 1
            df_responden.index = range(
                1,
                len(df_responden) + 1
            )

            df_responden.index.name = "No"

            kolom_jawaban = [
                kolom for kolom in headers
                if kolom.startswith(
                    ("EDM", "APO", "BAI", "DSS", "MEA")
                )
            ]

            if kolom_jawaban:

                # =====================================
                # RINGKASAN JAWABAN
                # =====================================

                st.subheader("Ringkasan Jawaban")

                semua_jawaban = (
                    df_responden[kolom_jawaban]
                    .values.flatten()
                )

                jumlah_ya = sum(semua_jawaban == "Ya")
                jumlah_tidak = sum(semua_jawaban == "Tidak")
                jumlah_na = sum(semua_jawaban == "N/A")

                c1, c2, c3, c4 = st.columns(4)

                c1.metric(
                    "Total Responden",
                    len(df_responden)
                )

                c2.metric(
                    "Jawaban Ya",
                    int(jumlah_ya)
                )

                c3.metric(
                    "Jawaban Tidak",
                    int(jumlah_tidak)
                )

                c4.metric(
                    "Jawaban N/A",
                    int(jumlah_na)
                )

                # =====================================
                # TABEL JAWABAN RESPONDEN
                # =====================================

                st.subheader("Tabel Jawaban Responden")

                st.dataframe(
                    df_responden,
                    use_container_width=True
                )

                # =====================================
                # REKAPITULASI DOMAIN
                # =====================================

                rekap = []

                for domain in ["EDM", "APO", "BAI", "DSS", "MEA"]:

                    kolom_domain = [
                        kolom for kolom in kolom_jawaban
                        if kolom.startswith(domain)
                    ]

                    nilai = (
                        df_responden[kolom_domain]
                        .values.flatten()
                    )

                    ya = int(sum(nilai == "Ya"))
                    tidak = int(sum(nilai == "Tidak"))
                    na = int(sum(nilai == "N/A"))

                    total_valid = ya + tidak

                    persentase = (
                        ya / total_valid * 100
                        if total_valid > 0 else 0
                    )

                    rekap.append({
                        "Domain": domain,
                        "Ya": ya,
                        "Tidak": tidak,
                        "N/A": na,
                        "Persentase Ya (%)": round(
                            persentase,
                            2
                        )
                    })

                df_rekap = pd.DataFrame(rekap)

                # Nomor urut tabel rekapitulasi dimulai dari 1
                df_rekap.index = range(
                    1,
                    len(df_rekap) + 1
                )

                df_rekap.index.name = "No"

                st.subheader("Rekapitulasi per Domain COBIT 5")

                st.dataframe(
                    df_rekap,
                    use_container_width=True
                )

                # =====================================
                # GRAFIK JAWABAN
                # =====================================

                st.subheader("Grafik Jawaban")

                grafik_jawaban = df_rekap.melt(
                    id_vars="Domain",
                    value_vars=["Ya", "Tidak", "N/A"],
                    var_name="Jawaban",
                    value_name="Jumlah"
                )

                maks_jawaban = int(
                    grafik_jawaban.groupby("Domain")["Jumlah"]
                    .sum()
                    .max()
                )

                chart_jawaban = (
                    alt.Chart(grafik_jawaban)
                    .mark_bar()
                    .encode(
                        x=alt.X(
                            "Domain:N",
                            title="Domain COBIT 5",
                            sort=["EDM", "APO", "BAI", "DSS", "MEA"]
                        ),
                        y=alt.Y(
                            "Jumlah:Q",
                            title="Jumlah Jawaban",
                            stack="zero",
                            scale=alt.Scale(
                                domain=[0, maks_jawaban],
                                nice=False
                            ),
                            axis=alt.Axis(
                                tickMinStep=1,
                                format="d"
                            )
                        ),
                        color=alt.Color(
                            "Jawaban:N",
                            title="Kategori Jawaban",
                            scale=alt.Scale(
                                domain=["Ya", "Tidak", "N/A"],
                                range=[
                                    "#FF3030",
                                    "#80C4F8",
                                    "#0066CC"
                                ]
                            )
                        ),
                        tooltip=[
                            "Domain",
                            "Jawaban",
                            "Jumlah"
                        ]
                    )
                    .properties(height=400)
                )

                st.altair_chart(
                    chart_jawaban,
                    use_container_width=True
                )

                # =====================================
                # GRAFIK PERSENTASE PER DOMAIN
                # =====================================

                st.subheader("Grafik Persentase per Domain")

                grafik_persentase = df_rekap[
                    ["Domain", "Persentase Ya (%)"]
                ]

                chart_persentase = (
                    alt.Chart(grafik_persentase)
                    .mark_bar(color="#0066CC")
                    .encode(
                        x=alt.X(
                            "Domain:N",
                            title="Domain COBIT 5",
                            sort=["EDM", "APO", "BAI", "DSS", "MEA"]
                        ),
                        y=alt.Y(
                            "Persentase Ya (%):Q",
                            title="Persentase Ya (%)",
                            scale=alt.Scale(
                                domain=[0, 100],
                                nice=False
                            ),
                            axis=alt.Axis(
                                tickMinStep=20,
                                format=".0f"
                            )
                        ),
                        tooltip=[
                            "Domain",
                            "Persentase Ya (%)"
                        ]
                    )
                    .properties(height=400)
                )

                st.altair_chart(
                    chart_persentase,
                    use_container_width=True
                )

        else:

            st.info("Belum ada jawaban responden.")

    else:

        st.error("Data Google Sheets belum berhasil dibaca.")

except Exception as e:

    st.error(
        f"Gagal mengambil data Google Sheets: {e}"
    )
