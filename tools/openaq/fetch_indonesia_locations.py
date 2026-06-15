#!/usr/bin/env python3
"""
Fetch all OpenAQ locations in Indonesia, then filter for Sulawesi region
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
print("📡 Fetching All Air Quality Locations in INDONESIA")
print("="*70)

all_locations = []
page = 1

while True:
    print(f"\n📄 Fetching page {page}...")
    
    response = requests.get(
        f"{BASE_URL}/locations",
        headers=headers,
        params={
            "countries": "ID",  # Indonesia country code
            "limit": 100,
            "page": page
        }
    )
    
    if response.status_code != 200:
        print(f"   ⚠️  Error: {response.status_code}")
        print(f"   Response: {response.text[:200]}")
        break
    
    data = response.json()
    results = data.get('results', [])
    
    if not results:
        print(f"   ℹ️  No more results on page {page}")
        break
    
    for loc in results:
        # Extract key info
        location_data = {
            'location_id': loc['id'],
            'name': loc['name'],
            'city': loc.get('city'),
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
    
    print(f"   ✅ Found {len(results)} locations (Total: {len(all_locations)})")
    
    # Check if more pages
    if len(results) < 100:
        break
    page += 1

print(f"\n{'='*70}")
print(f"✅ Total Indonesia locations: {len(all_locations)}")

# Filter to PM2.5/PM10 locations
pm_locations = [loc for loc in all_locations if loc['has_pm25'] or loc['has_pm10']]
print(f"📊 Locations with PM2.5/PM10: {len(pm_locations)}")

# Filter for SULAWESI region by latitude/longitude
# Sulawesi bounding box (approximate):
# Latitude: -5.5 (south) to 2.5 (north)
# Longitude: 118.5 (west) to 125.5 (east)
sulawesi_locations = []
for loc in pm_locations:
    lat = loc['latitude']
    lon = loc['longitude']
    if lat and lon:
        if -5.5 <= lat <= 2.5 and 118.5 <= lon <= 125.5:
            sulawesi_locations.append(loc)

print(f"🗺️  Sulawesi region locations: {len(sulawesi_locations)}")

# Save to CSV
output_dir = Path("data/raw/openaq")
output_dir.mkdir(parents=True, exist_ok=True)

# Save all Indonesia PM locations
output_file_all = output_dir / "indonesia_locations_pm.csv"
if pm_locations:
    with open(output_file_all, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=pm_locations[0].keys())
        writer.writeheader()
        writer.writerows(pm_locations)
    print(f"\n💾 All Indonesia PM data saved to: {output_file_all}")

# Save Sulawesi locations
output_file_sulawesi = output_dir / "sulawesi_locations_pm.csv"
if sulawesi_locations:
    with open(output_file_sulawesi, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=sulawesi_locations[0].keys())
        writer.writeheader()
        writer.writerows(sulawesi_locations)
    print(f"💾 Sulawesi PM data saved to: {output_file_sulawesi}")
    
    # Summary
    print(f"\n📋 Sulawesi Locations Summary:")
    for loc in sulawesi_locations:
        pm_types = []
        if loc['has_pm25']:
            pm_types.append('PM2.5')
        if loc['has_pm10']:
            pm_types.append('PM10')
        date_range = ""
        if loc['date_first']:
            date_range = f"{loc['date_first'][:10]} to {loc['date_last'][:10] if loc['date_last'] else 'N/A'}"
        else:
            date_range = "No date info"
        
        print(f"  • {loc['name']} ({loc['city'] or loc['locality'] or 'Unknown'})")
        print(f"    Lat/Lon: {loc['latitude']:.3f}, {loc['longitude']:.3f}")
        print(f"    Parameters: {', '.join(pm_types)}")
        print(f"    Date range: {date_range}")
        print()

else:
    print("❌ No Sulawesi locations with PM2.5/PM10 found!")
    
    # Show all Indonesia locations for reference
    if pm_locations:
        print("\n📍 Available Indonesia PM locations:")
        cities = {}
        for loc in pm_locations:
            city = loc['city'] or loc['locality'] or 'Unknown'
            if city not in cities:
                cities[city] = 0
            cities[city] += 1
        
        for city, count in sorted(cities.items(), key=lambda x: x[1], reverse=True)[:20]:
            print(f"  {city}: {count} locations")

print("\n" + "="*70)
