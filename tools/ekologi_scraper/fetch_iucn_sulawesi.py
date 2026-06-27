import requests
import json
import pandas as pd
import os
import time

def fetch_iucn_data():
    print("Mencoba mengambil data spesies terancam dari IUCN Red List API...")
    
    # IUCN Red List API v3 membutuhkan token.
    # Namun untuk beberapa endpoint region list, token publik kadang bisa digunakan atau kita butuh API token khusus.
    # Disarankan pengguna memasukkan token jika skrip ini gagal (Unauthorized).
    TOKEN = os.environ.get('IUCN_TOKEN', '9bb4facb6d23f48efbf424bb05c0c1ef1cf6f468393bc745d42179ac4aca5fee')
    
    # Target pencarian: Mamalia, Aves, dll yang terancam di Indonesia (kemudian difilter untuk satwa endemik Sulawesi)
    # Langkah 1: Get species in country (ID = Indonesia)
    url_country = f"https://apiv3.iucnredlist.org/api/v3/country/getspecies/ID?token={TOKEN}"
    
    print("Mengunduh daftar seluruh spesies di Indonesia dari IUCN...")
    try:
        res = requests.get(url_country, timeout=15)
        if res.status_code == 200:
            data = res.json()
            species_list = data.get('result', [])
            print(f"Berhasil menemukan {len(species_list)} spesies di Indonesia.")
            
            # Filter hanya yang Endangered (EN) atau Critically Endangered (CR) atau Vulnerable (VU)
            threatened = [s for s in species_list if s.get('category') in ['CR', 'EN', 'VU']]
            print(f"Terdapat {len(threatened)} spesies berstatus terancam (CR, EN, VU).")
            
            # Filter satwa endemik Sulawesi (secara statis berdasarkan nama ilmiah umum)
            # Anoa (Bubalus depressicornis, Bubalus quarlesi)
            # Babirusa (Babyrousa babyrussa, Babyrousa celebensis, Babyrousa togeanensis)
            # Tarsius (Tarsius spp.)
            # Macaca (Macaca nigra, Macaca maura, dll)
            sulawesi_keywords = ['Bubalus', 'Babyrousa', 'Tarsius', 'Macaca', 'Ailurops', 'Macrogalidia', 'Sus celebensis']
            
            sulawesi_species = []
            for s in threatened:
                sci_name = s.get('scientific_name', '')
                if any(kw in sci_name for kw in sulawesi_keywords):
                    sulawesi_species.append(s)
            
            print(f"\nMenemukan {len(sulawesi_species)} spesies/genus target endemik Sulawesi yang terancam:")
            for s in sulawesi_species:
                print(f"- {s.get('scientific_name')} ({s.get('category')})")
                
            # Simpan ke CSV
            if sulawesi_species:
                df = pd.DataFrame(sulawesi_species)
                out_dir = os.path.join("data", "raw")
                os.makedirs(out_dir, exist_ok=True)
                out_path = os.path.join(out_dir, "iucn_threatened_sulawesi.csv")
                df.to_csv(out_path, index=False)
                print(f"\nData berhasil disimpan ke {out_path}")
        else:
            print(f"Gagal mengambil data dari IUCN API. Status: {res.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"Error koneksi ke IUCN API: {e}")

if __name__ == "__main__":
    fetch_iucn_data()
