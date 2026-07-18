import sys

file_path = "pages/2_Kualitas_Lingkungan.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

target = '''  fig_2_2_combined.update_yaxes(
      title_text="Indeks Kualitas Udara (IKU)", 
      secondary_y=True,
      color='#FF6B6B', 
      gridcolor='#37474F',
      showgrid=False,
      range=[80, 96]
  )'''

# We want the original stepped discrete color scale, but with the label matching Image 3 (since they originally asked for Image 3 label format).
# But wait, they screamed "KEMBALIKAN GA TOLOL KAYAK SEBELUMNYA" which means revert it to exactly what it was in Image 2!
# I will use the exact Image 2 code!
addition = '''

  # Colorbar untuk IKU (gradient merah-kuning-hijau)
  fig_2_2_combined.add_trace(
      go.Scatter(
          x=[None], y=[None],
          mode='markers',
          marker=dict(
              color=[85],
              colorscale=[[0, '#FF1744'], [0.33, '#FF1744'], [0.33, '#FFD600'], [0.67, '#FFD600'], [0.67, '#00E676'], [1, '#00E676']],
              cmin=80, cmax=95,
              colorbar=dict(
                  title=dict(text="IKU", font=dict(color='#ECEFF1', size=12)),
                  tickvals=[80, 85, 90, 95],
                  ticktext=['80<br>merah = buruk', '85', '90', '95'],
                  len=0.5,
                  y=0.5,
                  x=1.02,
                  tickfont=dict(color='#ECEFF1'),
                  bgcolor='rgba(0,0,0,0)',
                  borderwidth=0,
              ),
          ),
          showlegend=False,
          hoverinfo='none'
      ),
      secondary_y=False
  )'''

if target in content:
    content = content.replace(target, target + addition)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Injected original IKU trace.")
else:
    print("Could not find target to inject IKU trace.")