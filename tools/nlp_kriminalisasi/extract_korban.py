import pandas as pd
import re
import os

def word_to_num(word):
    word = word.lower().strip()
    num_map = {
        'satu': 1, 'seorang': 1, 'dua': 2, 'tiga': 3, 'empat': 4, 'lima': 5,
        'enam': 6, 'tujuh': 7, 'delapan': 8, 'sembilan': 9, 'sepuluh': 10,
        'sebelas': 11, 'belasan': 15, 'puluhan': 20, 'ratusan': 100, 'ribuan': 1000
    }
    if word.isdigit():
        return int(word)
    return num_map.get(word, 0)

def extract_victims(text):
    if not isinstance(text, str):
        return 0, 0, 0
    
    text = text.lower()
    
    # Regex patterns
    # Matches: "2 orang tewas", "tewas 3 warga", "puluhan tewas", "seorang meninggal"
    num_pattern = r'(\d+|satu|seorang|dua|tiga|empat|lima|enam|tujuh|delapan|sembilan|sepuluh|sebelas|belasan|puluhan|ratusan|ribuan)'
    
    tewas_keywords = r'(tewas|meninggal|gugur|ditembak mati|dibunuh)'
    luka_keywords = r'(luka|terluka|kritis|dianiaya|dipukul|babak belur)'
    tangkap_keywords = r'(ditangkap|ditahan|dikriminalisasi|dipenjara|diperiksa|tersangka)'
    
    # Search for patterns where number is before or after the keyword
    # e.g., 5 orang warga tewas
    tewas_matches = re.findall(rf'{num_pattern}(?:\s+\w+){{0,3}}\s+{tewas_keywords}', text) + \
                    re.findall(rf'{tewas_keywords}(?:\s+\w+){{0,3}}\s+{num_pattern}', text)
                    
    luka_matches = re.findall(rf'{num_pattern}(?:\s+\w+){{0,3}}\s+{luka_keywords}', text) + \
                   re.findall(rf'{luka_keywords}(?:\s+\w+){{0,3}}\s+{num_pattern}', text)
                   
    tangkap_matches = re.findall(rf'{num_pattern}(?:\s+\w+){{0,3}}\s+{tangkap_keywords}', text) + \
                      re.findall(rf'{tangkap_keywords}(?:\s+\w+){{0,3}}\s+{num_pattern}', text)
                      
    def get_max(matches, is_tewas_luka=False):
        if not matches: return 0
        nums = []
        for match in matches:
            # match is a tuple like ('2', 'tewas') or ('tewas', '2')
            for item in match:
                val = word_to_num(item)
                if val > 0:
                    # Cegah tahun terdeteksi sebagai korban (misal: "sejak 1998, tewas...")
                    if 1900 <= val <= 2099:
                        continue
                    nums.append(val)
        return max(nums) if nums else 0

    return get_max(tangkap_matches), get_max(luka_matches, True), get_max(tewas_matches, True)

def process_dataset(filepath):
    print(f"Reading dataset: {filepath}")
    df = pd.read_csv(filepath)
    
    old_tangkap = pd.to_numeric(df['jumlah_ditangkap'], errors='coerce').fillna(0).sum()
    old_luka = pd.to_numeric(df['jumlah_luka'], errors='coerce').fillna(0).sum()
    old_tewas = pd.to_numeric(df['jumlah_tewas'], errors='coerce').fillna(0).sum()
    
    print(f"Original Totals -> Ditangkap: {old_tangkap}, Luka: {old_luka}, Tewas: {old_tewas}")
    
    new_tangkap_list = []
    new_luka_list = []
    new_tewas_list = []
    
    for idx, row in df.iterrows():
        # Gabungkan narasi, deskripsi, dan judul
        full_text = " ".join([str(row.get('judul', '')), str(row.get('deskripsi', '')), str(row.get('narasi', ''))])
        
        nlp_tangkap, nlp_luka, nlp_tewas = extract_victims(full_text)
        
        # Ambil nilai maksimal antara data terstruktur asli vs hasil ekstraksi NLP
        orig_tangkap = pd.to_numeric(row.get('jumlah_ditangkap', 0), errors='coerce')
        orig_tangkap = orig_tangkap if pd.notna(orig_tangkap) else 0
        
        orig_luka = pd.to_numeric(row.get('jumlah_luka', 0), errors='coerce')
        orig_luka = orig_luka if pd.notna(orig_luka) else 0
        
        orig_tewas = pd.to_numeric(row.get('jumlah_tewas', 0), errors='coerce')
        orig_tewas = orig_tewas if pd.notna(orig_tewas) else 0
        
        final_tangkap = max(orig_tangkap, nlp_tangkap)
        final_luka = max(orig_luka, nlp_luka)
        final_tewas = max(orig_tewas, nlp_tewas)
        
        new_tangkap_list.append(final_tangkap)
        new_luka_list.append(final_luka)
        new_tewas_list.append(final_tewas)
        
    df['jumlah_ditangkap'] = new_tangkap_list
    df['jumlah_luka'] = new_luka_list
    df['jumlah_tewas'] = new_tewas_list
    
    # Otomatis flag 'indikasi_kriminalisasi' = True jika ada yang ditangkap/luka/tewas
    mask_represi = (df['jumlah_ditangkap'] > 0) | (df['jumlah_luka'] > 0) | (df['jumlah_tewas'] > 0)
    df.loc[mask_represi, 'indikasi_kriminalisasi'] = True
    
    new_tot_tangkap = df['jumlah_ditangkap'].sum()
    new_tot_luka = df['jumlah_luka'].sum()
    new_tot_tewas = df['jumlah_tewas'].sum()
    new_tot_kasus = df[df['indikasi_kriminalisasi'] == True].shape[0]
    
    print(f"NLP Extracted Totals -> Ditangkap: {new_tot_tangkap}, Luka: {new_tot_luka}, Tewas: {new_tot_tewas}, Kasus Kriminalisasi: {new_tot_kasus}")
    
    df.to_csv(filepath, index=False)
    print(f"Data saved to: {filepath}")

if __name__ == '__main__':
    dataset_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/processed/sulawesi_konflik_agraria_tanahkita.csv'))
    process_dataset(dataset_path)
