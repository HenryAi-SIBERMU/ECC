import re

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    old_func = """def get_spa_aktual(prov: str) -> float:
    import re, os
    spa_val = 60.0
    try:
        path_kemenkes = os.path.join("data", "raw", "profil kesehatan_nasional_kemenkes", "raw_kemenkes_puskesmas_2024.csv")
        if os.path.exists(path_kemenkes):
            with open(path_kemenkes, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                items = re.findall(r'([A-Za-z\s]+)\s(\d+,\d+)', content)
                parsed_spa = {k.strip(): float(v.replace(',', '.')) for k, v in items if 'Sulawesi' in k or 'Gorontalo' in k}
                if prov in parsed_spa:
                    spa_val = parsed_spa[prov]
                elif prov == 'Pulau Sulawesi' and len(parsed_spa) > 0:
                    spa_val = sum(parsed_spa.values()) / len(parsed_spa)
    except Exception:
        pass
    return spa_val"""

    new_func = """def get_spa_aktual(prov: str) -> float:
    # Diekstrak dari raw_kemenkes_puskesmas_2024.csv Baris 39 (Persentase Puskesmas SPA)
    parsed_spa = {
        'Gorontalo': 94.12,
        'Sulawesi Barat': 89.84,
        'Sulawesi Tengah': 77.57,
        'Sulawesi Selatan': 67.65,
        'Sulawesi Tenggara': 62.08,
        'Sulawesi Utara': 54.84
    }
    if prov in parsed_spa:
        return parsed_spa[prov]
    elif prov == 'Pulau Sulawesi' or prov == 'Sulawesi':
        return sum(parsed_spa.values()) / len(parsed_spa)
    return 60.0"""
    
    if old_func in content:
        content = content.replace(old_func, new_func)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {filepath}")
    else:
        print(f"Could not find old_func in {filepath}")

fix_file("pages/6_Audit_D3TLH.py")
fix_file("tools/algo_skoring_provinsi_ZscoreEWM/kalkulasi_provinsi_sulawesi.py")
fix_file("tools/algo_skoring_pulau/kalkulasi_pulau_sulawesi.py")
