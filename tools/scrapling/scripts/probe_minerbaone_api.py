#!/usr/bin/env python3
"""
MinerbaOne API Probe
Try to find hidden API endpoints
"""

import requests
import json

BASE_URL = "https://minerbaone.esdm.go.id"

# Common API patterns for pagination
API_PATTERNS = [
    "/api/badan-usaha",
    "/api/publik/badan-usaha",
    "/api/v1/badan-usaha",
    "/api/v1/publik/badan-usaha",
    "/api/companies",
    "/api/public/companies",
    "/api/list/badan-usaha",
]

# Try with different query parameters
PARAMS_TO_TRY = [
    {},
    {"page": 1},
    {"page": 1, "limit": 10},
    {"page": 1, "per_page": 10},
    {"offset": 0, "limit": 10},
]

def probe_api(endpoint: str, params: dict):
    """Test an API endpoint"""
    url = BASE_URL + endpoint
    
    try:
        print(f"\n{'='*60}")
        print(f"Testing: {url}")
        print(f"Params: {params}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Accept': 'application/json',
        }
        
        r = requests.get(url, params=params, headers=headers, timeout=10)
        
        print(f"Status: {r.status_code}")
        
        if r.status_code == 200:
            print(f"✅ SUCCESS!")
            print(f"Content-Type: {r.headers.get('content-type')}")
            print(f"Length: {len(r.text)} chars")
            
            # Try to parse as JSON
            try:
                data = r.json()
                print(f"📊 JSON Response:")
                print(json.dumps(data, indent=2, ensure_ascii=False)[:500])
                
                # Save full response
                with open(f'output/api_response_{endpoint.replace("/", "_")}.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                return True
            except:
                print(f"⚠️  Not JSON, first 200 chars:")
                print(r.text[:200])
        else:
            print(f"❌ Status {r.status_code}")
        
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    print("MinerbaOne API Probe")
    print("="*60)
    
    found_endpoints = []
    
    for endpoint in API_PATTERNS:
        for params in PARAMS_TO_TRY:
            success = probe_api(endpoint, params)
            if success:
                found_endpoints.append((endpoint, params))
                break  # Found working params, move to next endpoint
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    if found_endpoints:
        print(f"✅ Found {len(found_endpoints)} working endpoint(s):")
        for endpoint, params in found_endpoints:
            print(f"   - {endpoint} with {params}")
    else:
        print("❌ No API endpoints found.")
        print("   Will need browser automation.")
    
    print("="*60)


if __name__ == "__main__":
    main()
