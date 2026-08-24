import os
import json
import threading
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env'))

client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

CACHE_FILE = os.path.join(os.path.dirname(__file__), 'krim_llm_cache.json')
cache_lock = threading.Lock()

def load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_cache(cache):
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, indent=4)

def extract_kriminalisasi_llm(text: str) -> dict:
    """
    Perform NER using OpenAI to extract Kriminalisasi data.
    """
    if not text or not str(text).strip() or str(text) == 'nan':
        return {"indikasi_kriminalisasi": False, "jumlah_ditangkap": 0, "jumlah_luka": 0, "jumlah_tewas": 0}
        
    with cache_lock:
        cache = load_cache()
        # Simple hash for cache key (first 100 chars + length)
        cache_key = f"{str(text)[:100]}_{len(str(text))}"
        if cache_key in cache:
            return cache[cache_key]
        
    prompt = f"""
Anda adalah pakar HAM (Hak Asasi Manusia) dan Natural Language Processing.
Tugas Anda adalah membaca narasi konflik agraria di bawah ini dan mengekstrak DATA KRIMINALISASI DAN KEKERASAN.

Narasi Konflik:
\"\"\"{text}\"\"\"

Instruksi Analisis:
1. Tentukan apakah ada "indikasi_kriminalisasi" (true/false).
   Kriminalisasi/Kekerasan meliputi: 
   - Penangkapan/penahanan warga tanpa prosedur atau pemanggilan paksa polisi (contoh: warga ditangkap, warga dibawa ke polisi).
   - Kekerasan fisik oleh aparat atau preman (contoh: warga dipukul, warga dianiaya, warga luka-luka).
   - Penembakan aparat atau kematian akibat bentrok konflik.
   - Penggusuran paksa secara beringas atau intimidasi represif aparat kepolisian/TNI yang disebutkan.
   - Jika narasi secara umum menyebut ada kriminalisasi walau angkanya tidak jelas, indikasi ini harus true.
2. Tentukan "jumlah_ditangkap" (integer). Jika spesifik (misal: '2 orang ditangkap'), isi 2. Jika disebut 'beberapa', 'sejumlah', isi estimasi min (misal 2). Jika tidak ada isi 0.
3. Tentukan "jumlah_luka" (integer). Jika luka/kritis/babak belur. 
4. Tentukan "jumlah_tewas" (integer).

Output wajib dalam format JSON murni tanpa markdown, dengan struktur eksak berikut:
{{
  "indikasi_kriminalisasi": boolean,
  "jumlah_ditangkap": int,
  "jumlah_luka": int,
  "jumlah_tewas": int
}}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that only outputs valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0
        )
        result_text = response.choices[0].message.content.strip()
        
        # Clean markdown if accidentally present
        if result_text.startswith("```json"):
            result_text = result_text[7:-3].strip()
        elif result_text.startswith("```"):
            result_text = result_text[3:-3].strip()
            
        data = json.loads(result_text)
        
        # Validation
        validated = {
            "indikasi_kriminalisasi": bool(data.get("indikasi_kriminalisasi", False)),
            "jumlah_ditangkap": int(data.get("jumlah_ditangkap", 0)),
            "jumlah_luka": int(data.get("jumlah_luka", 0)),
            "jumlah_tewas": int(data.get("jumlah_tewas", 0))
        }
        
        with cache_lock:
            cache = load_cache()
            cache[cache_key] = validated
            save_cache(cache)
            
        return validated
    except Exception as e:
        print(f"Error parsing LLM response: {e}")
        return {"indikasi_kriminalisasi": False, "jumlah_ditangkap": 0, "jumlah_luka": 0, "jumlah_tewas": 0}

def process_dataset(filepath):
    print(f"Reading dataset: {filepath}")
    df = pd.read_csv(filepath)
    
    old_krim = df['indikasi_kriminalisasi'].sum() if 'indikasi_kriminalisasi' in df.columns else 0
    old_tangkap = pd.to_numeric(df['jumlah_ditangkap'], errors='coerce').fillna(0).sum() if 'jumlah_ditangkap' in df.columns else 0
    old_luka = pd.to_numeric(df['jumlah_luka'], errors='coerce').fillna(0).sum() if 'jumlah_luka' in df.columns else 0
    old_tewas = pd.to_numeric(df['jumlah_tewas'], errors='coerce').fillna(0).sum() if 'jumlah_tewas' in df.columns else 0
    
    print(f"Original Totals -> Insiden Kriminalisasi: {old_krim}, Ditangkap: {old_tangkap}, Luka: {old_luka}, Tewas: {old_tewas}")
    
    new_krim_list = []
    new_tangkap_list = []
    new_luka_list = []
    new_tewas_list = []
    
    # Process sequentially for safety with caching
    for idx, row in tqdm(df.iterrows(), total=len(df)):
        # Gabungkan narasi, deskripsi, dan judul
        parts = []
        if pd.notna(row.get('judul')): parts.append(str(row['judul']))
        if pd.notna(row.get('deskripsi')): parts.append(str(row['deskripsi']))
        if pd.notna(row.get('narasi')): parts.append(str(row['narasi']))
        full_text = " ".join(parts)
        
        llm_data = extract_kriminalisasi_llm(full_text)
        
        # Ambil nilai maksimal antara data terstruktur asli (jika ada) vs hasil ekstraksi NLP LLM
        orig_tangkap = pd.to_numeric(row.get('jumlah_ditangkap', 0), errors='coerce') if 'jumlah_ditangkap' in row else 0
        orig_tangkap = orig_tangkap if pd.notna(orig_tangkap) else 0
        
        orig_luka = pd.to_numeric(row.get('jumlah_luka', 0), errors='coerce') if 'jumlah_luka' in row else 0
        orig_luka = orig_luka if pd.notna(orig_luka) else 0
        
        orig_tewas = pd.to_numeric(row.get('jumlah_tewas', 0), errors='coerce') if 'jumlah_tewas' in row else 0
        orig_tewas = orig_tewas if pd.notna(orig_tewas) else 0
        
        final_tangkap = max(orig_tangkap, llm_data['jumlah_ditangkap'])
        final_luka = max(orig_luka, llm_data['jumlah_luka'])
        final_tewas = max(orig_tewas, llm_data['jumlah_tewas'])
        
        # Kriminalisasi true if explicitly flagged by LLM OR if there are any victims
        final_krim = llm_data['indikasi_kriminalisasi'] or (final_tangkap > 0) or (final_luka > 0) or (final_tewas > 0)
        
        new_krim_list.append(final_krim)
        new_tangkap_list.append(final_tangkap)
        new_luka_list.append(final_luka)
        new_tewas_list.append(final_tewas)
        
    df['indikasi_kriminalisasi'] = new_krim_list
    df['jumlah_ditangkap'] = new_tangkap_list
    df['jumlah_luka'] = new_luka_list
    df['jumlah_tewas'] = new_tewas_list
    
    new_krim = df['indikasi_kriminalisasi'].sum()
    new_tangkap = df['jumlah_ditangkap'].sum()
    new_luka = df['jumlah_luka'].sum()
    new_tewas = df['jumlah_tewas'].sum()
    
    print(f"\nNew LLM Totals -> Insiden Kriminalisasi: {new_krim}, Ditangkap: {new_tangkap}, Luka: {new_luka}, Tewas: {new_tewas}")
    
    df.to_csv(filepath, index=False)
    print(f"Saved extracted data back to {filepath}")

if __name__ == "__main__":
    v3_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'processed', 'sulawesi_konflik_agraria_tanahkita_v3.csv')
    process_dataset(v3_path)
