def patch_file():
    with open('pages/1_Ekspansi_Industri.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # Part 1: Add import plotly and fix routes
    old_routes = '''MAP_ROUTES = [
    # label, src_lon, src_lat, tgt_lon, tgt_lat, hex_color, text_pos, curve_offset
    ("IMIP",         122.15, -2.82, 113.8, 22.8,  "rgb(230, 25, 25)",  "middle right", 0.15),
    ("GNI",          121.32, -1.91, 113.8, 22.8,  "rgb(255, 140, 0)",  "top center", 0.02),
    ("VDNI",         122.42, -3.83, 113.8, 22.8,  "rgb(0, 112, 220)",  "bottom left", -0.1),
    ("OSS",          122.48, -3.80, 113.8, 22.8,  "rgb(0, 190, 220)",  "bottom right", -0.15),
    ("ANTAM",        121.60, -4.18, 135.0, 35.0,  "rgb(0, 180, 80)",   "bottom center", 0.12),
    ("PT Vale",      121.34, -2.56, 135.0, 35.0,  "rgb(180, 0, 200)",  "middle left", -0.05),
]'''

    new_routes = '''import plotly.graph_objects as go

MAP_ROUTES = [
    # label, src_lon, src_lat, tgt_lon, tgt_lat, hex_color, ax, ay, curve_offset
    ("IMIP",         122.15, -2.82, 113.8, 22.8,  "rgb(230, 25, 25)",  45, -15, 0.15),
    ("GNI",          121.32, -1.91, 113.8, 22.8,  "rgb(255, 140, 0)",  0, -35, 0.02),
    ("VDNI",         122.42, -3.83, 113.8, 22.8,  "rgb(0, 112, 220)",  -45, 15, -0.1),
    ("OSS",          122.48, -3.80, 113.8, 22.8,  "rgb(0, 190, 220)",  45, 15, -0.15),
    ("ANTAM",        121.60, -4.18, 135.0, 35.0,  "rgb(0, 180, 80)",   0, 35, 0.12),
    ("PT Vale",      121.34, -2.56, 135.0, 35.0,  "rgb(180, 0, 200)",  -45, -15, -0.05),
]'''
    
    content = content.replace(old_routes, new_routes)

    # Part 2: Change loop to unpack 8 variables (now with ax, ay instead of text_pos)
    old_loop1 = 'for label, slon, slat, tlon, tlat, color, pos, offset in MAP_ROUTES:'
    new_loop1 = 'for label, slon, slat, tlon, tlat, color, ax, ay, offset in MAP_ROUTES:'
    content = content.replace(old_loop1, new_loop1)

    # Part 3: Modify the src nodes trace to use annotations instead of text
    old_src_trace = '''src_lons = [r[1] for r in MAP_ROUTES]
src_lats = [r[2] for r in MAP_ROUTES]
src_labels = [r[0] for r in MAP_ROUTES]
src_colors = [r[5] for r in MAP_ROUTES]
src_pos = [r[6] for r in MAP_ROUTES]

fig.add_trace(go.Scattergeo(
    lon = src_lons,
    lat = src_lats,
    mode = 'markers+text',
    marker = dict(size = 9, color = src_colors, symbol='circle'),
    text = src_labels,
    textposition = src_pos,
    textfont=dict(size=13, color="#111", family="Inter", weight="bold"),
    name = "Smelter Sulawesi",
    hoverinfo = 'text',
    showlegend = False
))'''

    new_src_trace = '''src_lons = [r[1] for r in MAP_ROUTES]
src_lats = [r[2] for r in MAP_ROUTES]
src_labels = [r[0] for r in MAP_ROUTES]
src_colors = [r[5] for r in MAP_ROUTES]

fig.add_trace(go.Scattergeo(
    lon = src_lons,
    lat = src_lats,
    mode = 'markers',
    marker = dict(size = 9, color = src_colors, symbol='circle'),
    name = "Smelter Sulawesi",
    hoverinfo = 'text',
    text = src_labels,
    showlegend = False
))

# Tambahkan label dengan pointer line (annotation) agar tidak pernah saling tindih
for label, slon, slat, tlon, tlat, color, ax, ay, offset in MAP_ROUTES:
    fig.add_annotation(
        x = slon,
        y = slat,
        text = f"<b>{label}</b>",
        font = dict(size=13, color="#111", family="Inter"),
        showarrow = True,
        arrowhead = 0,
        arrowwidth = 1.5,
        arrowcolor = "#666",
        ax = ax,
        ay = ay,
        xref = "x",
        yref = "y"
    )'''

    content = content.replace(old_src_trace, new_src_trace)
    
    # Part 4: Fix dataframe column map
    old_df = 'df_logistik_map = pd.DataFrame(MAP_ROUTES, columns=["Nama Smelter", "Lon Origin", "Lat Origin", "Lon Dest", "Lat Dest", "Color", "Text Pos", "Curve Offset"])'
    new_df = 'df_logistik_map = pd.DataFrame(MAP_ROUTES, columns=["Nama Smelter", "Lon Origin", "Lat Origin", "Lon Dest", "Lat Dest", "Color", "AX", "AY", "Curve Offset"])'
    content = content.replace(old_df, new_df)

    with open('pages/1_Ekspansi_Industri.py', 'w', encoding='utf-8') as f:
        f.write(content)

patch_file()
print("OK")
