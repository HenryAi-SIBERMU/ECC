import sys
import re

file_path = "pages/2_Kualitas_Lingkungan.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old_trace = '''# "?"? Colorbar untuk IKU (gradient merah+'kuning+'hijau) "?"?
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
              ),'''

new_trace = '''# Colorbar untuk IKU (gradient merah-kuning-hijau)
  fig_2_2_combined.add_trace(
      go.Scatter(
          x=[None], y=[None],
          mode='markers',
          marker=dict(
              color=[85],
              colorscale=[
                  [0.0, '#FF1744'], # 80 - Merah (Buruk)
                  [0.5, '#FFD600'], # 87.5 - Kuning (Sedang)
                  [1.0, '#00E676']  # 95 - Hijau (Baik)
              ],
              cmin=80, cmax=95,
              colorbar=dict(
                  title=dict(text="IKU<br>merah = buruk", font=dict(color='#ECEFF1', size=12), side="right"),
                  tickvals=[80, 85, 90, 95],
                  ticktext=['80', '85', '90', '95'],
                  len=0.5,
                  y=0.5,
                  x=1.02,
                  tickfont=dict(color='#ECEFF1'),
                  bgcolor='rgba(0,0,0,0)',
                  borderwidth=0,
              ),'''

# Let's use regex instead because of potential invisible chars like "?
pattern = r"# .*?Colorbar untuk IKU.*?borderwidth=0,\s*\),"
replacement = r'''# Colorbar untuk IKU (gradient halus merah-kuning-hijau)
  fig_2_2_combined.add_trace(
      go.Scatter(
          x=[None], y=[None],
          mode='markers',
          marker=dict(
              color=[85],
              colorscale=[
                  [0.0, '#FF1744'],
                  [0.5, '#FFD600'],
                  [1.0, '#00E676']
              ],
              cmin=80, cmax=95,
              colorbar=dict(
                  title=dict(text="IKU<br>merah = buruk", font=dict(color='#ECEFF1', size=12), side="right"),
                  tickvals=[80, 85, 90, 95],
                  ticktext=['80', '85', '90', '95'],
                  len=0.5,
                  y=0.5,
                  x=1.02,
                  tickfont=dict(color='#ECEFF1'),
                  bgcolor='rgba(0,0,0,0)',
                  borderwidth=0,
              ),'''

new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(new_content)
print("Trace updated.")