import pandas as pd
df = pd.read_excel('data/ECC_Lampiran_Teknis_2_dataset mining.xlsx')
with open('excel_output.txt', 'w', encoding='utf-8') as f:
    for i, row in df.iterrows():
        f.write(str(dict(row)) + '\n')
