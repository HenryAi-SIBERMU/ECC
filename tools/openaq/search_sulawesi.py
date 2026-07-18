#!/usr/bin/env python3
"""
Search OpenAQ for Sulawesi air quality locations using geospatial bounding box
Sulawesi coordinates: roughly -6.0 to 2.0 lat, 119.0 to 127.0 lon
"""

import requests
import json

API_KEY = "e60fbf886cd900097ff7362b8332161680d2c2e2b4ee1fd7f84aa4ec9af718f5"
BASE_URL = "https://api.openaq.org/v3"

headers = {
    "X-API-Key": API_KEY
}

print("="*70)
print("🗺️  Searching OpenAQ for Sulawesi Air Quality Locations")
print("="*70)

# Sulawesi bounding box (approximate)
# Southwest corner: -6.0, 119.0
# Northeast corner: 2.0, 127.0
bbox = "119.0,-6.0,127.0,2.0"  # format: minLon,minLat,maxLon,maxLat

print(f"\n📍 Bounding Box: {bbox}")
print("   (Covering entire Sulawesi island)")

response = requests.get(
    f"{BASE_URL}/locations",
    headers=headers,
    params={
        "bbox": bbox,
        "limit": 100
    }
)

print(f"\nStatus: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    found = data['meta']['found']
    results = data['results']
    
    print(f"✅ Found: {found} locations in Sulawesi region")
    print(f"Retrieved: {len(results)} locations\n")
    
    if results:
        print("📋 Locations found:")
        for i, loc in enumerate(results, 1):
            name = loc['name']
            locality = loc.get('locality', 'N/A')
            coords = loc.get('coordinates', {})
            lat = coords.get('latitude', 'N/A')
            lon = coords.get('longitude', 'N/A')
            
            sensors = loc.get('sensors', [])
            params = [s['parameter']['displayName'] for s in sensors]
            
            # Get date range
            first = loc.get('datetimeFirst', {})
            last = loc.get('datetimeLast', {})
            date_first = first.get('utc', 'N/A')[:10] if first else 'N/A'
            date_last = last.get('utc', 'N/A')[:10] if last else 'N/A'
            
            print(f"\n{i}. {name}")
            print(f"   Location: {locality}")
            print(f"   Coordinates: {lat}, {lon}")
            print(f"   Parameters: {', '.join(params)}")
            print(f"   Data range: {date_first} to {date_last}")
            print(f"   Location ID: {loc['id']}")
    else:
        print("❌ No locations found in Sulawesi bounding box")
        print("   OpenAQ might not have data for this region")

else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)

# Also try searching by city names
print("\n" + "="*70)
print("🏙️  Searching by major Sulawesi cities")
print("="*70)

cities = ['Makassar', 'Manado', 'Palu', 'Kendari', 'Gorontalo', 'Mamuju']

for city in cities:
    response = requests.get(
        f"{BASE_URL}/locations",
        headers=headers,
        params={
            "city": city,
            "limit": 10
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        found = data['meta'].get('found', 0)
        if found and found != '0':
            print(f"✅ {city}: Found {found} location(s)")
        else:
            print(f"❌ {city}: No locations found")
    else:
        print(f"⚠️  {city}: API error")

print("\n" + "="*70)
