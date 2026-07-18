#!/usr/bin/env python3
"""
Cari data Kualitas Udara / IKU / PM2.5 di BPS Web API
"""

import requests
import json

BASE_URL = "https://webapi.bps.go.id/v1/api/interoperabilitas"

print("="*70)
print("🔍 Mencari Data Kualitas Udara di BPS Web API")
print("="*70)

keywords = [
    "kualitas udara",
    "indeks kualitas udara",
    "IKU",
    "PM2.5",
    "PM10",
    "polusi udara",
    "pencemaran udara",
    "udara"
]

all_results = {}

for keyword in keywords:
    print(f"\n📌 Keyword: '{keyword}'")
    
    try:
        response = requests.get(
            f"{BASE_URL}/list",
            params={
                "keyword": keyword,
                "type": "all"
            },
            timeout=10
        )
        
        if response.status_code != 200:
            print(f"   ❌ Error {response.status_code}")
            continue
        
        data = response.json()
        
        if 'data' in data and len(data['data']) > 0:
            results = data['data']
            print(f"   ✅ Ditemukan {len(results)} tabel")
            
            for item in results[:5]:  # Show top 5
                table_id = item.get('table_id')
                title = item.get('title')
                subcat = item.get('subcat', {}).get('subcat_name', 'N/A')
                
                if table_id not in all_results:
                    all_results[table_id] = {
                        'id': table_id,
                        'title': title,
                        'subcat': subcat,
                        'keywords': [keyword]
                    }
                else:
                    all_results[table_id]['keywords'].append(keyword)
                
                print(f"      • [{table_id}] {title}")
                print(f"        Kategori: {subcat}")
        else:
            print(f"   ℹ️  Tidak ada hasil")
    
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

print("\n" + "="*70)
print("📊 RINGKASAN TABEL DITEMUKAN:")
print("="*70)

if all_results:
    for table_id, info in sorted(all_results.items()):
        print(f"\n🔖 [{table_id}] {info['title']}")
        print(f"   Kategori: {info['subcat']}")
        print(f"   Cocok dengan keyword: {', '.join(set(info['keywords']))}")
else:
    print("\n❌ TIDAK ADA DATA KUALITAS UDARA di BPS Web API")
    print("\n💡 REKOMENDASI:")
    print("   → Gunakan Portal Open Data Provinsi Sulawesi")
    print("   → Atau gunakan data proxy (NASA FIRMS hotspot)")

print("\n" + "="*70)
