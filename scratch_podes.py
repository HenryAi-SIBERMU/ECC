import pandas as pd

try:
    df = pd.read_excel(r'C:\Users\yooma\OneDrive\Desktop\duniahub\client\8.1 Celios4-EBTsmallstack\refrensi\Data\Rawdata\Energi Terbarukan(AutoRecovered).xlsx', nrows=30)
    with open('scratch.txt', 'w', encoding='utf-8') as f:
        f.write(df.to_markdown())
except Exception as e:
    with open('scratch.txt', 'w', encoding='utf-8') as f:
        f.write(str(e))
