import requests
import json
import pandas as pd
import os

API_KEY = "0b9fbc7bdccf0bb7bf0ff8502dbd6ec0"
BASE_URL = "https://webapi.bps.go.id/v1/api/list/model/data/domain/0000/var/{} /key/{}/"

def search_bps_variables():
    # Subject 152 is Environment/Lingkungan Hidup
    url = f"https://webapi.bps.go.id/v1/api/list/model/var/domain/0000/subject/152/key/{API_KEY}/"
    resp = requests.get(url)
    data = resp.json()
    bencana_vars = []
    
    if data.get("data") and len(data["data"]) > 1:
        for v in data["data"][1]:
            title = v.get("title", "").lower()
            if "bencana" in title or "banjir" in title or "longsor" in title:
                bencana_vars.append(v)
                
    return bencana_vars

if __name__ == "__main__":
    print("Mencari variabel bencana di BPS...")
    vars_found = search_bps_variables()
    for v in vars_found:
        print(f"ID: {v['var_id']} | Judul: {v['title']}")
        
    if not vars_found:
        print("Tidak menemukan variabel secara langsung, mencoba keyword search.")
