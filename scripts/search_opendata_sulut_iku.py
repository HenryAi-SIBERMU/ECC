#!/usr/bin/env python3
"""
Search Portal Open Data Sulut untuk dataset IKU (Kualitas Udara) historis
"""

import requests

API_URL = 'https://opendata.sulutprov.go.id/api/3/action/package_search'

keywords = [
    'kualitas udara',
    'IKU',
    'indeks kualitas udara',
    'udara',
    'IKLH',
    'lingkungan hidup'
]

print("="*70)
print("🔍 Search Open Data Sulut - Dataset Kualitas Udara")
print("="*70)

all_datasets = {}

for keyword in keywords:
    print(f"\n📌 Keyword: '{keyword}'")
    
    try:
        response = requests.get(API_URL, params={'q': keyword, 'rows': 100}, timeout=10)
        
        if response.status_code != 200:
            print(f"   ❌ Error {response.status_code}")
            continue
        
        data = response.json()
        
        if not data.get('success'):
            print(f"   ⚠️  API returned success=false")
            continue
        
        results = data.get('result', {}).get('results', [])
        
        if not results:
            print(f"   ℹ️  No results")
            continue
        
        print(f"   ✅ Found {len(results)} datasets")
        
        for dataset in results:
            ds_id = dataset.get('id')
            ds_name = dataset.get('name')
            ds_title = dataset.get('title', 'N/A')
            
            if ds_id not in all_datasets:
                all_datasets[ds_id] = {
                    'id': ds_id,
                    'name': ds_name,
                    'title': ds_title,
                    'keywords': [keyword]
                }
            else:
                all_datasets[ds_id]['keywords'].append(keyword)
    
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

print("\n" + "="*70)
if all_datasets:
    print(f"📊 TOTAL UNIQUE DATASETS: {len(all_datasets)}")
    print("="*70)
    
    for ds_id, info in all_datasets.items():
        print(f"\n🔖 {info['title']}")
        print(f"   ID: {info['id']}")
        print(f"   Name: {info['name']}")
        print(f"   Keywords: {', '.join(set(info['keywords']))}")
else:
    print("❌ Tidak ada dataset kualitas udara di Open Data Sulut")

print("\n" + "="*70)
