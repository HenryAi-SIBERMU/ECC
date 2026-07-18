import math

def patch_file():
    with open('pages/1_Ekspansi_Industri.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # Part 1: Replace MAP_ROUTES and drawing logic
    old_routes_logic = '''MAP_ROUTES = [
    # label, src_lon, src_lat, tgt_lon, tgt_lat, hex_color, text_pos
    ("IMIP",         122.15, -2.82, 113.8, 22.8,  "rgb(230, 25, 25)",  "top right"),
    ("GNI",          121.32, -1.91, 113.8, 22.8,  "rgb(255, 140, 0)",  "top left"),
    ("VDNI/OSS",     122.42, -3.83, 113.8, 22.8,  "rgb(0, 112, 220)",  "middle right"),
    ("ANTAM",        121.60, -4.18, 135.0, 35.0,  "rgb(0, 180, 80)",   "bottom right"),
    ("PT Vale",      121.34, -2.56, 135.0, 35.0,  "rgb(180, 0, 200)",  "bottom left"),
]

fig = go.Figure()

# Tambahkan trace untuk setiap rute smelter
for label, slon, slat, tlon, tlat, color, pos in MAP_ROUTES:
    fig.add_trace(go.Scattergeo(
        lon = [slon, tlon],
        lat = [slat, tlat],
        mode = 'lines',
        line = dict(width = 3.5, color = color),
        name = label,
        hoverinfo = 'skip',
        showlegend = True
    ))'''

    new_routes_logic = '''MAP_ROUTES = [
    # label, src_lon, src_lat, tgt_lon, tgt_lat, hex_color, text_pos, curve_offset
    ("IMIP",         122.15, -2.82, 113.8, 22.8,  "rgb(230, 25, 25)",  "top right", 0.15),
    ("GNI",          121.32, -1.91, 113.8, 22.8,  "rgb(255, 140, 0)",  "top left", 0.02),
    ("VDNI/OSS",     122.42, -3.83, 113.8, 22.8,  "rgb(0, 112, 220)",  "middle right", -0.1),
    ("ANTAM",        121.60, -4.18, 135.0, 35.0,  "rgb(0, 180, 80)",   "bottom right", 0.12),
    ("PT Vale",      121.34, -2.56, 135.0, 35.0,  "rgb(180, 0, 200)",  "bottom left", -0.05),
]

fig = go.Figure()

import math
def get_curve(slon, slat, tlon, tlat, offset):
    mid_lon = (slon + tlon) / 2
    mid_lat = (slat + tlat) / 2
    angle = math.atan2(tlat - slat, tlon - slon)
    perp_angle = angle + math.pi/2
    dist = math.sqrt((tlat - slat)**2 + (tlon - slon)**2)
    c_lon = mid_lon + math.cos(perp_angle) * dist * offset
    c_lat = mid_lat + math.sin(perp_angle) * dist * offset
    lons, lats = [], []
    for i in range(30):
        t = i / 29.0
        lon = (1-t)**2 * slon + 2*(1-t)*t * c_lon + t**2 * tlon
        lat = (1-t)**2 * slat + 2*(1-t)*t * c_lat + t**2 * tlat
        lons.append(lon)
        lats.append(lat)
    return lons, lats

# Tambahkan trace untuk setiap rute smelter
for label, slon, slat, tlon, tlat, color, pos, offset in MAP_ROUTES:
    curve_lons, curve_lats = get_curve(slon, slat, tlon, tlat, offset)
    fig.add_trace(go.Scattergeo(
        lon = curve_lons,
        lat = curve_lats,
        mode = 'lines',
        line = dict(width = 3.5, color = color),
        name = label,
        hoverinfo = 'skip',
        showlegend = True
    ))'''

    content = content.replace(old_routes_logic, new_routes_logic)

    # Part 2: Replace title
    old_title = '<h4 style="margin-top: 0; color: #D32F2F; font-size: 1.1rem; font-weight: 600;">Analisis Kritis: Ketergantungan Struktural Rantai Pasok</h4>'
    new_title = '<h4 style="margin-top: 0; color: #D32F2F; font-size: 1.1rem; font-weight: 600;">Ketergantungan Struktural Rantai Pasok</h4>'
    
    content = content.replace(old_title, new_title)

    with open('pages/1_Ekspansi_Industri.py', 'w', encoding='utf-8') as f:
        f.write(content)

patch_file()
print("OK")
