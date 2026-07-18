import sys

with open('pages/2_Kualitas_Lingkungan.py', 'r', encoding='utf-8') as f:
    text = f.read()

start_str = "import plotly.graph_objects as go"
end_str = "fig_2_2_combined.update_yaxes("

start_idx = text.find(start_str)

# Find the LAST update_yaxes block
last_update_idx = text.rfind(end_str, start_idx, start_idx + 3000)

if start_idx == -1 or last_update_idx == -1:
    print('Could not find block')
    sys.exit(1)

# Find the end of the last update_yaxes function call
end_idx = text.find(")", last_update_idx) + 1

new_code = '''import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import numpy as np

# Warna dan urutan (dari bawah ke atas di stacked area)
pltu_config = [
    {'prov': 'Gorontalo', 'color': '#757575', 'label': 'Gorontalo — PLTU max 100 MW'},
    {'prov': 'Sulawesi Utara', 'color': '#8D6E63', 'label': 'Sulawesi Utara — PLTU max 220 MW'},
    {'prov': 'Sulawesi Selatan', 'color': '#FBC02D', 'label': 'Sulawesi Selatan — PLTU max 1,520 MW'},
    {'prov': 'Sulawesi Tenggara', 'color': '#F57C00', 'label': 'Sulawesi Tenggara — PLTU max 2,000 MW'},
    {'prov': 'Sulawesi Tengah', 'color': '#D32F2F', 'label': 'Sulawesi Tengah — PLTU max 7,325 MW'}
]

fig_2_2_combined = make_subplots(specs=[[{"secondary_y": True}]])

# 1. Tambahkan Stacked Area per Provinsi untuk PLTU (Left Y-axis)
for cfg in pltu_config:
    d = df_pltu_trend[df_pltu_trend['Provinsi'] == cfg['prov']]
    if not d.empty:
        fig_2_2_combined.add_trace(
            go.Scatter(
                x=d['Tahun'], 
                y=d['Kapasitas_PLTU_MW'], 
                name=cfg['label'], 
                mode='lines', 
                stackgroup='one',
                line=dict(width=1, color=cfg['color']),
                fillcolor=cfg['color'],
                hoveron='points+fills',
                hovertemplate=cfg['prov'] + ': %{y:,.0f} MW<extra></extra>',
                showlegend=True
            ),
            secondary_y=False
        )

# 2. Definisikan warna untuk marker IKU
def get_iku_color(val):
    if val < 85: return '#D32F2F' # Merah (buruk)
    elif val < 90: return '#FBC02D' # Kuning (tertekan)
    else: return '#4CAF50' # Hijau (baik)

iku_colors = [get_iku_color(v) for v in df_iku_avg['IKU']]

# Tambahkan Garis IKU (Sebagai garis solid dengan gradient/warna-warni menggunakan trik multi-segment, 
# atau garis abu-abu dengan titik warna)
for i in range(len(df_iku_avg)-1):
    fig_2_2_combined.add_trace(
        go.Scatter(
            x=df_iku_avg['Tahun'].iloc[i:i+2],
            y=df_iku_avg['IKU'].iloc[i:i+2],
            mode='lines',
            line=dict(color=iku_colors[i+1], width=4),
            showlegend=False,
            hoverinfo='skip'
        ),
        secondary_y=True
    )

# Tambahkan Marker IKU Rata-rata di atas garis
fig_2_2_combined.add_trace(
    go.Scatter(
        x=df_iku_avg['Tahun'], 
        y=df_iku_avg['IKU'], 
        name="Rata-rata IKU Sulawesi (warna = kondisi IKU)", 
        mode='markers', 
        marker=dict(color=iku_colors, size=10, line=dict(width=1, color='#FFFFFF')), 
        hovertemplate='Tahun %{x}<br>IKU: %{y:.1f}<extra></extra>',
        showlegend=False
    ),
    secondary_y=True
)

# Dummy traces untuk legend IKU
fig_2_2_combined.add_trace(go.Scatter(x=[None], y=[None], mode='markers', marker=dict(color='#4CAF50', size=10), name='IKU relatif baik (hijau)', secondary_y=True))
fig_2_2_combined.add_trace(go.Scatter(x=[None], y=[None], mode='markers', marker=dict(color='#FBC02D', size=10), name='IKU tertekan (kuning)', secondary_y=True))
fig_2_2_combined.add_trace(go.Scatter(x=[None], y=[None], mode='markers', marker=dict(color='#D32F2F', size=10), name='IKU buruk/kritis (merah)', secondary_y=True))
fig_2_2_combined.add_trace(go.Scatter(x=[None], y=[None], mode='lines', line=dict(color='#FFFFFF', width=2), name='Rata-rata IKU Sulawesi (warna = kondisi IKU)', secondary_y=True))


# Update layout
fig_2_2_combined.update_layout(
    title=dict(text="Semua PLTU Batubara vs Penurunan Kualitas Udara (2010-2024)", font=dict(color='#ECEFF1', size=22, family="Arial")),
    plot_bgcolor='#11151c',
    paper_bgcolor='#11151c',
    font=dict(color='#ECEFF1', family='Arial, sans-serif'),
    legend=dict(
        orientation="v", 
        yanchor="top", 
        y=0.95, 
        xanchor="left", 
        x=0.05,
        bgcolor='rgba(17, 21, 28, 0.7)',
        bordercolor='#555',
        borderwidth=1,
        font=dict(size=11),
        traceorder='reversed'
    ),
    xaxis=dict(
        title="",
        tickmode='linear',
        dtick=2,
        tickformat='d',
        showgrid=True,
        gridcolor='#2b3240',
        gridwidth=1,
        griddash='dash',
        showline=True,
        linewidth=1,
        linecolor='#555555',
        rangeslider=dict(visible=False), # Dimatikan agar persis spt gambar
    ),
    hovermode="x unified",
    hoverlabel=dict(
        bgcolor="rgba(0, 0, 0, 0.8)",
        font_size=13,
        font_family="Arial",
        font_color="#FFFFFF"
    ),
    height=550,
    margin=dict(l=60, r=60, t=60, b=40)
)

# Update Y-axes
fig_2_2_combined.update_yaxes(
    title_text="Kapasitas PLTU Kumulatif (MW)", 
    secondary_y=False,
    color='#ECEFF1', 
    gridcolor='#2b3240',
    gridwidth=1,
    griddash='dash',
    tickformat=',.1s',
    dtick=500,
    ticksuffix=' MW'
)
fig_2_2_combined.update_yaxes(
    title_text="Indeks Kualitas Udara (IKU)", 
    secondary_y=True,
    color='#ECEFF1', 
    showgrid=False,
    dtick=2
)
'''

text = text[:start_idx] + new_code + text[end_idx:]

with open('pages/2_Kualitas_Lingkungan.py', 'w', encoding='utf-8') as f:
    f.write(text)

print('Success')
