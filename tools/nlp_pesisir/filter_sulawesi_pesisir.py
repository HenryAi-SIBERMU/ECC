import pandas as pd
import re
import os

def is_sulawesi_and_pesisir(text):
    if not isinstance(text, str):
        return False, False
    
    text = text.lower()
    
    # 1. Klasifikasi Geografis: Hanya Sulawesi
    sulawesi_keywords = [
        r'\bsulawesi\b', r'\bsulteng\b', r'\bsultra\b', r'\bsulsel\b', r'\bsulut\b', r'\bsulbar\b', r'\bgorontalo\b',
        r'\bmorowali\b', r'\bkonawe\b', r'\bkolaka\b', r'\bkendari\b', r'\bpalu\b', r'\bposo\b', r'\bluwu\b', 
        r'\bmakassar\b', r'\bmanado\b', r'\bbitung\b', r'\bbanggai\b', r'\bwakatobi\b', r'\bmuna\b', r'\bbuton\b', r'\bbombana\b'
    ]
    is_sulawesi = any(re.search(kw, text) for kw in sulawesi_keywords)
    
    # 2. Klasifikasi Ekologi: Pesisir / Laut / Air
    pesisir_keywords = [
        r'\bair\b', r'\blaut\b', r'\bpesisir\b', r'\bnelayan\b', r'\bsungai\b', r'\bpulau\b', r'\btailing\b', 
        r'\bterumbu karang\b', r'\bmangrove\b', r'\bpantai\b', r'\bair tanah\b', r'\bperairan\b', r'\bdanau\b'
    ]
    is_pesisir = any(re.search(kw, text) for kw in pesisir_keywords)
    
    return is_sulawesi, is_pesisir

def process_dataset(filepath):
    print(f"Reading dataset: {filepath}")
    df = pd.read_csv(filepath)
    
    sulawesi_flags = []
    pesisir_flags = []
    
    for idx, row in df.iterrows():
        # Gabungkan narasi, deskripsi, dan judul
        full_text = " ".join([str(row.get('judul', '')), str(row.get('deskripsi', '')), str(row.get('narasi', ''))])
        
        sul, pesisir = is_sulawesi_and_pesisir(full_text)
        sulawesi_flags.append(sul)
        pesisir_flags.append(pesisir)
        
    df['is_sulawesi'] = sulawesi_flags
    df['is_pesisir'] = pesisir_flags
    
    # Flag khusus untuk Tab Air 3
    df['indikasi_air_sulawesi'] = df['is_sulawesi'] & df['is_pesisir']
    
    new_tot_sulawesi = df['is_sulawesi'].sum()
    new_tot_pesisir = df['is_pesisir'].sum()
    new_tot_air_sulawesi = df['indikasi_air_sulawesi'].sum()
    
    print(f"NLP Extracted Totals -> Sulawesi: {new_tot_sulawesi}, Pesisir/Air: {new_tot_pesisir}, Sulawesi + Pesisir: {new_tot_air_sulawesi}")
    
    df.to_csv(filepath, index=False)
    print(f"Data saved to: {filepath}")

if __name__ == '__main__':
    dataset_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/processed/sulawesi_konflik_agraria_tanahkita.csv'))
    process_dataset(dataset_path)
