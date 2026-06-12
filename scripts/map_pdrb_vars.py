import requests
import json
from concurrent.futures import ThreadPoolExecutor

API_KEY = "06fd644648629502353deaed29fc6383"
BASE_URL = "https://webapi.bps.go.id/v1/api"

PROVINSI_DOMAINS = {
    "1100": "Aceh", "1200": "Sumatera Utara", "1300": "Sumatera Barat", "1400": "Riau",
    "1500": "Jambi", "1600": "Sumatera Selatan", "1700": "Bengkulu", "1800": "Lampung",
    "1900": "Kepulauan Bangka Belitung", "2100": "Kepulauan Riau", "3100": "DKI Jakarta",
    "3200": "Jawa Barat", "3300": "Jawa Tengah", "3400": "DI Yogyakarta", "3500": "Jawa Timur",
    "3600": "Banten", "5100": "Bali", "5200": "Nusa Tenggara Barat", "5300": "Nusa Tenggara Timur",
    "6100": "Kalimantan Barat", "6200": "Kalimantan Tengah", "6300": "Kalimantan Selatan",
    "6400": "Kalimantan Timur", "6500": "Kalimantan Utara", "7100": "Sulawesi Utara",
    "7200": "Sulawesi Tengah", "7300": "Sulawesi Selatan", "7400": "Sulawesi Tenggara",
    "7500": "Gorontalo", "7600": "Sulawesi Barat", "8100": "Maluku", "8200": "Maluku Utara",
    "9100": "Papua Barat", "9400": "Papua", "9500": "Papua Selatan", "9600": "Papua Tengah",
    "9700": "Papua Pegunungan", "9800": "Papua Barat Daya"
}

def get_all_subjects(domain_id):
    subjects = []
    for page in range(1, 10):
        url = f"{BASE_URL}/list/model/subject/domain/{domain_id}/page/{page}/key/{API_KEY}/"
        try:
            resp = requests.get(url, timeout=10).json()
            data = resp.get('data', [])
            if not data: break
            if len(data) > 1 and isinstance(data[1], list):
                subs = data[1]
                if not subs: break
                subjects.extend(subs)
            else:
                break
        except:
            break
    return subjects

def get_all_vars(domain_id, subject_id):
    variables = []
    for page in range(1, 10):
        url = f"{BASE_URL}/list/model/var/domain/{domain_id}/subject/{subject_id}/page/{page}/key/{API_KEY}/"
        try:
            resp = requests.get(url, timeout=10).json()
            data = resp.get('data', [])
            if not data: break
            if len(data) > 1 and isinstance(data[1], list):
                vrs = data[1]
                if not vrs: break
                variables.extend(vrs)
            else:
                break
        except:
            break
    return variables

def map_domain(domain_id, nama):
    subs = get_all_subjects(domain_id)
    sub_id = None
    for s in subs:
        if isinstance(s, dict) and 'title' in s:
            t = s['title'].lower()
            if 'pdrb' in t or 'domestik regional bruto' in t:
                if 'lapangan usaha' in t:
                    sub_id = s['sub_id']
                    break
    if not sub_id:
        for s in subs:
            if isinstance(s, dict) and 'title' in s:
                t = s['title'].lower()
                if 'pdrb' in t or 'domestik regional bruto' in t:
                    sub_id = s['sub_id']
                    break
    if sub_id:
        vars = get_all_vars(domain_id, sub_id)
        var_id = None
        for v in vars:
            if isinstance(v, dict) and 'title' in v:
                t = v['title'].lower()
                if ('pdrb' in t or 'domestik regional' in t) and 'berlaku' in t and 'kapita' not in t and 'distribusi' not in t and 'laju' not in t and 'pertumbuhan' not in t:
                    var_id = v['var_id']
                    break
        if not var_id:
            for v in vars:
                if isinstance(v, dict) and 'title' in v:
                    t = v['title'].lower()
                    if 'pdrb' in t and 'berlaku' in t:
                        var_id = v['var_id']
                        break
        if var_id:
            print(f"[{nama}] Ketemu Var ID: {var_id}")
            return domain_id, var_id
    print(f"[{nama}] Gagal menemukan Var ID PDRB.")
    return domain_id, None

mapping = {}
with ThreadPoolExecutor(max_workers=20) as executor:
    futures = [executor.submit(map_domain, d, n) for d, n in PROVINSI_DOMAINS.items()]
    for f in futures:
        domain_id, var_id = f.result()
        if var_id:
            mapping[domain_id] = var_id

with open('scripts/pdrb_var_mapping.json', 'w') as f:
    json.dump(mapping, f, indent=2)
print("Selesai! Berhasil mapping", len(mapping), "provinsi.")
