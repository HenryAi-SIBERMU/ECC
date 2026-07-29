import re

with open('pages/6_Audit_D3TLH.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update load_data() return
content = content.replace(
    'return df_kes, df_ika, df_bencana, df_konflik, df_izin, df_iku, df_b3, df_pltu_op, df_gfw, df_gfw_lindung, df_gfw_driver, df_konflik_fpic, df_kpa_izin, df_pltu_captive, df_kawasan_nikel, df_faskes',
    'df_nasa = pd.read_csv(os.path.join(DATA_DIR, "gee_nasa_no2_sulawesi_monthly_raw.csv")) if os.path.exists(os.path.join(DATA_DIR, "gee_nasa_no2_sulawesi_monthly_raw.csv")) else pd.DataFrame()\n    return df_kes, df_ika, df_bencana, df_konflik, df_izin, df_iku, df_b3, df_pltu_op, df_gfw, df_gfw_lindung, df_gfw_driver, df_konflik_fpic, df_kpa_izin, df_pltu_captive, df_kawasan_nikel, df_faskes, df_nasa'
)
content = content.replace(
    'df_kes, df_ika, df_bencana, df_konflik, df_izin, df_iku, df_b3, df_pltu_op, df_gfw, df_gfw_lindung, df_gfw_driver, df_konflik_fpic, df_kpa_izin, df_pltu_captive, df_kawasan_nikel, df_faskes = load_data()',
    'df_kes, df_ika, df_bencana, df_konflik, df_izin, df_iku, df_b3, df_pltu_op, df_gfw, df_gfw_lindung, df_gfw_driver, df_konflik_fpic, df_kpa_izin, df_pltu_captive, df_kawasan_nikel, df_faskes, df_nasa = load_data()'
)

# 2. Replace skor_1 calculation in Section A Pre-calculate (lines ~161-169)
# Also there is a second place around line ~553-563. I will replace both.
old_skor1 = """kapasitas_terkini = 0
iku_terkini = 75
if not df_pltu_op.empty:
    kapasitas_terkini = df_pltu_op[(df_pltu_op['Status'].str.lower() == 'operating')]['Capacity (MW)'].sum()
if not df_iku.empty:
    df_iku_avg_pre = df_iku.groupby('Tahun')['IKU'].mean().reset_index()
    if 2024 in df_iku_avg_pre['Tahun'].values:
        iku_terkini = df_iku_avg_pre[df_iku_avg_pre['Tahun'] == 2024]['IKU'].values[0]
skor_1 = min(10.0, (kapasitas_terkini / 10000) * 5 + max(0, (80 - iku_terkini) / 30) * 5)"""

new_skor1 = """kapasitas_terkini = 0
no2_terkini = 4.0e-6
if not df_pltu_op.empty:
    kapasitas_terkini = df_pltu_op[(df_pltu_op['Status'].str.lower() == 'operating')]['Capacity (MW)'].sum()
if not df_nasa.empty:
    df_nasa_annual = df_nasa.groupby('Tahun')['Rata_Rata_NO2'].mean().reset_index()
    if not df_nasa_annual.empty:
        no2_terkini = df_nasa_annual.loc[df_nasa_annual['Tahun'].idxmax(), 'Rata_Rata_NO2']
# Normalisasi: PLTU Max 10.000 MW (skor 5), NO2 kritis pada 7.0e-6 (range 4.0e-6 ke 7.0e-6 = skor 5)
skor_1 = min(10.0, (kapasitas_terkini / 10000) * 5 + max(0, (no2_terkini - 4.0e-6) / (7.0e-6 - 4.0e-6)) * 5)"""
content = content.replace(old_skor1, new_skor1)

# Another variant of old_skor1 has a comment # Normalisasi: ...
old_skor1_var2 = """kapasitas_terkini = 0
iku_terkini = 75
if not df_pltu_op.empty:
    kapasitas_terkini = df_pltu_op[(df_pltu_op['Status'].str.lower() == 'operating')]['Capacity (MW)'].sum()
if not df_iku.empty:
    df_iku_avg_pre = df_iku.groupby('Tahun')['IKU'].mean().reset_index()
    if 2024 in df_iku_avg_pre['Tahun'].values:
        iku_terkini = df_iku_avg_pre[df_iku_avg_pre['Tahun'] == 2024]['IKU'].values[0]
# Normalisasi: PLTU Max 10.000 MW, IKU kritis pada 50 (range 80 ke 50)
skor_1 = min(10.0, (kapasitas_terkini / 10000) * 5 + max(0, (80 - iku_terkini) / 30) * 5)"""
content = content.replace(old_skor1_var2, new_skor1)

# 3. Replace the UI block for Tab 1
# From "st.markdown("<div style='font-size:0.9em; color:#B0BEC5; margin-bottom:15px;'><b>Narasi Anomali:</b> Pemerintah sering merilis angka rata-rata IKU tahunan seolah 'Masih Aman'..."
# To "st.caption("Sumber: `sulawesi_pltu_captive.csv` (gabungan captive + grid)")"

tab1_pattern = re.compile(r'(\s*st\.markdown\("<div style=\'font-size:0\.9em; color:#B0BEC5; margin-bottom:15px;\'><b>Narasi Anomali:</b> Pemerintah sering merilis.*?)(?=\s*with tab2:)', re.DOTALL)

new_tab1_content = """            st.markdown("<div style='font-size:0.9em; color:#B0BEC5; margin-bottom:15px;'><b>Narasi Anomali:</b> Pemerintah sebelumnya mengklaim IKU 'Masih Aman'. Namun pantauan independen Satelit TROPOMI NASA mengungkap realitas lain: konsentrasi gas beracun NO2 meledak meroket sejajar dengan ekspansi PLTU captive. <b>Threshold Kritis NASA: NO2 > 6.0e-6 mol/m²</b>.</div>", unsafe_allow_html=True)
            
            if not df_pltu_op.empty and not df_nasa.empty:
                years = list(range(2010, 2025))
                prov_map = {
                    'Central Sulawesi': 'Sulawesi Tengah', 'South East Sulawesi': 'Sulawesi Tenggara',
                    'South Sulawesi': 'Sulawesi Selatan', 'North Sulawesi': 'Sulawesi Utara',
                    'West Sulawesi': 'Sulawesi Barat', 'Gorontalo': 'Gorontalo'
                }
                
                df_pltu_op_tab = df_pltu_op.copy()
                df_pltu_op_tab['Provinsi'] = df_pltu_op_tab['Subnational unit (province, state)'].replace(prov_map)
                df_pltu_op_tab = df_pltu_op_tab[(df_pltu_op_tab['Status'].str.lower() == 'operating') & df_pltu_op_tab['Start year'].notna()]
                
                grid_pltu = pd.DataFrame([
                    {'Provinsi': 'Gorontalo', 'Capacity (MW)': 100, 'Start year': 2010},
                    {'Provinsi': 'Sulawesi Utara', 'Capacity (MW)': 220, 'Start year': 2010},
                    {'Provinsi': 'Sulawesi Selatan', 'Capacity (MW)': 920, 'Start year': 2010},
                    {'Provinsi': 'Sulawesi Tenggara', 'Capacity (MW)': 100, 'Start year': 2010}
                ])
                df_pltu_op_tab = pd.concat([df_pltu_op_tab, grid_pltu], ignore_index=True)
                
                panel_data_pltu = []
                for y in years:
                    for prov in prov_map.values():
                        cap = df_pltu_op_tab[(df_pltu_op_tab['Provinsi'] == prov) & (df_pltu_op_tab['Start year'] <= y)]['Capacity (MW)'].sum()
                        panel_data_pltu.append({'Tahun': y, 'Provinsi': prov, 'Kapasitas_PLTU_MW': cap})
                df_pltu_trend = pd.DataFrame(panel_data_pltu)
                
                df_nasa_annual = df_nasa.groupby('Tahun')['Rata_Rata_NO2'].mean().reset_index()
                df_nasa_annual.rename(columns={'Tahun': 'year', 'Rata_Rata_NO2': 'median'}, inplace=True)
                
                kapasitas_grafik = df_pltu_trend[df_pltu_trend['Tahun'] == 2024]['Kapasitas_PLTU_MW'].sum()
                no2_grafik = df_nasa_annual.loc[df_nasa_annual['year'].idxmax(), 'median'] if not df_nasa_annual.empty else 0.0
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Kapasitas PLTU Aktif", f"{kapasitas_grafik:,.0f} MW", "Max threshold: 10.000 MW")
                col2.metric("Rata-rata Polusi NO2 NASA", f"{no2_grafik:.2e}", "Kritis jika naik melebihi 6.0e-6", delta_color="inverse")
                col3.metric("Skor Ancaman Udara", f"{skor_1:.1f} / 10", "STATUS: KRITIS", delta_color="inverse")
                st.markdown("<hr style='border:1px solid #444; margin-top:5px; margin-bottom:15px;'>", unsafe_allow_html=True)
                
                pltu_colors = {
                    'Gorontalo': '#757575',
                    'Sulawesi Utara': '#8D6E63',
                    'Sulawesi Selatan': '#FBC02D',
                    'Sulawesi Tenggara': '#F57C00',
                    'Sulawesi Tengah': '#D32F2F'
                }
                
                pltu_config = []
                for prov, color in pltu_colors.items():
                    d_trend = df_pltu_trend[df_pltu_trend['Provinsi'] == prov]
                    if not d_trend.empty:
                        max_mw = d_trend['Kapasitas_PLTU_MW'].max()
                        label = f"{prov} — PLTU max {max_mw:,.0f} MW"
                        pltu_config.append({'prov': prov, 'color': color, 'label': label})

                def get_no2_color(val):
                    if val > 6.0e-6: return '#D32F2F'
                    elif val > 5.0e-6: return '#FBC02D'
                    else: return '#4CAF50'
                
                no2_annual_colors = [get_no2_color(v) for v in df_nasa_annual['median']]

                fig_nasa_combined = make_subplots(specs=[[{"secondary_y": True}]])
                
                for cfg in pltu_config:
                    d_trend = df_pltu_trend[df_pltu_trend['Provinsi'] == cfg['prov']]
                    if not d_trend.empty:
                        fig_nasa_combined.add_trace(
                            go.Scatter(
                                x=d_trend['Tahun'], y=d_trend['Kapasitas_PLTU_MW'], name=cfg['label'], 
                                mode='lines', stackgroup='one', line=dict(width=1, color=cfg['color']),
                                fillcolor=cfg['color'], hoveron='points+fills',
                                hovertemplate=cfg['prov'] + ': %{y:,.0f} MW<extra></extra>', showlegend=True
                            ),
                            secondary_y=False
                        )

                for i in range(len(df_nasa_annual)-1):
                    fig_nasa_combined.add_trace(
                        go.Scatter(
                            x=df_nasa_annual['year'].iloc[i:i+2],
                            y=df_nasa_annual['median'].iloc[i:i+2],
                            mode='lines',
                            line=dict(color=no2_annual_colors[i+1], width=4),
                            showlegend=False, hoverinfo='skip'
                        ),
                        secondary_y=True
                    )
                
                fig_nasa_combined.add_trace(
                    go.Scatter(
                        x=df_nasa_annual['year'], y=df_nasa_annual['median'], name="Rata-rata NO2 Tahunan", 
                        mode='markers', marker=dict(color=no2_annual_colors, size=10, line=dict(width=1, color='#FFFFFF')), 
                        hovertemplate='Tahun %{x}<br>NO2: %{y:.2e}<extra></extra>', showlegend=False
                    ),
                    secondary_y=True
                )

                fig_nasa_combined.add_trace(go.Scatter(x=[None], y=[None], mode='markers', marker=dict(color='#D32F2F', size=10), name='Polusi NO2 Tinggi (> 6.0e-6)'), secondary_y=True)
                fig_nasa_combined.add_trace(go.Scatter(x=[None], y=[None], mode='markers', marker=dict(color='#FBC02D', size=10), name='Polusi NO2 Sedang (5.0-6.0e-6)'), secondary_y=True)
                fig_nasa_combined.add_trace(go.Scatter(x=[None], y=[None], mode='markers', marker=dict(color='#4CAF50', size=10), name='Polusi NO2 Rendah (< 5.0e-6)'), secondary_y=True)

                fig_nasa_combined.update_layout(
                    title=dict(text="Semua PLTU Batubara vs Polusi NO2 (Data Satelit NASA)", font=dict(color='#ECEFF1', size=16)),
                    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#ECEFF1', family='Arial, sans-serif'),
                    legend=dict(orientation="v", yanchor="top", y=0.98, xanchor="left", x=0.02, bgcolor='rgba(30,30,30,0.8)', bordercolor='#555', borderwidth=1, font=dict(size=11), traceorder='reversed'),
                    xaxis=dict(title="", tickmode='linear', dtick=2, tickformat='d', showgrid=True, gridcolor='#2b3240', gridwidth=1, griddash='dash', showline=True, linewidth=1, linecolor='#555555', rangeslider=dict(visible=False)),
                    yaxis=dict(title="Kapasitas PLTU Kumulatif (MW)", showgrid=True, gridcolor='#2b3240', gridwidth=1, griddash='dash', side='left', tickformat=',.1s', dtick=500, ticksuffix=' MW'),
                    yaxis2=dict(title="Konsentrasi NO2 (mol/m²)", showgrid=False, overlaying='y', side='right'),
                    hovermode="x unified", hoverlabel=dict(bgcolor="rgba(0, 0, 0, 0.8)", font_size=13, font_family="Arial", font_color="#FFFFFF"),
                    margin=dict(l=0, r=0, t=40, b=0)
                )

                st.plotly_chart(fig_nasa_combined, use_container_width=True, config={'displayModeBar': False})
                
                with st.expander("Lihat Data Mentah: Kapasitas PLTU per Provinsi", expanded=False):
                    df_pivot_pltu = df_pltu_trend.pivot(index='Tahun', columns='Provinsi', values='Kapasitas_PLTU_MW').reset_index()
                    st.dataframe(df_pivot_pltu, use_container_width=True, hide_index=True)
                    st.caption("Sumber: `sulawesi_pltu_captive.csv` (gabungan captive + grid)")
"""

content = re.sub(tab1_pattern, new_tab1_content, content)

with open('pages/6_Audit_D3TLH.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Done updating 6_Audit_D3TLH.py")
