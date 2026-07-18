import codecs

def fix_map_text_vertical():
    with codecs.open('pages/1_Ekspansi_Industri.py', 'r', 'utf-8') as f:
        content = f.read()

    start_marker = "# Trace Garis Melengkung (Bezier) dan Label di atas garis"
    start_idx = content.find(start_marker)
    
    end_marker = "# Trace Titik Smelter Asli (Tanpa Teks)"
    end_idx = content.find(end_marker)
    
    if start_idx == -1 or end_idx == -1:
        print("Marker tidak ditemukan!")
        return
        
    new_trace_code = '''# Trace Garis Melengkung (Bezier) dan Label di atas garis
for label, slon, slat, tlon, tlat, color, offset in MAP_ROUTES:
    curve_lons, curve_lats = get_curve(slon, slat, tlon, tlat, offset)
    
    # 1. Gambar Garis
    fig.add_trace(go.Scattergeo(
        lon = curve_lons,
        lat = curve_lats,
        mode = 'lines',
        line = dict(width = 3.5, color = color),
        name = label,
        hoverinfo = 'skip',
        showlegend = True
    ))
    
    # 2. Bikin Teks Vertikal (Stacking ke bawah) agar seolah diputar 90 derajat
    vertical_label = "<br>".join([char for char in label if char != " "])
    
    # Letakkan teks dengan staggering ekstrem
    if label == "VDNI":
        t_idx = 10
    elif label == "GNI":
        t_idx = 16
    elif label == "IMIP":
        t_idx = 20
    elif label == "PT Vale":
        t_idx = 24
    elif label == "OSS":
        t_idx = 28
    elif label == "ANTAM":
        t_idx = 32
    else:
        t_idx = 15
        
    # Karena teksnya vertikal, kita taruh pas di tengah garis (middle center)
    fig.add_trace(go.Scattergeo(
        lon = [curve_lons[t_idx]],
        lat = [curve_lats[t_idx]],
        mode = 'text',
        text = [f"<b>{vertical_label}</b>"],
        textposition = "middle center",
        textfont = dict(size=13, color="#111", family="Inter"),
        showlegend = False,
        hoverinfo='skip'
    ))

'''
    
    content = content[:start_idx] + new_trace_code + content[end_idx:]
    
    with codecs.open('pages/1_Ekspansi_Industri.py', 'w', 'utf-8') as f:
        f.write(content)

fix_map_text_vertical()
print("OK")
