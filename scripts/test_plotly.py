import plotly.graph_objects as go

def build_map():
    fig = go.Figure()

    MAP_ROUTES = [
        # label, src_lon, src_lat, tgt_lon, tgt_lat, hex_color
        ("IMIP - Morowali",      122.15, -2.82, 113.8, 22.8,  "rgb(230, 25,  25)"),
        ("GNI - Morowali Utara", 121.32, -1.91, 113.8, 22.8,  "rgb(255, 140, 0)"),
        ("VDNI/OSS - Konawe",    122.42, -3.83, 113.8, 22.8,  "rgb(0,  112, 220)"),
        ("ANTAM - Kolaka",       121.60, -4.18, 135.0, 35.0,  "rgb(0,  180, 80)"),
        ("PT Vale - Sorowako",   121.34, -2.56, 135.0, 35.0,  "rgb(180, 0,  200)"),
    ]

    for label, slon, slat, tlon, tlat, color in MAP_ROUTES:
        # We can add a slight curve by adding a midpoint, but straight lines are fine
        fig.add_trace(go.Scattergeo(
            lon = [slon, tlon],
            lat = [slat, tlat],
            mode = 'lines+markers',
            line = dict(width = 3, color = color),
            marker = dict(size = [8, 0], color = color), # Only marker on source
            name = label.split('-')[0].strip(),
            text = [label, ""],
            hoverinfo = 'text'
        ))

    # Add destinations
    fig.add_trace(go.Scattergeo(
        lon = [113.8, 135.0],
        lat = [22.8, 35.0],
        mode = 'markers+text',
        marker = dict(size = 12, color = 'rgb(50,50,50)', symbol='circle'),
        text = ["China (Pasar Utama)", "Jepang/Korea"],
        textposition=["top left", "top center"],
        textfont=dict(size=13, color="black"),
        name = "Tujuan Ekspor",
        hoverinfo='text'
    ))

    fig.update_layout(
        geo = dict(
            projection_type = "mercator",
            showland = True,
            landcolor = "rgb(240, 240, 240)",
            countrycolor = "rgb(204, 204, 204)",
            showocean = True,
            oceancolor = "rgb(220, 230, 240)",
            showcountries=True,
            center = dict(lon=122, lat=12),
            lataxis = dict(range=[-8, 45]),
            lonaxis = dict(range=[100, 145])
        ),
        margin = dict(l=0, r=0, t=10, b=0),
        legend = dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5, font=dict(size=12))
    )
    return fig

print('PLOTLY SCRIPT OK')
