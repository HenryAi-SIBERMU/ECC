"""
extract_chapter_4.py
100% faithful extraction of pages/4_Konflik_Sosial.py → chapter_4.md
"""
import os, sys, re, textwrap
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import scipy.stats as stats
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DATA = ROOT / "data" / "processed"
VIS  = HERE / "visuals_bab4"
VIS.mkdir(exist_ok=True)

def save_plotly(fig, path, w=900, h=500):
    fig.write_image(str(path), width=w, height=h, scale=2)

# ─── DATA LOAD ───────────────────────────────────────────────────────────────
def load_konflik_data_full():
    df = pd.read_csv(DATA / "sulawesi_konflik_agraria_tanahkita.csv")
    keywords = r'\b(sulawesi|sulsel|sulteng|sultra|sulut|sulbar|gorontalo|morowali|konawe|kolaka|bombana|poso|donggala|makassar|manado|minahasa|sangihe|mamuju|majene|polewali|halmahera|maluku utara|weda|obi|soroako|luwu|bantaeng|buton|muna|wakatobi|banggai|buol|toli-toli|parigi|luwuk|kendari|baubau|palu|bitung|tomohon|kotamobagu|gowa|takalar|jeneponto|bulukumba|sinjai|bone|maros|pangkep|barru|pinrang|enrekang|toraja|palopo)\b'
    mask = (df['judul'].str.contains(keywords, case=False, na=False, regex=True) |
            df['deskripsi'].str.contains(keywords, case=False, na=False, regex=True) |
            df['narasi'].str.contains(keywords, case=False, na=False, regex=True) |
            df['lokasi'].str.contains(keywords, case=False, na=False, regex=True))
    return df[mask].copy()

df_konflik = load_konflik_data_full()

# ─── METRIC CALCULATIONS ─────────────────────────────────────────────────────
total_konflik       = len(df_konflik)
konflik_kebun       = len(df_konflik[df_konflik['status'].str.contains('Perkebunan', case=False, na=False)])
konflik_tambang     = len(df_konflik[df_konflik['status'].str.contains('Pertambangan', case=False, na=False)])
konflik_hutan       = len(df_konflik[df_konflik['status'].str.contains('Hutan', case=False, na=False)])
konflik_infrastruktur = len(df_konflik[df_konflik['status'].str.contains('Infrastruktur|Bendungan|Transmigrasi|Energi|Fasilitas|Jalan', case=False, na=False)])
konflik_pariwisata  = len(df_konflik[df_konflik['status'].str.contains('Pariwisata|Konservasi Laut', case=False, na=False)])
rasio_ekstraktif    = ((konflik_tambang + konflik_kebun + konflik_hutan) / total_konflik) * 100 if total_konflik > 0 else 0

df_konflik['dampak_masyarakat_jiwa'] = pd.to_numeric(df_konflik['dampak_masyarakat_jiwa'], errors='coerce').fillna(0)
total_jiwa           = int(df_konflik['dampak_masyarakat_jiwa'].sum())
status_belum_selesai = len(df_konflik[df_konflik['status_konflik'].str.contains('Belum Ditangani', na=False)])
libat_pemerintah     = df_konflik['keterlibatan_pemerintah'].notna().sum()
libat_perusahaan     = df_konflik['keterlibatan_perusahaan'].notna().sum()
libat_masyarakat     = df_konflik['keterlibatan_masyarakat'].notna().sum()

# ─── SEKTOR MAPPING ──────────────────────────────────────────────────────────
def map_sektor(status):
    status = str(status).lower()
    if 'kebun' in status: return 'Perkebunan'
    if 'tambang' in status: return 'Pertambangan'
    if 'hutan' in status: return 'Kehutanan'
    if any(x in status for x in ['infrastruktur','bendungan','transmigrasi','energi','fasilitas','jalan','industri']): return 'Infrastruktur & PSN'
    if any(x in status for x in ['pariwisata','laut','pesisir']): return 'Pariwisata & Pesisir'
    return 'Lainnya'

df_ts = df_konflik.copy()
df_ts['Sektor_Grup'] = df_ts['status'].apply(map_sektor)
df_ts_modern = df_ts[df_ts['tahun'] >= 1990]

# 4.1 time series metrics
total_ts  = len(df_ts)
pasca_2005 = len(df_ts[df_ts['tahun'] >= 2005])
pra_2005   = len(df_ts[df_ts['tahun'] < 2005])
lonjakan   = (pasca_2005 / pra_2005 * 100) if pra_2005 > 0 else 0

# 4.2 sector damage
df_dampak = df_ts.copy()
df_dampak['dampak_masyarakat_jiwa'] = pd.to_numeric(df_dampak['dampak_masyarakat_jiwa'], errors='coerce').fillna(0)
df_dampak['luas_ha'] = pd.to_numeric(df_dampak['luas_ha'], errors='coerce').fillna(0)
df_sektor_agg = df_dampak.groupby('Sektor_Grup').agg({'dampak_masyarakat_jiwa':'sum','luas_ha':'sum'}).reset_index()
df_sektor_agg = df_sektor_agg[df_sektor_agg['Sektor_Grup'] != 'Lainnya']

jiwa_kehutanan = df_sektor_agg[df_sektor_agg['Sektor_Grup']=='Kehutanan']['dampak_masyarakat_jiwa'].sum()
jiwa_tambang   = df_sektor_agg[df_sektor_agg['Sektor_Grup']=='Pertambangan']['dampak_masyarakat_jiwa'].sum()
ha_kebun       = df_sektor_agg[df_sektor_agg['Sektor_Grup']=='Perkebunan']['luas_ha'].sum()
ha_kehutanan   = df_sektor_agg[df_sektor_agg['Sektor_Grup']=='Kehutanan']['luas_ha'].sum()
ha_tambang     = df_sektor_agg[df_sektor_agg['Sektor_Grup']=='Pertambangan']['luas_ha'].sum()

# 4.3 kriminalisasi
df_dampak['jumlah_ditangkap'] = pd.to_numeric(df_dampak['jumlah_ditangkap'], errors='coerce').fillna(0)
df_dampak['jumlah_luka']      = pd.to_numeric(df_dampak['jumlah_luka'], errors='coerce').fillna(0)
df_dampak['jumlah_tewas']     = pd.to_numeric(df_dampak['jumlah_tewas'], errors='coerce').fillna(0)
total_kriminalisasi = df_dampak[df_dampak['indikasi_kriminalisasi'] == True].shape[0]
total_ditangkap     = int(df_dampak['jumlah_ditangkap'].sum())
total_luka          = int(df_dampak['jumlah_luka'].sum())
total_tewas         = int(df_dampak['jumlah_tewas'].sum())

df_krim_tahun  = df_dampak[(df_dampak['indikasi_kriminalisasi'] == True) & (df_dampak['tahun'] >= 2000)].groupby('tahun').size().reset_index(name='jumlah_kasus')
df_krim_sektor = df_dampak[(df_dampak['indikasi_kriminalisasi'] == True) & (df_dampak['Sektor_Grup'] != 'Lainnya')].groupby('Sektor_Grup').size().reset_index(name='jumlah_kasus').sort_values('jumlah_kasus', ascending=True)
top_sektor       = df_krim_sektor.iloc[-1]['Sektor_Grup'] if not df_krim_sektor.empty else "Industri"
top_sektor_count = df_krim_sektor.iloc[-1]['jumlah_kasus'] if not df_krim_sektor.empty else 0
top_tahun        = int(df_krim_tahun.loc[df_krim_tahun['jumlah_kasus'].idxmax()]['tahun']) if not df_krim_tahun.empty else 0
top_tahun_count  = int(df_krim_tahun['jumlah_kasus'].max()) if not df_krim_tahun.empty else 0

# Before-After (4.4)
df_ba    = df_dampak[df_dampak['tahun'] >= 1990].copy()
df_pra   = df_ba[df_ba['tahun'] < 2014]
df_pasca = df_ba[df_ba['tahun'] >= 2014]
tahun_pra   = max(1, 2014 - int(df_pra['tahun'].min())) if not df_pra.empty else 24
tahun_pasca = max(1, int(df_pasca['tahun'].max()) - 2013) if not df_pasca.empty else 11
avg_pra   = len(df_pra) / tahun_pra
avg_pasca = len(df_pasca) / tahun_pasca

# ─── COLOR MAP ───────────────────────────────────────────────────────────────
color_map = {
    'Perkebunan':       '#FFC107',
    'Kehutanan':        '#8BC34A',
    'Pertambangan':     '#FF9800',
    'Infrastruktur & PSN': '#03A9F4',
    'Pariwisata & Pesisir': '#E91E63',
    'Lainnya':          '#9E9E9E'
}

# ─── CROSSTAB DATA PREP ───────────────────────────────────────────────────────
df_crosstab = pd.read_csv(DATA / "sulawesi_konflik_agraria_tanahkita.csv")
df_crosstab['tahun'] = pd.to_numeric(df_crosstab['tahun'], errors='coerce')
df_crosstab = df_crosstab[df_crosstab['tahun'] >= 1990]
df_crosstab['Periode_Ekspansi']       = df_crosstab['tahun'].apply(lambda x: 'Pasca-ekspansi (≥ 2014)' if x >= 2014 else 'Pra-ekspansi (< 2014)')
df_crosstab['Sektor_Tambang']         = df_crosstab['status'].str.contains('Tambang|Pertambangan', case=False, na=False).apply(lambda x: 'Sektor Pertambangan' if x else 'Sektor Non-Tambang')
df_crosstab['Keterlibatan_Pemerintah']= df_crosstab['keterlibatan_pemerintah'].notna().apply(lambda x: 'Terlibat Aparat/Negara' if x else 'Tanpa Keterlibatan Negara')
df_crosstab['Indikasi_Kriminalisasi'] = df_crosstab['indikasi_kriminalisasi'].fillna(False).astype(bool).apply(lambda x: 'Ada Represi/Kriminalisasi' if x else 'Baseline (Tanpa Kriminalisasi)')
df_crosstab['Status_Penyelesaian']    = df_crosstab['status_konflik'].str.contains('Belum Ditangani', na=False).apply(lambda x: 'Konflik Dibiarkan Terlantar' if x else 'Konflik Selesai/Diproses')
has_luka   = pd.to_numeric(df_crosstab['jumlah_luka'],    errors='coerce').fillna(0) > 0
has_tewas  = pd.to_numeric(df_crosstab['jumlah_tewas'],   errors='coerce').fillna(0) > 0
has_tangkap= pd.to_numeric(df_crosstab['jumlah_ditangkap'], errors='coerce').fillna(0) > 0
df_crosstab['Dampak_Kekerasan']       = (has_luka | has_tewas | has_tangkap).apply(lambda x: 'Terjadi Kekerasan/Penangkapan' if x else 'Tanpa Insiden Fisik')

x_options = {
    "Periode_Ekspansi": "Periode Ekspansi Industri",
    "Sektor_Tambang": "Tipe Sektor (Tambang vs Non-Tambang)",
    "Keterlibatan_Pemerintah": "Keterlibatan Aparat/Pemerintah"
}
y_options = {
    "Indikasi_Kriminalisasi": "Tingkat Represi & Kriminalisasi",
    "Status_Penyelesaian": "Tingkat Penelantaran Kasus",
    "Dampak_Kekerasan": "Tingkat Insiden Fisik (Luka/Tewas/Ditangkap)"
}
x_order = {
    "Periode_Ekspansi":       ['Pra-ekspansi (< 2014)', 'Pasca-ekspansi (≥ 2014)'],
    "Sektor_Tambang":         ['Sektor Non-Tambang', 'Sektor Pertambangan'],
    "Keterlibatan_Pemerintah":['Tanpa Keterlibatan Negara', 'Terlibat Aparat/Negara']
}
y_order = {
    "Indikasi_Kriminalisasi": ['Baseline (Tanpa Kriminalisasi)', 'Ada Represi/Kriminalisasi'],
    "Dampak_Kekerasan":       ['Tanpa Insiden Fisik', 'Terjadi Kekerasan/Penangkapan'],
    "Status_Penyelesaian":    ['Konflik Selesai/Diproses', 'Konflik Dibiarkan Terlantar']
}

# ─── RENDER CHARTS ───────────────────────────────────────────────────────────
print("Rendering 4.1 Chart ...")
df_agg = df_ts_modern.groupby(['tahun','Sektor_Grup']).size().reset_index(name='Jumlah')
fig_ts = px.bar(df_agg, x='tahun', y='Jumlah', color='Sektor_Grup', color_discrete_map=color_map,
                title='Peningkatan Signifikan Konflik Agraria di Sulawesi (1990 - 2025)',
                labels={'tahun':'Tahun','Jumlah':'Total Letupan Konflik','Sektor_Grup':'Sektor Pemicu'})
fig_ts.update_layout(
    xaxis=dict(tickmode='linear', dtick=2),
    plot_bgcolor='white', paper_bgcolor='white',
    font=dict(color='#333'),
    hovermode='x unified',
    legend=dict(title="",orientation="h",yanchor="bottom",y=1.05,xanchor="center",x=0.5),
    margin=dict(t=80)
)
df_total_per_tahun = df_ts_modern.groupby('tahun').size().reset_index(name='Jumlah')
if not df_total_per_tahun.empty:
    max_row = df_total_per_tahun.loc[df_total_per_tahun['Jumlah'].idxmax()]
    peak_year, peak_value = int(max_row['tahun']), int(max_row['Jumlah'])
    fig_ts.add_annotation(x=peak_year, y=peak_value,
        text=f"Puncak Krisis:<br><b>{peak_value} Letupan ({peak_year})</b>",
        showarrow=True, arrowhead=2, arrowsize=1.5, arrowwidth=2, arrowcolor="#D32F2F",
        ax=-40, ay=-50, font=dict(size=12,color="#B71C1C"),
        bgcolor="rgba(211,47,47,0.15)", bordercolor="#B71C1C", borderwidth=1, borderpad=4)
    if 2006 in df_total_per_tahun['tahun'].values:
        val_2006 = int(df_total_per_tahun[df_total_per_tahun['tahun']==2006]['Jumlah'].values[0])
        fig_ts.add_annotation(x=2006, y=val_2006,
            text=f"Eskalasi Ekstraktif Dimulai<br><b>{val_2006} Kasus (2006)</b>",
            showarrow=True, arrowhead=2, arrowsize=1.5, arrowwidth=2, arrowcolor="#F57C00",
            ax=-50, ay=-40, font=dict(size=11,color="#E65100"),
            bgcolor="rgba(245,124,0,0.15)", bordercolor="#E65100", borderwidth=1, borderpad=4)
save_plotly(fig_ts, VIS / "chart_4_1_konflik_timeseries.png", w=1000, h=500)

print("Rendering 4.2 Charts ...")
df_sektor_tahun = df_dampak[df_dampak['tahun'] >= 1990].groupby(['tahun','Sektor_Grup']).agg(
    {'dampak_masyarakat_jiwa':'sum','luas_ha':'sum'}).reset_index()

fig_jiwa = px.bar(df_sektor_tahun, x='tahun', y='dampak_masyarakat_jiwa', color='Sektor_Grup',
    title='Peningkatan Signifikan Korban Terdampak (Jiwa) per Tahun', color_discrete_map=color_map,
    labels={'dampak_masyarakat_jiwa':'Total Korban (Jiwa)','tahun':'Tahun','Sektor_Grup':'Sektor Pemicu'}, barmode='stack')
fig_jiwa.update_layout(showlegend=False, plot_bgcolor='white', paper_bgcolor='white',
    font=dict(color='#333'),
    xaxis=dict(tickmode='linear',dtick=2),
    yaxis=dict(showgrid=True,gridcolor='rgba(0,0,0,0.1)'), margin=dict(t=60,b=40))
top_jiwa = df_sektor_tahun.groupby('tahun')['dampak_masyarakat_jiwa'].sum().sort_values(ascending=False)
top_jiwa = top_jiwa[top_jiwa > 0].head(2)
for i, (year, val) in enumerate(top_jiwa.items(), 1):
    fig_jiwa.add_annotation(x=year, y=val,
        text=f"<b>Anomali Jiwa {i}</b>",
        showarrow=True, arrowhead=2, arrowcolor="#FF5252", ax=0, ay=-35,
        font=dict(size=11,color="white"), bgcolor="rgba(211,47,47,0.8)", bordercolor="#FF5252")
save_plotly(fig_jiwa, VIS / "chart_4_2a_jiwa.png", w=700, h=400)

fig_ha = px.bar(df_sektor_tahun, x='tahun', y='luas_ha', color='Sektor_Grup',
    title='Monopoli Area Konflik (Hektar) per Tahun', color_discrete_map=color_map,
    labels={'luas_ha':'Luas Daratan (Hektar)','tahun':'Tahun','Sektor_Grup':'Sektor Pemicu'}, barmode='stack')
fig_ha.update_layout(showlegend=False, plot_bgcolor='white', paper_bgcolor='white',
    font=dict(color='#333'),
    xaxis=dict(tickmode='linear',dtick=2),
    yaxis=dict(showgrid=True,gridcolor='rgba(0,0,0,0.1)'), margin=dict(t=60,b=40))
top_ha = df_sektor_tahun.groupby('tahun')['luas_ha'].sum().sort_values(ascending=False)
top_ha = top_ha[top_ha > 0].head(2)
for i, (year, val) in enumerate(top_ha.items(), 1):
    fig_ha.add_annotation(x=year, y=val,
        text=f"<b>Anomali Area {i}</b>",
        showarrow=True, arrowhead=2, arrowcolor="#FFC107", ax=0, ay=-35,
        font=dict(size=11,color="#333"), bgcolor="rgba(255,193,7,0.9)", bordercolor="#FFB300")
save_plotly(fig_ha, VIS / "chart_4_2b_ha.png", w=700, h=400)

print("Rendering 4.3 Charts ...")
fig_krim_tahun = px.line(df_krim_tahun, x='tahun', y='jumlah_kasus', markers=True,
    title='Tren Kasus Kriminalisasi & Represi (Pasca 2000)',
    labels={'jumlah_kasus':'Total Kasus','tahun':'Tahun Kejadian'})
fig_krim_tahun.update_traces(line_color='#E53935', marker=dict(size=8, color='#B71C1C'))
fig_krim_tahun.update_layout(plot_bgcolor='white', paper_bgcolor='white', font=dict(color='#333'),
    xaxis=dict(showgrid=False,tickmode='linear',dtick=2),
    yaxis=dict(showgrid=True,gridcolor='rgba(0,0,0,0.1)'), margin=dict(t=50,b=40))
save_plotly(fig_krim_tahun, VIS / "chart_4_3a_kriminalisasi_trend.png", w=700, h=400)

fig_krim_sektor = px.bar(df_krim_sektor, y='Sektor_Grup', x='jumlah_kasus', orientation='h',
    color='Sektor_Grup', color_discrete_map=color_map,
    title='Sektor Industri Paling Represif',
    labels={'jumlah_kasus':'Total Kasus','Sektor_Grup':'Sektor Pemicu'})
fig_krim_sektor.update_layout(showlegend=False, plot_bgcolor='white', paper_bgcolor='white',
    font=dict(color='#333'),
    xaxis=dict(showgrid=True,gridcolor='rgba(0,0,0,0.1)'),
    yaxis=dict(showgrid=False), margin=dict(t=50,b=40))
save_plotly(fig_krim_sektor, VIS / "chart_4_3b_sektor_represif.png", w=700, h=400)

print("Rendering 4.5 Charts ...")
df_nlp = pd.read_csv(DATA / "sulawesi_konflik_agraria_tanahkita.csv")
text_corpus = " ".join((df_nlp['judul'].fillna('') + " " + df_nlp['deskripsi'].fillna('') + " " + df_nlp['narasi'].fillna('')).tolist())
pts = re.findall(r'\b(?:PT|CV)\.?\s*[A-Z][a-zA-Z]*(?:\s+[A-Z][a-zA-Z]*){0,3}\b', text_corpus)
pts = [" ".join(pt.split()) for pt in pts]
pts = [re.sub(r'\bPTPN(?:\s+(?:XIV|XII|VII|II|14|Unit\s*14))?\b', 'PT Perkebunan Nusantara (PTPN)', pt, flags=re.IGNORECASE) for pt in pts]
df_aktor_perusahaan = pd.Series(pts).value_counts().reset_index()
df_aktor_perusahaan.columns = ['Aktor','Frekuensi']

civils_raw = re.findall(r'\b(?:Preman|Ormas|Satgas|PAM Swakarsa|Pemuda Pancasila|GRIB|Laskar|Tandingan|Oknum|Security|Satpam|Pengamanan Swakarsa|Centeng|Beking)\b[^\.,;!\?\(\)\[\]\"\'\\-]*', text_corpus, flags=re.IGNORECASE)
stopwords = {'yang','dan','di','dari','dengan','untuk','pada','ke','dalam','oleh','serta','sebagai','adalah','ini','itu','tersebut','kepada','saat','ketika','juga','mengatasnamakan','berjumlah','melarang','datang','berupaya','segera','salah','lainnya','tak','nya','sedang','akan','karena','sebab','lalu','kemudian','mereka'}
civils_clean = []
for phrase in civils_raw:
    words = phrase.split()
    clean_words = []
    for w in words:
        if w.lower() in stopwords: break
        clean_words.append(w.title())
    if clean_words: civils_clean.append(' '.join(clean_words))
df_aktor_masyarakat = pd.Series(civils_clean).value_counts().reset_index()
df_aktor_masyarakat.columns = ['Aktor','Frekuensi']

top_corp = df_aktor_perusahaan.head(10).sort_values('Frekuensi', ascending=True)
fig_corp = px.bar(top_corp, x='Frekuensi', y='Aktor', orientation='h', color_discrete_sequence=['#F57C00'])
fig_corp.update_layout(plot_bgcolor='white', paper_bgcolor='white', font=dict(color='#333'),
    margin=dict(l=0,r=0,t=10,b=0),
    xaxis=dict(showgrid=True,gridcolor='rgba(0,0,0,0.1)',tickformat='d'))
save_plotly(fig_corp, VIS / "chart_4_5a_korporasi.png", w=700, h=400)

top_civil = df_aktor_masyarakat.head(10).sort_values('Frekuensi', ascending=True)
fig_civil = px.bar(top_civil, x='Frekuensi', y='Aktor', orientation='h', color_discrete_sequence=['#D32F2F'])
fig_civil.update_layout(plot_bgcolor='white', paper_bgcolor='white', font=dict(color='#333'),
    margin=dict(l=0,r=0,t=10,b=0),
    xaxis=dict(showgrid=True,gridcolor='rgba(0,0,0,0.1)',tickformat='d'))
save_plotly(fig_civil, VIS / "chart_4_5b_vigilante.png", w=700, h=400)

top1_corp_name = df_aktor_perusahaan.iloc[0]['Aktor'] if not df_aktor_perusahaan.empty else "Korporasi"
top1_corp_freq = df_aktor_perusahaan.iloc[0]['Frekuensi'] if not df_aktor_perusahaan.empty else 0
top1_civ_name  = df_aktor_masyarakat.iloc[0]['Aktor'] if not df_aktor_masyarakat.empty else "Preman/Ormas"
top1_civ_freq  = df_aktor_masyarakat.iloc[0]['Frekuensi'] if not df_aktor_masyarakat.empty else 0

# ─── CROSSTAB CALCULATIONS ───────────────────────────────────────────────────
print("Computing Crosstabs ...")

def compute_crosstab(k_x, k_y):
    cx = x_order[k_x]; cy = y_order[k_y]
    ct = pd.crosstab(df_crosstab[k_x], df_crosstab[k_y]).reindex(index=cx, columns=cy, fill_value=0)
    try:
        c2, p, dof, exp = stats.chi2_contingency(ct)
    except:
        c2, p, dof, exp = 0, 1, 0, ct.values
    try:
        exp_df = pd.DataFrame(exp, index=cx, columns=cy)
    except:
        exp_df = pd.DataFrame(0.0, index=cx, columns=cy)
    try:
        aa = ct.loc[cx[0],cy[0]]; bb = ct.loc[cx[0],cy[1]]
        cc = ct.loc[cx[1],cy[0]]; dd = ct.loc[cx[1],cy[1]]
        or_v = (aa*dd)/(bb*cc) if (bb*cc) > 0 else 0
    except:
        or_v = 0
    return ct, exp_df, c2, p, dof, or_v

# Default view: Periode_Ekspansi vs Indikasi_Kriminalisasi
ct_default, exp_default, chi2_default, p_default, dof_default, or_default = compute_crosstab("Periode_Ekspansi","Indikasi_Kriminalisasi")

# Executive Summary All Combinations
summary_data = []
for k_x, v_x in x_options.items():
    for k_y, v_y in y_options.items():
        ct, exp, c2v, pv, dofv, orv = compute_crosstab(k_x, k_y)
        sig_status = "🟢 SIGNIFIKAN" if pv < 0.05 else "🔴 TIDAK SIGNIFIKAN"
        summary_data.append({
            "Variabel Independen (X)": v_x,
            "Variabel Dependen (Y)":   v_y,
            "Chi-Square": f"{c2v:.3f}",
            "P-Value":    f"{pv:.3f}",
            "Odds Ratio": f"{orv:.2f}",
            "Kesimpulan": sig_status
        })

sig_count = sum(1 for r in summary_data if "🟢 SIGNIFIKAN" in r["Kesimpulan"])
total_scenarios = len(summary_data)

if sig_count > 0:
    exec_narrative = (
        f"Dari **{total_scenarios} skenario pengujian**, terdapat **{sig_count} skenario yang terbukti SIGNIFIKAN**.\n\n"
        "Angka-angka pada tabel di atas bukan sekadar statistik di atas kertas, melainkan **bukti empiris** dari brutalitas pembangunan. "
        "Tingginya angka kemunculan represi pada skenario yang signifikan menegaskan bahwa setiap kali wilayah operasi investasi diperlebar, "
        "probabilitas dihadapkannya moncong senjata kepada warga melonjak drastis.\n\n"
        "Skenario yang *TIDAK SIGNIFIKAN* tidak berarti rezim terbebas dari dosa kekerasan, melainkan bukti bahwa represi terhadap warga "
        "yang mempertahankan tanahnya telah menjadi kultur mapan yang menyebar secara sporadis melampaui sekat waktu dan korporasi."
    )
else:
    exec_narrative = (
        f"Dari **{total_scenarios} skenario pengujian**, seluruhnya menunjukkan status **TIDAK SIGNIFIKAN**.\n\n"
        "Dalam kacamata ekonomi politik, ketidaksignifikanan secara agregat ini justru membuktikan bahwa aparatus represif telah dipekerjakan "
        "*sepanjang waktu secara stabil* dalam menggusur ruang hidup rakyat. Kekerasan bukanlah produk parsial satu rezim, melainkan "
        "instrumen fundamental yang menyokong eksistensi industri ekstraktif."
    )

is_significant_default = p_default < 0.05

# Exec summary table
exec_header = "| Variabel Independen (X) | Variabel Dependen (Y) | Chi-Square | P-Value | Odds Ratio | Kesimpulan |"
exec_sep    = "|---|---|---|---|---|---|"
exec_rows   = [exec_header, exec_sep]
for row in summary_data:
    exec_rows.append(f"| {row['Variabel Independen (X)']} | {row['Variabel Dependen (Y)']} | {row['Chi-Square']} | {row['P-Value']} | {row['Odds Ratio']} | {row['Kesimpulan']} |")
exec_table_md = "\n".join(exec_rows)

# ─── BUILD MARKDOWN ──────────────────────────────────────────────────────────
print("Writing 100% faithful chapter_4.md ...")

# Default crosstab table strings
total_cases_ct  = len(df_crosstab)
valid_cases_ct  = len(df_crosstab.dropna(subset=['Periode_Ekspansi','Indikasi_Kriminalisasi']))
missing_cases_ct= total_cases_ct - valid_cases_ct
x_lbl_ct = "Periode Ekspansi Industri"
y_lbl_ct = "Tingkat Represi & Kriminalisasi"
interaction_lbl = f"{x_lbl_ct} * {y_lbl_ct}"

cx_def = x_order["Periode_Ekspansi"]
cy_def = y_order["Indikasi_Kriminalisasi"]

# Crosstab rows for markdown table
def fmt_crosstab_md(ct, exp_df, cx, cy):
    header = "| | " + " | ".join(cy) + " | Total |"
    sep    = "|---|" + "|".join(["---"]*len(cy)) + "|---|"
    rows   = [header, sep]
    for x_cat in cx:
        counts = ct.loc[x_cat].tolist()
        exps   = exp_df.loc[x_cat].tolist()
        rows.append(f"| **{x_cat}** Count | " + " | ".join(str(v) for v in counts) + f" | {sum(counts)} |")
        rows.append(f"| **{x_cat}** Expected | " + " | ".join(f"{v:.1f}" for v in exps) + f" | {sum(exps):.1f} |")
    total_c = ct.sum().tolist()
    total_e = exp_df.sum().tolist()
    rows.append("| **Total** Count | " + " | ".join(str(v) for v in total_c) + f" | {sum(total_c)} |")
    rows.append("| **Total** Expected | " + " | ".join(f"{v:.1f}" for v in total_e) + f" | {sum(total_e):.1f} |")
    return "\n".join(rows)

crosstab_md = fmt_crosstab_md(ct_default, exp_default, cx_def, cy_def)

try:
    g_val, p_g, dof_g, _ = stats.chi2_contingency(ct_default, lambda_="log-likelihood")
except:
    g_val, p_g = 0, 1
x_codes = df_crosstab["Periode_Ekspansi"].replace({cx_def[0]:0, cx_def[1]:1})
y_codes = df_crosstab["Indikasi_Kriminalisasi"].replace({cy_def[0]:0, cy_def[1]:1})
try:
    r_val, p_corr = stats.pearsonr(list(x_codes), list(y_codes))
    lbl_val = (valid_cases_ct - 1) * (r_val**2)
except:
    r_val, p_corr, lbl_val = 0, 1, 0

status_text = "SIGNIFIKAN" if p_default < 0.05 else "TIDAK SIGNIFIKAN"

if p_default < 0.05:
    interp_text = (
        f"Temuan ini sangat krusial: pergeseran status **{x_lbl_ct}** terbukti **berkorelasi kuat dan signifikan** dengan **{y_lbl_ct}** "
        f"(P < 0.05). Angka Odds Ratio (OR: {or_default:.3f}) menjadi konfirmasi empiris bahwa narasi hilirisasi dan investasi bukanlah "
        "agenda nirkekerasan—ekspansi spasial mereka mutlak mengeskalasi pelanggaran hak asasi masyarakat tapak."
    )
else:
    interp_text = (
        f"Secara agregat, hubungan antara **{x_lbl_ct}** dan **{y_lbl_ct}** **tidak menunjukkan perbedaan yang signifikan** secara statistik "
        "(P >= 0.05). Hal ini mengindikasikan bahwa penggunaan instrumen kekerasan sudah mengakar dan sistematis di sepanjang sejarah konflik "
        "agraria tanpa memandang batas waktu rezim atau aktor yang terlihat."
    )

# BUILD ANOMALIES JIWA
jiwa_anomalies_md = ""
import urllib.parse
for i, year in enumerate(top_jiwa.index, 1):
    jiwa_anomalies_md += f"\n#### ANOMALI JIWA {i}: Lonjakan Korban Jiwa Tahun {year}\n"
    cases = df_konflik[df_konflik['tahun'] == year].copy()
    cases['jiwa_num'] = pd.to_numeric(cases['dampak_masyarakat_jiwa'].astype(str).replace(',', '', regex=True).replace(' Jiwa', '', regex=True), errors='coerce').fillna(0)
    top_case = cases.sort_values('jiwa_num', ascending=False).iloc[0] if not cases.empty else None
    
    if top_case is not None:
        judul = top_case['judul']
        korban = top_case['jiwa_num']
        pt = top_case['keterlibatan_perusahaan'] if pd.notna(top_case['keterlibatan_perusahaan']) else 'Tidak/Belum Teridentifikasi'
        narasi = str(top_case['narasi'])[:450] + "..." if pd.notna(top_case['narasi']) and str(top_case['narasi']).strip() != 'nan' else (str(top_case['deskripsi'])[:450] + "...")
        sumber_lsm = top_case['sumber'] if 'sumber' in top_case and pd.notna(top_case['sumber']) else 'Kompilasi LSM'
        tk_link = top_case['detail_url'] if 'detail_url' in top_case and pd.notna(top_case['detail_url']) else '#'
        search_query = urllib.parse.quote(f"{judul} {pt}")
        link = f"https://www.google.com/search?q={search_query}"
        
        jiwa_anomalies_md += f"- **Kasus Utama Pendongkrak Statistik:** {judul}\n"
        jiwa_anomalies_md += f"- **Total Korban (Kasus Ini):** {int(korban):,} Jiwa\n"
        jiwa_anomalies_md += f"- **Perusahaan Terlibat:** {pt}\n"
        jiwa_anomalies_md += f"- **Narasi Singkat:** {narasi}\n"
        jiwa_anomalies_md += f"- **Sumber Referensi:** Laporan {sumber_lsm} ([Telusuri Berita Kasus]({link}) | [Link Asli TanahKita]({tk_link}))\n"

# BUILD ANOMALIES AREA
ha_anomalies_md = ""
for i, year in enumerate(top_ha.index, 1):
    ha_anomalies_md += f"\n#### ANOMALI AREA {i}: Monopoli Area Konflik Tahun {year}\n"
    cases = df_konflik[df_konflik['tahun'] == year].copy()
    cases['ha_num'] = pd.to_numeric(cases['luas_ha'].astype(str).replace(',', '', regex=True).replace(' Ha', '', regex=True), errors='coerce').fillna(0)
    top_case = cases.sort_values('ha_num', ascending=False).iloc[0] if not cases.empty else None
    
    if top_case is not None:
        judul = top_case['judul']
        luas = top_case['ha_num']
        pt = top_case['keterlibatan_perusahaan'] if pd.notna(top_case['keterlibatan_perusahaan']) else 'Tidak/Belum Teridentifikasi'
        narasi = str(top_case['narasi'])[:450] + "..." if pd.notna(top_case['narasi']) and str(top_case['narasi']).strip() != 'nan' else (str(top_case['deskripsi'])[:450] + "...")
        sumber_lsm = top_case['sumber'] if 'sumber' in top_case and pd.notna(top_case['sumber']) else 'Kompilasi LSM'
        tk_link = top_case['detail_url'] if 'detail_url' in top_case and pd.notna(top_case['detail_url']) else '#'
        search_query = urllib.parse.quote(f"{judul} {pt}")
        link = f"https://www.google.com/search?q={search_query}"
        
        ha_anomalies_md += f"- **Kasus Utama Pendongkrak Statistik:** {judul}\n"
        ha_anomalies_md += f"- **Total Daratan Dirampas (Kasus Ini):** {int(luas):,} Hektar\n"
        ha_anomalies_md += f"- **Perusahaan Terlibat:** {pt}\n"
        ha_anomalies_md += f"- **Narasi Singkat:** {narasi}\n"
        ha_anomalies_md += f"- **Sumber Referensi:** Laporan {sumber_lsm} ([Telusuri Berita Kasus]({link}) | [Link Asli TanahKita]({tk_link}))\n"

md = f'''# Ruang Hidup yang Terampas

Analisis dinamika konflik sosial dan alokasi ruang agraria dalam konteks pembangunan kawasan.

---

Ekspansi industri ekstraktif dan proyek strategis berimplikasi pada dinamika sosial dan penggunaan lahan masyarakat. Data empiris mencatat akumulasi **{total_konflik} kasus konflik agraria**. Konflik ini berkaitan erat dengan perubahan tata guna lahan dan alokasi ruang di berbagai daerah.

Aktor dan sektor pemicu konflik mencakup sektor **Kehutanan** (Hutan Lindung, Produksi, Konservasi), **Infrastruktur & PSN** (Bendungan, Transmigrasi, Kawasan Industri), hingga proyek **Pariwisata & Pesisir**. Tiga sektor utama (Perkebunan, Kehutanan, dan Pertambangan) menyumbang porsi **{rasio_ekstraktif:.1f}%** dari keseluruhan catatan konflik.

---

### Ringkasan Metrik Agregat

| Indikator | Nilai | Keterangan |
|---|---|---|
| **Total Kasus Konflik** | **{total_konflik} kasus** | Catatan insiden sengketa agraria dan tata guna lahan. |
| **Korban Terdampak (Jiwa)** | **{total_jiwa:,} jiwa** | Estimasi jumlah warga yang terdampak oleh konflik sengketa lahan. |
| **Status: Belum Ditangani** | **{status_belum_selesai} kasus** | Kasus sengketa yang masih dalam proses penanganan. |
| **Komunitas Terdampak** | **{libat_masyarakat} komunitas** | Kelompok tani dan komunitas lokal yang terlibat dalam sengketa. |
| **Sektor Perkebunan** | **{konflik_kebun} kasus** | Sengketa tumpang tindih Hak Guna Usaha (HGU) perkebunan dengan lahan masyarakat. |
| **Sektor Kehutanan** | **{konflik_hutan} kasus** | Sengketa batas kawasan hutan produksi dan konservasi dengan wilayah kelola lokal. |
| **Sektor Pertambangan** | **{konflik_tambang} kasus** | Sengketa alokasi lahan untuk operasi pertambangan dan fasilitas hilirisasi. |
| **Infrastruktur & PSN** | **{konflik_infrastruktur} kasus** | Sengketa pengadaan tanah untuk Proyek Strategis Nasional. |
| **Pariwisata & Pesisir** | **{konflik_pariwisata} kasus** | Sengketa pemanfaatan wilayah pesisir dan kawasan pariwisata. |
| **Keterlibatan Pemerintah** | **{libat_pemerintah} kasus** | Keterlibatan instansi pemerintah dalam fasilitasi atau sengketa lahan. |
| **Keterlibatan Korporasi** | **{libat_perusahaan} kasus** | Entitas BUMN atau swasta yang terlibat dalam sengketa lahan. |

*Sumber Analisis Data: Konsorsium Pembaruan Agraria (KPA) / Tanah Kita*

---

### 4.1 Tren Eskalasi Konflik Agraria Seiring Ekspansi Industri

Visualisasi *time-series* di bawah ini memberikan gambaran korelasi antara ekspansi industri dan dinamika konflik agraria di daratan Sulawesi. Secara historis, perbandingan dua periode waktu menunjukkan perbedaan tingkat insidensi konflik. Pada periode pra-2005, sistem pendataan mencatat **{pra_2005} kasus** konflik agraria.

Pada periode pasca-2005 hingga saat ini, data mencatat **{pasca_2005} kasus** konflik lahan, yang mencerminkan peningkatan sebesar **{lonjakan:,.1f}%** dibandingkan periode sebelumnya. Perubahan tren ini beriringan dengan penerbitan Izin Usaha Pertambangan (IUP) serta ekspansi Hak Guna Usaha (HGU) untuk perkebunan.

Penelusuran tren satu dekade terakhir menunjukkan bahwa sengketa agraria mencakup berbagai sektor, termasuk pertambangan nikel, infrastruktur, dan Proyek Strategis Nasional. Akumulasi **{total_ts} insiden historis** ini mengindikasikan perlunya tata kelola alokasi lahan dan perlindungan hak masyarakat lokal yang lebih seimbang di kawasan investasi.

![Peningkatan Signifikan Konflik Agraria di Sulawesi (1990-2025)](visuals_bab4/chart_4_1_konflik_timeseries.png)

> **Interpretasi Ekologis: Puncak Insidensi Konflik 2017**
>
> Grafik memperlihatkan peningkatan insidensi konflik yang memuncak pada **tahun 2017** dengan **75 kasus konflik**. Pembedahan data sektoral menunjukkan konsentrasi pada sektor **Kehutanan (40 kasus)** dan **Perkebunan (21 kasus)**, diikuti oleh **Pertambangan dan Infrastruktur PSN**. Periode ini bertepatan dengan percepatan pelepasan kawasan hutan dan Izin Pinjam Pakai Kawasan Hutan (IPPKH) untuk mendukung proyek strategis dan kawasan industri.

> **Interpretasi Ekologis dan Sosial:**
>
> Peningkatan insidensi konflik beririsan dengan dinamika perizinan kawasan. Pengelolaan alokasi ruang dan perlindungan hak masyarakat di wilayah investasi menjadi faktor penting untuk meminimalkan dampak sosial.

---

### 4.2 Sebaran Sektoral: Dampak Masyarakat dan Penggunaan Lahan

Visualisasi komparatif di bawah ini menggambarkan skala dampak sosial dan penggunaan lahan berdasarkan sektor industri. Data menunjukkan bahwa **Sektor Kehutanan** mencatatkan jumlah warga terdampak sebanyak **{jiwa_kehutanan:,.0f} jiwa**, berkaitan dengan tumpang tindih kawasan hutan produksi, konservasi, dan Hutan Tanaman Industri (HTI) dengan wilayah kelola masyarakat lokal.

Menyusul berikutnya adalah **Sektor Pertambangan** dengan total korban terdampak sebanyak **{jiwa_tambang:,.0f} jiwa**, yang beririsan dengan proyek hilirisasi nikel dan tambang terbuka di kawasan pesisir dan pertanian.

Dari dimensi penggunaan lahan (luasan hektar yang terlibat sengketa), **Sektor Perkebunan** mencatatkan luas sengketa terbesar yaitu **{ha_kebun:,.0f} Hektar**, disusul oleh sektor Kehutanan seluas **{ha_kehutanan:,.0f} Ha** dan Pertambangan seluas **{ha_tambang:,.0f} Ha**. Data ini menunjukkan bahwa dinamika penguasaan lahan di tiga sektor tersebut berkorelasi dengan tingginya insidensi sengketa agraria di tingkat lokal.

![Peningkatan Signifikan Korban Terdampak (Jiwa) per Tahun](visuals_bab4/chart_4_2a_jiwa.png)

![Monopoli Area Konflik (Hektar) per Tahun](visuals_bab4/chart_4_2b_ha.png)

> **Interpretasi Ekologis dan Sosial:**
>
> Dinamika Grafik mencerminkan akumulasi dampak sosial di wilayah industri yang memerlukan perhatian dalam pengelolaan sengketa lahan.

### Bedah Forensik Anomali (Spike) Konflik Agraria

Berdasarkan ekstraksi dataset secara mendalam, berikut adalah bedah anatomis dari lonjakan-lonjakan ekstrem (*spikes*) yang terjadi pada grafik **Peningkatan Signifikan Korban Terdampak (Jiwa)** dan **Monopoli Area Konflik (Hektar)** di wilayah ini.

{jiwa_anomalies_md}

{ha_anomalies_md}

---

### 4.3 Indikasi Represi dan Kriminalisasi dalam Konflik Agraria

Data kuantitatif di wilayah Sulawesi mencatat indikasi terjadinya represi dan tindakan kriminalisasi dalam sebagian sengketa agraria. Dari database yang didokumentasikan, terdapat **{total_kriminalisasi} kasus indikasi kriminalisasi** dan **{total_ditangkap} warga/aktivis lingkungan yang tercatat pernah ditangkap** dalam penanganan sengketa lahan.

Berdasarkan distribusi sektoral, **Sektor {top_sektor}** mencatatkan frekuensi indikasi represi tertinggi dengan **{top_sektor_count} kasus**. Tahun dengan jumlah catatan insiden represi tertinggi adalah **{top_tahun}** dengan **{top_tahun_count} kasus**.

Catatan ini menunjukkan pentingnya pendekatan hukum yang adil, penyelesaian konflik secara ramah HAM, serta jaminan perlindungan bagi pejuang lingkungan dan komunitas lokal sesuai dengan peraturan perundang-undangan.

| Kasus Indikasi Kriminalisasi | Warga/Aktivis Ditangkap | Korban Luka-luka | Korban Tewas |
|---|---|---|---|
| **{total_kriminalisasi} Kasus** | **{total_ditangkap} Orang** | **{total_luka} Orang** | **{total_tewas} Orang** |

![Tren Kasus Kriminalisasi & Represi (Pasca 2000)](visuals_bab4/chart_4_3a_kriminalisasi_trend.png)

![Sektor Industri Paling Represif](visuals_bab4/chart_4_3b_sektor_represif.png)

> **Interpretasi Ekologis & Hak Asasi Manusia:** Keberadaan kasus kriminalisasi di sekitar area konsesi (terutama {top_sektor}) mengindikasikan pentingnya jaminan perlindungan ruang sipil dan penghormatan HAM dalam setiap proses pembangunan.

---

### 4.4 Pembuktian Statistik: Ekspansi vs Eskalasi Konflik

Hipotesis utama dalam evaluasi ini adalah bahwa **industrialisasi dan ekspansi korporasi** berbanding lurus dengan **eskalasi konflik dan represi** terhadap masyarakat. 
Untuk mengujinya secara statistik sesuai pedoman D3TLH, analisis dibagi menjadi dua bagian: (1) Komparasi metrik Before-After, dan (2) Uji signifikansi Crosstab Chi-Square. Unit observasinya adalah catatan kejadian letupan konflik historis.

#### A. Analisis Komparatif Before-After (Pra vs Era Hilirisasi)

Perbandingan absolut eskalasi konflik agraria sebelum dan sesudah rezim hilirisasi masif dimulai (cut-off tahun 2014).

| Periode | Rata-rata Konflik | Total Letupan | Warga Ditangkap | Korban Tewas |
|---|---|---|---|---|
| **Pra-Ekspansi (1990 - 2013)** | **{avg_pra:.1f} Kasus/Tahun** | {len(df_pra)} kejadian | {int(df_pra['jumlah_ditangkap'].sum())} jiwa | {int(df_pra['jumlah_tewas'].sum())} jiwa |
| **Pasca-Ekspansi (2014 - 2024)** | **{avg_pasca:.1f} Kasus/Tahun** | {len(df_pasca)} kejadian | {int(df_pasca['jumlah_ditangkap'].sum())} jiwa | {int(df_pasca['jumlah_tewas'].sum())} jiwa |

#### B. Uji Statistik Crosstab (Chi-Square)

**Variabel Independen (X):** Periode Ekspansi Industri

**Variabel Dependen (Y):** Tingkat Represi & Kriminalisasi

#### Case Processing Summary

| | Valid N | Valid % | Missing N | Missing % | Total N | Total % |
|---|---|---|---|---|---|---|
| {interaction_lbl} | {valid_cases_ct} | {valid_cases_ct/total_cases_ct*100:.1f}% | {missing_cases_ct} | {missing_cases_ct/total_cases_ct*100:.1f}% | {total_cases_ct} | 100.0% |

#### {interaction_lbl} Crosstabulation

{crosstab_md}

#### Chi-Square Tests

**{interaction_lbl}**

| | Value | df | Asymp. Sig. (2-sided) |
|---|---|---|---|
| Pearson Chi-Square | {chi2_default:.3f} | {dof_default} | {p_default:.3f} |
| Likelihood Ratio | {g_val:.3f} | {dof_default} | {p_g:.3f} |
| Linear-by-Linear Association | {lbl_val:.3f} | 1 | {p_corr:.3f} |
| N of Valid Cases | {valid_cases_ct} | | |

### Ringkasan Uji Hipotesis

**Result: {status_text}**

| Parameter | Nilai |
|---|---|
| P-Value | {p_default:.4f} |
| Chi-Square | {chi2_default:.3f} |
| df | {dof_default} |
| **Odds Ratio (Risk Estimate)** | **{or_default:.3f}** |

> **Interpretasi Sosial Kritis:** {interp_text}

---

### Ringkasan Eksekutif Seluruh Skenario Crosstab

Tabel di bawah ini merangkum hasil pengujian statistik (Chi-Square) untuk semua kemungkinan kombinasi antara indikator Ekspansi (X) dan Eskalasi Konflik (Y) pada panel data yang sama.

{exec_table_md}

> **Pembedahan Realitas Kemanusiaan:**
>
> {exec_narrative}

---

### 4.5 Peta Entitas Aktor: Korporasi dan Organisasi Masyarakat

Analisis entitas aktor berbasis pemrosesan teks (*string parsing*) terhadap catatan kronologi dokumentasi TanahKita memetakan keterlibatan berbagai pihak dalam sengketa agraria. Hasil ekstraksi teks mengidentifikasi entitas korporasi, lembaga pemerintah, serta organisasi masyarakat sipil yang tercatat dalam dokumentasi kasus. Grafik frekuensi di bawah menampilkan entitas korporasi dan kelompok masyarakat yang paling sering teridentifikasi dalam catatan sengketa lahan.

#### Top 10 Entitas Korporasi Paling Dominan

![Top 10 Entitas Korporasi Paling Dominan](visuals_bab4/chart_4_5a_korporasi.png)

> **Analisis Data Korporasi:** Ekstraksi teks mencatat frekuensi penyebutan entitas **{top1_corp_name}** dalam **{top1_corp_freq} catatan kasus terpisah**.

#### Top Aktor Proksi & Vigilante Terdeteksi

![Top Aktor Proksi & Vigilante Terdeteksi](visuals_bab4/chart_4_5b_vigilante.png)

> **Analisis Kritis Proksi/Vigilante:** Kemunculan kelompok sipil seperti **{top1_civ_name}** (terdeteksi hingga **{top1_civ_freq} kali**) menangkap besarnya skala orkestrasi horizontal. Korporasi seringkali menggunakan jasa pengamanan swakarsa, kelompok preman, hingga ormas vigilante sebagai "bemper proksi" untuk mengintimidasi warga lokal dan memecah belah solidaritas akar rumput.

*\\* Grafik di atas hanya menampilkan Top 10 entitas. Untuk melihat daftar lengkap dan detail seluruh aktor yang terdeteksi, silakan buka tabel data.*
'''
out_path = HERE / "chapter_4.md"
out_path.write_text(md, encoding="utf-8")
print(f"Done! 100% faithful chapter_4.md saved to {out_path}")
