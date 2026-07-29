import os
import json
import requests
from pathlib import Path
import urllib3
urllib3.disable_warnings()

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / 'data' / 'raw' / 'ika_ngo'
RAW_DIR.mkdir(parents=True, exist_ok=True)

# List of documents from Google Vertex AI Search
DOCUMENTS = [
    {
        "filename": "Earthworks_Tailing_Filtered_IMIP_2026.pdf",
        "title": "Tailing yang Difilter di Indonesia",
        "publisher": "Earthworks",
        "year": 2026,
        "description": "Laporan insiden jebolnya fasilitas tailing PT Huayue Nickel Cobalt (IMIP) ke Sungai Bahodopi, mencakup temuan kadar Kromium Heksavalen (Cr6+).",
        "source_url": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHrcFBSrNvQXdpWNcSLgI40GxI9Mz3y3EDvaAuUCcXt8m9CA9-8m62Mfz1air59JYdBhlyWfvqHp_2O4looTSQH2hTTAhb3RtT2Jwwkks-noSZO82s9U9N4Fg03EvuUt2DszgPymEtmL1WnQYeJJByPS_BzD2iKPj-sauPetyAqCL9rdSDK89kXaihZ0XU="
    },
    {
        "filename": "AEER_Risiko_Laut_IMIP_Cr6.pdf",
        "title": "Kebijakan, Risiko, dan Pencegahan Dampak Pertambangan Nikel pada Laut di Indonesia",
        "publisher": "AEER",
        "year": 2025, # estimated
        "description": "Hasil pemantauan lingkungan Morowali, termasuk analisis kadar Kromium Heksavalen (Cr6+) di perairan sekitar kawasan IMIP.",
        "source_url": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHR-1q0IKXzAo_0WFp-gNMoGpAKZ_gnoLKP8xt1lFei9QXzIzVzUtiNl9aEUNViwbvS5La9TrDtpDjRozmn2UmTVANPwFQ0Hl3VXdc1MRC3Xlqz49I2dXOOO9KmQDSQ6zws7AXo2qw4BG10r_quszIvnp5waJ0CUkLErRklwOeF8X3sLCP0aHfEUBenYAvGcO7oqSgIII_f75GuTKqk8lbyONqBS25rRiTcqKsv1xo8pMIrs4entSVgTIWEZbymElfHB6OFGj_cU4c3VOyLgQ=="
    },
    {
        "filename": "WALHI_Sulsel_Lumbung_Polusi.pdf",
        "title": "Policy Paper: Sulawesi Lumbung Polusi",
        "publisher": "WALHI Sulsel",
        "year": 2024,
        "description": "Tinjauan pencemaran kromium heksavalen di aliran sungai dan pesisir akibat limpasan air hujan dari stockpile bijih nikel IMIP.",
        "source_url": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH-1Zlj8dzMx7yBfIGzkdi1TS8G-OWBAP5zZm4fXRQUP4DBMGOubGoC5BYAyVi8HLLenNw9kJEU7aNN55uCmEI-9q7BiB2pK1J9m-Cf5Qubo3AkptpyV4zu7AtrgG8Xdm5yA8K3tKFsdsKQ3WtehTVgeeyoNaJS6ZkB9cg_5VSCTu4-6LxL489qGVV0jnEwIwORhw=="
    },
    {
        "filename": "Tesis_UGM_Matarape_Morowali.pdf",
        "title": "Analisis Kualitas Air Limpasan Tambang Nikel di Morowali",
        "publisher": "UGM",
        "year": 2023,
        "description": "Penelitian akademis menguji kualitas air limpasan dari pertambangan nikel laterit di Desa Matarape, Kabupaten Morowali.",
        "source_url": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGc3EbvW6IYZVtqiqXmxtv-BKKgAN24QyR2-lB_4ApIyvS30e31LLPkIkcDENnutzUf5uW2n96pCLw7c9BV5JiCgCzZMGW-oOM9_TPMQEFOgrqWz8dLP3x8uFRfWZXXb4ZXnV2zlOwp8fnfETHI2qM="
    }
]

def resolve_url(redirect_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }
    try:
        r = requests.get(redirect_url, headers=headers, allow_redirects=True, verify=False, timeout=20)
        return r.url
    except Exception as e:
        print(f"Error resolving {redirect_url}: {e}")
        return redirect_url

def download_file(url, filepath):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'https://www.google.com/'
    }
    
    try:
        r = requests.get(url, headers=headers, stream=True, verify=False, timeout=30)
        if r.status_code == 200:
            with open(filepath, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
        else:
            print(f"Failed HTTP {r.status_code} for {url}")
            return False
    except Exception as e:
        print(f"Download failed: {e}")
        return False

def main():
    print("Fetching NGO Water Pollution Data for Morowali...")
    
    metadata = []
    for doc in DOCUMENTS:
        print(f"\nProcessing: {doc['title']}")
        
        filepath = RAW_DIR / doc['filename']
        if filepath.exists():
            print(f"[-] Already exists: {doc['filename']}")
            doc['local_path'] = str(filepath.relative_to(BASE_DIR))
            metadata.append(doc)
            continue
            
        print("[*] Resolving real URL...")
        real_url = resolve_url(doc['source_url'])
        print(f"    -> {real_url}")
        
        print(f"[*] Downloading to {doc['filename']}...")
        success = download_file(real_url, filepath)
        
        if success:
            print(f"[+] Download complete: {doc['filename']}")
            doc['resolved_url'] = real_url
            doc['local_path'] = str(filepath.relative_to(BASE_DIR))
            metadata.append(doc)
        else:
            print(f"[!] Could not download {doc['filename']}")
            
    # Save metadata
    meta_path = RAW_DIR / 'metadata_ika_ngo.json'
    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=4, ensure_ascii=False)
        
    print(f"\nMetadata saved to {meta_path.relative_to(BASE_DIR)}")
    print("Done!")

if __name__ == "__main__":
    main()
