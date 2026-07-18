#!/usr/bin/env python3
"""Test if TanahKita has API endpoints"""

import requests
import json

# Try potential API endpoints
test_urls = [
    "https://tanahkita.id/api/konflik",
    "https://tanahkita.id/api/data/konflik",
    "https://tanahkita.id/api/v1/konflik",
    "https://tanahkita.id/data/konflik.json",
]

print("=== Testing API endpoints ===\n")

for url in test_urls:
    try:
        response = requests.get(url, timeout=5)
        print(f"✅ {url}")
        print(f"   Status: {response.status_code}")
        print(f"   Content-Type: {response.headers.get('Content-Type')}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"   JSON keys: {list(data.keys())[:5]}")
            except:
                print(f"   Not JSON, text length: {len(response.text)}")
        print()
    except Exception as e:
        print(f"❌ {url}: {e}\n")

# Check the main list page for Ajax/XHR
print("\n=== Checking main page for datatables Ajax ===")
response = requests.get("https://tanahkita.id/data-konflik")
if 'dataTables' in response.text or 'ajax' in response.text.lower():
    print("✅ Found dataTables or Ajax references")
    # Extract potential Ajax URL
    import re
    ajax_matches = re.findall(r'"ajax":\s*["\']([^"\']+)["\']', response.text)
    if ajax_matches:
        print(f"   Possible Ajax endpoint: {ajax_matches}")
else:
    print("❌ No Ajax/dataTables found")
