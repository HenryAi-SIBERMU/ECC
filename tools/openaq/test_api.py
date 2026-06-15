#!/usr/bin/env python3
"""
Test OpenAQ API - Search locations in Indonesia (Sulawesi)
"""

import requests
import json

API_KEY = "e60fbf886cd900097ff7362b8332161680d2c2e2b4ee1fd7f84aa4ec9af718f5"
BASE_URL = "https://api.openaq.org/v3"

headers = {
    "X-API-Key": API_KEY
}

print("="*70)
print("🌐 Testing OpenAQ API - Indonesia Locations")
print("="*70)

# Test 1: Get locations in Indonesia
print("\n📍 Test 1: Searching locations in Indonesia...")
response = requests.get(
    f"{BASE_URL}/locations",
    headers=headers,
    params={
        "countries": "ID",  # Indonesia
        "limit": 100
    }
)

print(f"Status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    found = data['meta']['found']
    results = data['results']
    
    print(f"✅ Found: {found} locations in Indonesia")
    print(f"Retrieved: {len(results)} locations")
    
    # Show first 10
    print("\n📋 Sample locations:")
    for i, loc in enumerate(results[:10], 1):
        name = loc['name']
        locality = loc.get('locality', 'N/A')
        coords = loc.get('coordinates', {})
        lat = coords.get('latitude', 'N/A')
        lon = coords.get('longitude', 'N/A')
        
        sensors = loc.get('sensors', [])
        params = [s['parameter']['displayName'] for s in sensors]
        
        print(f"  {i}. {name}")
        print(f"     Location: {locality}")
        print(f"     Coords: {lat}, {lon}")
        print(f"     Parameters: {', '.join(params)}")
    
    # Check for Sulawesi locations
    print("\n🔍 Searching for Sulawesi locations...")
    sulawesi_keywords = ['sulawesi', 'makassar', 'manado', 'palu', 'kendari', 'gorontalo', 'mamuju']
    sulawesi_locs = []
    
    for loc in results:
        name_lower = loc['name'].lower()
        locality_lower = (loc.get('locality') or '').lower()
        
        for keyword in sulawesi_keywords:
            if keyword in name_lower or keyword in locality_lower:
                sulawesi_locs.append(loc)
                break
    
    if sulawesi_locs:
        print(f"✅ Found {len(sulawesi_locs)} locations in Sulawesi!")
        for loc in sulawesi_locs:
            print(f"  - {loc['name']} ({loc.get('locality', 'N/A')})")
    else:
        print("❌ No Sulawesi locations found in first 100 results")
        print("   Need to paginate or use geospatial search")

else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)

print("\n" + "="*70)
