#!/usr/bin/env python3
"""
Fetch all OpenAQ locations in Sulawesi cities
Target: PM2.5, PM10 data for 2014-2024
"""

import requests
import json
import csv
from pathlib import Path

API_KEY = "e60fbf886cd900097ff7362b8332161680d2c2e2b4ee1fd7f84aa4ec9af718f5"
BASE_URL = "https://api.openaq.org/v3"

headers = {
    "X-API-Key": API_KEY
}

print("="*70)
print("📡 Fetching All Sulawesi Air Quality Locations")
print("="*70)

cities = ['Makassar', 'Manado', 'Palu', 'Kendari', 'Gorontalo', 'Mamuju']
all_locations = []

for city in cities:
    print(f"\n🏙️  Fetching: {city}...")
    
    page = 1
    while True:
        response = requests.get(
            f"{BASE_URL}/locations",
            headers=headers,
            params={
                "city": city,
                "limit": 100,
                "page": page
            }
        )
        
        if response.status_code != 200:
            print(f"   ⚠️  Error on page {page}: {response.status_code}")
            break
        
        data = response.json()
        results = data['results']
        
        if not results:
            break
        
        for loc in results:
            # Extract key info
            location_data = {
                'location_id': loc['id'],
                'name': loc['name'],
                'city': city,
                'locality': loc.get('locality'),
                'latitude': loc.get('coordinates', {}).get('latitude'),
                'longitude': loc.get('coordinates', {}).get('longitude'),
                'country': loc.get('country', {}).get('name'),
                'country_code': loc.get('country', {}).get('code'),
                'owner': loc.get('owner', {}).get('name'),
                'provider': loc.get('provider', {}).get('name'),
                'is_mobile': loc.get('isMobile'),
                'is_monitor': loc.get('isMonitor'),
                'timezone': loc.get('timezone'),
            }
            
            # Extract parameters available
            sensors = loc.get('sensors', [])
            params = [s['parameter']['name'] for s in sensors]
            location_data['parameters'] = ', '.join(params)
            
            # Check if has PM2.5 or PM10
            location_data['has_pm25'] = 'pm25' in params
            location_data['has_pm10'] = 'pm10' in params
            
            # Date range
            first = loc.get('datetimeFirst', {})
            last = loc.get('datetimeLast', {})
            location_data['date_first'] = first.get('utc', '') if first else ''
            location_data['date_last'] = last.get('utc', '') if last else ''
            
            all_locations.append(location_data)
        
        print(f"   Page {page}: {len(results)} locations")
        
        # Check if more pages
        if len(results) < 100:
            break
        page += 1

print(f"\n✅ Total locations found: {len(all_locations)}")

# Filter to PM2.5/PM10 locations
pm_locations = [loc for loc in all_locations if loc['has_pm25'] or loc['has_pm10']]
print(f"📊 Locations with PM2.5/PM10: {len(pm_locations)}")

# Save to CSV
output_dir = Path("data/raw/openaq")
output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / "sulawesi_locations.csv"

if pm_locations:
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=pm_locations[0].keys())
        writer.writeheader()
        writer.writerows(pm_locations)
    
    print(f"\n💾 Saved to: {output_file}")
    
    # Summary by city
    print("\n📋 Summary by City:")
    for city in cities:
        city_locs = [loc for loc in pm_locations if loc['city'] == city]
        pm25_count = sum(1 for loc in city_locs if loc['has_pm25'])
        pm10_count = sum(1 for loc in city_locs if loc['has_pm10'])
        print(f"  {city}: {len(city_locs)} locations (PM2.5: {pm25_count}, PM10: {pm10_count})")
    
    # Check date coverage
    print("\n📅 Date Coverage Check:")
    for loc in pm_locations[:5]:  # Sample first 5
        print(f"  {loc['name']} ({loc['city']})")
        print(f"    First: {loc['date_first'][:10] if loc['date_first'] else 'N/A'}")
        print(f"    Last: {loc['date_last'][:10] if loc['date_last'] else 'N/A'}")

else:
    print("❌ No PM2.5/PM10 locations found!")

print("\n" + "="*70)
