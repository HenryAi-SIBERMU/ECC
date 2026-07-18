import sys

file_path = "pages/2_Kualitas_Lingkungan.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

target = "st.plotly_chart(fig_2_2_combined, use_container_width=True)"

addition = '''# Colorbar untuk IKU
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
)

st.plotly_chart(fig_2_2_combined, use_container_width=True)'''

if target in content:
    content = content.replace(target, addition)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Injected original IKU trace before plotly_chart.")
else:
    print("Could not find target to inject IKU trace.")
