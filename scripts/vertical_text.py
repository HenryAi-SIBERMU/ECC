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
    
    # 2. Letakkan teks tepat di atas garis dengan format VERTIKAL (Rotasi 90 derajat manual)
    if label == "VDNI":
        t_idx = 8
    elif label == "GNI":
        t_idx = 14
    elif label == "IMIP":
        t_idx = 18
    elif label == "PT Vale":
        t_idx = 22
    elif label == "OSS":
        t_idx = 26
    elif label == "ANTAM":
        t_idx = 30
    else:
        t_idx = 15
        
    vertical_text = "<br>".join(list(label.replace(" ", " ")))
    
    fig.add_trace(go.Scattergeo(
        lon = [curve_lons[t_idx]],
        lat = [curve_lats[t_idx]],
        mode = 'text',
        text = [f"<b>{vertical_text}</b>"],
        textposition = "middle center", # Center perfectly on the line
        textfont = dict(size=11, color="#111", family="Inter"),
        showlegend = False,
        hoverinfo='skip'
    ))

'''
    
    content = content[:start_idx] + new_trace_code + content[end_idx:]
    
    with codecs.open('pages/1_Ekspansi_Industri.py', 'w', 'utf-8') as f:
        f.write(content)

fix_map_text_vertical()
print("OK")
