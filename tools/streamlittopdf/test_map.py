import plotly.express as px
import plotly.graph_objects as go
import json
import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent.parent
with open(BASE / "data" / "processed" / "sulawesi_provinces.geojson") as f:
    geojson = json.load(f)

df = pd.DataFrame({
    'Provinsi': ['Sulawesi Tengah', 'Sulawesi Tenggara', 'Sulawesi Selatan', 'Sulawesi Utara', 'Gorontalo', 'Sulawesi Barat'],
    'Val': [55.2, 58.4, 70.1, 75.3, 72.0, 68.5]
})

fig = px.choropleth_mapbox(
    df, geojson=geojson, locations='Provinsi', featureidkey='properties.Provinsi',
    color='Val', color_continuous_scale='Reds', mapbox_style='carto-positron',
    zoom=4.2, center={"lat": -1.8, "lon": 120.5}
)
fig.update_layout(paper_bgcolor='white', margin=dict(l=0,r=0,t=0,b=0))
fig.write_image("test_map.png", width=600, height=400)
print("SUCCESS writing test_map.png")
