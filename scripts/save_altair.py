import pandas as pd
import altair as alt
import os

df_ngo_cr6 = pd.read_csv("data/processed/ika_ngo_cr6_gabungan.csv")
bar_chart = alt.Chart(df_ngo_cr6).mark_bar().encode(
    x=alt.X('Titik Sampling:N', sort=None, title='Titik Sampling', axis=alt.Axis(labelAngle=0)),
    y=alt.Y('Konsentrasi Cr6+ (mg/L):Q', title='Konsentrasi (mg/L)'),
    color=alt.Color('Konsentrasi Cr6+ (mg/L):Q', scale=alt.Scale(range=["#ffebee", "#b71c1c"]), legend=None)
).properties(
    title=alt.TitleParams(text="Kadar Kromium Heksavalen (Cr6+) di Lingkar Tambang vs Baku Mutu", color='#ECEFF1', anchor='start'),
    height=500, width=800
)
text_labels = bar_chart.mark_text(align='center', baseline='bottom', dy=-5, color='white').encode(text=alt.Text('Konsentrasi Cr6+ (mg/L):Q', format='.3f'))
rule_biota = alt.Chart(pd.DataFrame({'y': [0.005]})).mark_rule(strokeDash=[4, 4], color='red').encode(y='y:Q')
text_biota = alt.Chart(pd.DataFrame({'y': [0.005], 'text': ['Batas Aman Biota Laut (0.005 mg/L)']})).mark_text(align='left', baseline='bottom', dy=-5, dx=5, color='red').encode(y='y:Q', text='text:N')
rule_budidaya = alt.Chart(pd.DataFrame({'y': [0.050]})).mark_rule(strokeDash=[4, 4], color='orange').encode(y='y:Q')
text_budidaya = alt.Chart(pd.DataFrame({'y': [0.050], 'text': ['Batas Aman Budidaya (0.050 mg/L)']})).mark_text(align='left', baseline='bottom', dy=-5, dx=5, color='orange').encode(y='y:Q', text='text:N')
final_chart = (bar_chart + text_labels + rule_biota + text_biota + rule_budidaya + text_budidaya).configure(background='rgba(0,0,0,0)').configure_axis(gridColor='rgba(255,255,255,0.1)', labelColor='#B0BEC5', titleColor='#B0BEC5')

try:
    final_chart.save("tools/streamlittopdf/visuals_bab3/chart_3_6_ngo.png")
    print("PNG successfully created.")
except Exception as e:
    print(f"Failed to generate PNG: {e}")
