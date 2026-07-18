import os
import json
import time
import requests
import pandas as pd
from datetime import datetime
from tqdm import tqdm

API_KEY = "06fd644648629502353deaed29fc6383"
BASE_URL = "https://webapi.bps.go.id/v1/api"

# Target Kabupaten for Sulawesi Tengah (72xx) and Sulawesi Tenggara (74xx)
TARGET_PROVINCES = ["72", "74"]

def get_kabupaten_list(prov_code):
    """Fetch list of kabupaten for a province from BPS API"""
    url = f"{BASE_URL}/domain/type/kabbyprov/prov/{prov_code}/key/{API_KEY}/"
    resp = requests.get(url)
    if resp.status_code == 200:
        data = resp.json().get('data', [])
        # BPS domain string is usually 4 digits: prov_code + kab_code (e.g., 7201)
        return [(d['domain_id'], d['domain_name']) for d in data[1:]] # Skip first which is usually the province itself
    return []

def find_pdrb_var_id(domain_id):
    """Find the var_id for 'PDRB... Atas Dasar Harga Berlaku Menurut Lapangan Usaha' in a specific domain"""
    url = f"{BASE_URL}/list/model/data/domain/{domain_id}/key/{API_KEY}/"
    try:
        resp = requests.get(url)
        data = resp.json().get('data', [])
        data = data[1] if len(data) > 1 else [] # the actual data array is in [1] for dynamictable list
        
        for item in data:
            title = str(item.get('title', '')).lower()
            if 'pdrb' in title and 'lapangan usaha' in title and 'berlaku' in title:
                return item['var_id']
    except Exception as e:
        print(f"Error finding var_id for {domain_id}: {e}")
    return None

def fetch_data_for_var(domain_id, var_id, start_year, end_year):
    """Fetch the actual PDRB dataset"""
    # var/{var_id} will give us the variables. 
    # To get actual data, we need model/data. 
    # BPS API is complex. Usually it's better to fetch dynamic table data via /data/
    # However, BPS API /data/ is deprecated in favor of /list/model/data/...? No, it's /data/
    url = f"{BASE_URL}/data/domain/{domain_id}/var/{var_id}/key/{API_KEY}/"
    try:
        resp = requests.get(url)
        return resp.json()
    except Exception as e:
        print(f"Error fetching data for {domain_id}: {e}")
    return None

def main():
    print("Mencari Kabupaten di Sulteng dan Sultra...")
    all_kabupaten = []
    for prov in TARGET_PROVINCES:
        kabs = get_kabupaten_list(prov)
        print(f"Provinsi {prov}: ditemukan {len(kabs)} kabupaten/kota.")
        all_kabupaten.extend(kabs)
        
    print(f"Total Kabupaten/Kota yang akan discrape: {len(all_kabupaten)}")
    print(all_kabupaten)

if __name__ == '__main__':
    main()
