import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Lampiran", layout="wide")

st.title("Lampiran Data & Metodologi")
st.markdown("Halaman ini berisi tabel referensi, metodologi kalkulasi, dan data mentah yang digunakan sebagai landasan (*ground truth*) dalam ECC Intelligence System.")

st.write("---")

st.header("Lampiran 1: Rincian Kalkulasi Kapasitas PLTU Captive di Sulawesi")

st.markdown("""
**Referensi Kolom Data Mentah (`sulawesi_pltu_captive.csv`):**
*   **Filter Status:** Kolom `Status`
*   **Nama Pabrik:** Kolom `Plant name`
*   **Kapasitas:** Kolom `Capacity (MW)`
*   **Tahun Beroperasi:** Kolom `Start year`
""")

html_table = """
<style>
.ecc-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.9em;
    margin-bottom: 20px;
}
.ecc-table th, .ecc-table td {
    border: 1px solid #444;
    padding: 10px;
    text-align: left;
}
.ecc-table th {
    background-color: #262730;
    font-weight: bold;
}
.subtotal-row {
    background: linear-gradient(90deg, #1c3d5a 0%, #112233 100%);
    font-weight: bold;
}
.subtotal-row-2 {
    background: linear-gradient(90deg, #5a3d1c 0%, #332211 100%);
    font-weight: bold;
}
.grandtotal-row {
    background: linear-gradient(90deg, #5a1c1c 0%, #331111 100%);
    font-weight: bold;
}
</style>

<table class="ecc-table">
  <thead>
    <tr>
      <th>Kategori Filter</th>
      <th>Status GEM</th>
      <th>Penjelasan Status</th>
      <th>Daftar Nama Fasilitas / Pabrik</th>
      <th>Lokasi Baris Data (Index Raw Dataset)</th>
      <th>Kapasitas (MW)</th>
      <th>Data Tahun Beroperasi</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Kalkulasi "Udara 1"</strong><br>*(Asap Polusi Saat Ini)*</td>
      <td><strong>1. <code>operating</code></strong></td>
      <td>PLTU sudah aktif beroperasi penuh dan menghasilkan emisi ke udara.</td>
      <td>1. Delong Phase I, II, III, & IV, 2. Sulawesi Labota (IMIP), 3. Sulawesi Mining (IMIP), 4. PT IHIP, 5. Qingdao Zhongsheng, 6. Wanxiang Nickel, 7. Pomalaa Nickel, 8. Tonasa Cement</td>
      <td><strong>Total 55 Baris:</strong><br>(Tersebar di indeks 9744 s/d 10131)</td>
      <td>9.825 MW</td>
      <td><strong>2015 - 2024</strong></td>
    </tr>
    <tr class="subtotal-row">
      <td></td>
      <td>SUB-TOTAL AKTIF<br>(Udara 1)</td>
      <td colspan="3">Hanya menghitung unit PLTU yang sudah beroperasi secara komersial dan berkontribusi langsung pada emisi aktual.</td>
      <td>9.825 MW</td>
      <td></td>
    </tr>
    <tr>
      <td rowspan="4"><strong>Tambahan untuk "Veto 3"</strong><br>*(Ancaman Ekspansi)*</td>
      <td><strong>2. <code>construction</code></strong></td>
      <td>Konstruksi fisik (tiang/pabrik) sedang dibangun, akan beroperasi segera.</td>
      <td>1. Delong Phase IV</td>
      <td><strong>Total 1 Baris:</strong><br>(Baris ke-9775)</td>
      <td>330 MW</td>
      <td>-</td>
    </tr>
    <tr>
      <td><strong>3. <code>announced</code></strong></td>
      <td>Rencana ekspansi unit diumumkan resmi, tapi belum dibangun.</td>
      <td>1. PT IHIP</td>
      <td><strong>Total 1 Baris:</strong><br>(Baris ke-9999)</td>
      <td>100 MW</td>
      <td>-</td>
    </tr>
    <tr>
      <td><strong>4. <code>permitted</code></strong></td>
      <td>Izin amdal & lingkungan disahkan, tapi konstruksi belum mulai.</td>
      <td>*(Tidak ada data di Sulawesi)*</td>
      <td>-</td>
      <td>0 MW</td>
      <td>-</td>
    </tr>
    <tr>
      <td><strong>5. <code>pre-permit</code></strong></td>
      <td>Masih dalam tahap awal pengurusan perizinan (Amdal).</td>
      <td>*(Tidak ada data di Sulawesi)*</td>
      <td>-</td>
      <td>0 MW</td>
      <td>-</td>
    </tr>
    <tr class="subtotal-row-2">
      <td></td>
      <td>SUB-TOTAL PIPELINE<br>(Veto 3)</td>
      <td colspan="3">Menghitung Total Pipa Ekspansi Aktif (Operating + Construction + Announced)</td>
      <td>10.255 MW<br>(10,26 GW)</td>
      <td></td>
    </tr>
    <tr>
      <td rowspan="4"><strong>Tidak Dihitung Dasbor</strong><br>*(Mangkrak / Batal / Mati)*</td>
      <td><strong>6. <code>shelved</code></strong></td>
      <td>Ekspansi proyek ditangguhkan / mangkrak tanpa batas waktu.</td>
      <td>1. Delong Phase III</td>
      <td><strong>Total 5 Baris:</strong><br>(Baris ke-9751 s/d 9755)</td>
      <td>1.350 MW</td>
      <td>-</td>
    </tr>
    <tr>
      <td><strong>7. <code>cancelled</code></strong></td>
      <td>Ekspansi proyek resmi dibatalkan (biasanya karena ditolak/dana).</td>
      <td>1. Qingdao Zhongsheng, 2. Delong Phase II</td>
      <td><strong>Total 5 Baris:</strong><br>(Baris ke-9766 & 10012 s/d 10015)</td>
      <td>640 MW</td>
      <td>-</td>
    </tr>
    <tr>
      <td><strong>8. <code>mothballed</code></strong></td>
      <td>PLTU dinonaktifkan sementara waktu, tapi mesin belum dibongkar.</td>
      <td>*(Tidak ada data di Sulawesi)*</td>
      <td>-</td>
      <td>0 MW</td>
      <td>-</td>
    </tr>
    <tr>
      <td><strong>9. <code>retired</code></strong></td>
      <td>PLTU sudah ditutup/dibongkar secara permanen (pensiun).</td>
      <td>*(Tidak ada data di Sulawesi)*</td>
      <td>-</td>
      <td>0 MW</td>
      <td>-</td>
    </tr>
    <tr class="grandtotal-row">
      <td>-</td>
      <td>GRAND TOTAL</td>
      <td colspan="3">Keseluruhan riwayat rencana proyek di database</td>
      <td>12.245 MW</td>
      <td></td>
    </tr>
  </tbody>
</table>
"""
st.markdown(html_table, unsafe_allow_html=True)

st.write("---")

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Dropdown dataset 1 (Filtered)
with st.expander("Lihat Data Mentah: sulawesi_pltu_captive.csv", expanded=False):
    st.markdown("Tabel di bawah ini memuat langsung isi dari file CSV murni khusus untuk PLTU Captive di Sulawesi. Anda dapat mencocokkan nomor baris (*index*) yang tertera pada **Lampiran 1** dengan data mentah di bawah.")
    
    data_path = os.path.join(base_dir, 'data', 'processed', 'sulawesi_pltu_captive.csv')
    try:
        df = pd.read_csv(data_path)
        st.dataframe(df, use_container_width=True)
        st.caption("Sumber: `sulawesi_pltu_captive.csv` (Global Energy Monitor 2023)")
    except Exception as e:
        st.error(f"Gagal memuat dataset: {e}")

# Dropdown dataset 2 (Raw GEM Global)
with st.expander("Lihat Data Mentah: Global Energy Monitor (Raw Dataset)", expanded=False):
    st.markdown("Tabel di bawah ini memuat *raw dataset* global dari GEM sebelum dilakukan pemilahan khusus PLTU Captive Sulawesi.")
    
    raw_gem_path = os.path.join(base_dir, 'data', 'raw', 'izin_ESDM', 'gem-data', 'Global-Coal-Plant-Tracker-January-2026.xlsx')
    try:
        df_gem_raw = pd.read_excel(raw_gem_path, sheet_name='Units')
        st.dataframe(df_gem_raw, use_container_width=True)
    except Exception as e:
        st.error(f"Gagal memuat raw dataset GEM: {e}")
