#!/usr/bin/env python3
"""
TEST SAMPLING: Cek apakah ada data Indonesia di OpenAQ
Ambil 2 page saja (200 lokasi) untuk test
"""

import requests
import json

API_KEY = "e60fbf886cd900097ff7362b8332161680d2c2e2b4ee1fd7f84aa4ec9af718f5"
BASE_URL = "https://api.openaq.org/v3"

headers = {
    "X-API-Key": API_KEY
}

print("="*70)
print("🧪 TEST SAMPLING - Indonesia Locations (2 pages only)")
print("="*70)

# Test dengan filter countries=ID
print("\n📊 Testing filter: countries=ID")

for page in [1, 2]:
    print(f"\n📄 Page {page}:")
    
    response = requests.get(
        f"{BASE_URL}/locations",
        headers=headers,
        params={
            "countries": "ID",
            "limit": 100,
            "page": page
        }
    )
    
    if response.status_code != 200:
        print(f"   ❌ Error {response.status_code}: {response.text[:200]}")
        continue
    
    data = response.json()
    results = data.get('results', [])
    
    print(f"   ✅ Found {len(results)} locations")
    
    if results:
        # Check countries
        countries = {}
        indonesia_locs = []
        
        for loc in results:
            country_code = loc.get('country', {}).get('code')
            country_name = loc.get('country', {}).get('name')
            
            if country_code not in countries:
                countries[country_code] = 0
            countries[country_code] += 1
            
            if country_code == 'ID':
                lat = loc.get('coordinates', {}).get('latitude')
                lon = loc.get('coordinates', {}).get('longitude')
                city = loc.get('city')
                locality = loc.get('locality')
                name = loc.get('name')
                
                # Check parameters
                sensors = loc.get('sensors', [])
                params = [s['parameter']['name'] for s in sensors]
                has_pm = 'pm25' in params or 'pm10' in params
                
                indonesia_locs.append({
                    'name': name,
                    'city': city or locality,
                    'lat': lat,
                    'lon': lon,
                    'params': params,
                    'has_pm': has_pm
                })
        
        print(f"\n   📍 Countries found:")
        for cc, count in countries.items():
            print(f"      {cc}: {count} locations")
        
        if indonesia_locs:
            print(f"\n   🇮🇩 Indonesia locations with PM data:")
            for loc in indonesia_locs:
                if loc['has_pm']:
                    print(f"      • {loc['name']} ({loc['city']})")
                    print(f"        Lat/Lon: {loc['lat']}, {loc['lon']}")
                    print(f"        Parameters: {', '.join(loc['params'])}")
        else:
            print(f"\n   ⚠️  No Indonesia locations found on this page")
    
    if len(results) < 100:
        print(f"\n   ℹ️  Last page reached")
        break

print("\n" + "="*70)
print("🎯 KESIMPULAN:")
print("   Kalau tidak ada data Indonesia sama sekali,")
print("   berarti kita harus pakai sumber alternatif:")
print("   1. Portal Open Data Provinsi Sulawesi")
print("   2. BPS Web API (tabel Lingkungan)")
print("="*70)
