import os
import json
import threading
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env'))

client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

CACHE_FILE = os.path.join(os.path.dirname(__file__), 'llm_ner_cache.json')
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

def deduce_sulawesi_province_llm(text: str, default_val: str = "LUAR_SULAWESI") -> str:
    """
    Perform Zero-Shot NER using OpenAI to deduce the actual province in Sulawesi.
    """
    if not text or not str(text).strip():
        return default_val
        
    with cache_lock:
        cache = load_cache()
        
        # Simple hash for cache key (first 100 chars + length)
        cache_key = f"{text[:100]}_{len(text)}"
        if cache_key in cache:
            return cache[cache_key]
        
    prompt = f"""
Anda adalah pakar Geografi Spasial dan Natural Language Processing.
Tugas Anda adalah mengekstrak LOKASI UTAMA (Provinsi) dari kejadian konflik agraria berdasarkan narasi di bawah ini.

Narasi Konflik:
\"\"\"{text}\"\"\"

Instruksi Analisis Objektif:
1. Ekstrak LOKASI GEOGRAFIS UTAMA tempat terjadinya konflik secara FAKTUAL. 
2. Jika lokasi tersebut BENAR-BENAR berada di Pulau Sulawesi, jawab dengan nama provinsi yang sesuai ('Sulawesi Tengah', 'Sulawesi Tenggara', 'Sulawesi Selatan', 'Sulawesi Utara', 'Sulawesi Barat', 'Gorontalo'). 
   Petunjuk: Daerah-daerah ini ADA di Sulawesi (morowali, konawe, kolaka, bombana, poso, donggala, makassar, manado, minahasa, sangihe, mamuju, majene, polewali, soroako, luwu, bantaeng, buton, muna, wakatobi, banggai, buol, toli-toli, parigi, luwuk, kendari, baubau, palu, bitung, tomohon, kotamobagu, gowa, takalar, jeneponto, bulukumba, sinjai, bone, maros, pangkep, barru, pinrang, enrekang, toraja, palopo).
3. Anda SANGAT DIREKOMENDASIKAN untuk menjawab 'LUAR_SULAWESI' jika:
   - Kasus terjadi di luar Pulau Sulawesi (misal: Riau, Kalimantan, Barito, Sumatera, Jawa, Maluku, Papua).
   - Konteks wilayahnya nasional atau tidak bisa dipastikan secara spesifik berada di Sulawesi.
   - Tidak ada sebutan nama kabupaten/kota yang valid di wilayah provinsi Sulawesi.
4. Jangan memaksa mencocokkan ke Sulawesi jika Anda melihat indikator daerah di luar Sulawesi.
5. Output Anda HANYA SATU STRING EKSAK dari 7 pilihan berikut:
   'Sulawesi Tengah', 'Sulawesi Tenggara', 'Sulawesi Selatan', 'Sulawesi Utara', 'Sulawesi Barat', 'Gorontalo', 'LUAR_SULAWESI'.
Tidak boleh ada penjelasan apapun.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a precise geospatial extraction API. You output ONLY the requested exact string, nothing else."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0,
            max_tokens=10
        )
        
        result = response.choices[0].message.content.strip()
        
        valid_outputs = [
            'Sulawesi Tengah', 'Sulawesi Tenggara', 'Sulawesi Selatan', 
            'Sulawesi Utara', 'Sulawesi Barat', 'Gorontalo', 'LUAR_SULAWESI'
        ]
        
        if result not in valid_outputs:
            print(f"Warning: Unexpected LLM output '{result}', defaulting to {default_val}")
            result = default_val
            
        # Cache the result
        with cache_lock:
            cache = load_cache() # Reload to get other threads' updates
            cache[cache_key] = result
            save_cache(cache)
        
        return result
        
    except Exception as e:
        print(f"LLM API Error: {e}")
        return default_val
