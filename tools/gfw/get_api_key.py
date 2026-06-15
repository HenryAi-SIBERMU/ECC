import requests
import json

BASE = "https://data-api.globalforestwatch.org"

# Login
print("Attempting login...")
login_data = {
    "grant_type": "password",
    "username": "henryai@sibermu.ac.id",
    "password": "@Henry0778365361"
}

try:
    resp = requests.post(
        f"{BASE}/auth/token",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=30
    )
    
    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.text[:500]}")
    
    if resp.status_code == 200:
        data = resp.json()
        # Response structure: {"data": {"access_token": "..."}}
        access_token = data.get("data", {}).get("access_token") or data.get("access_token")
        print(f"\n✅ Login successful!")
        print(f"Access Token: {access_token[:50] if access_token else 'NOT FOUND'}...")
        
        # Create API key
        print("\nCreating API key...")
        api_key_resp = requests.post(
            f"{BASE}/auth/apikey",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            },
            json={
                "alias": "celios-research",
                "organization": "CELIOS",
                "email": "henryai@sibermu.ac.id"
            },
            timeout=30
        )
        
        print(f"Status: {api_key_resp.status_code}")
        
        if api_key_resp.status_code == 200:
            api_data = api_key_resp.json()
            api_key = api_data["data"]["attributes"]["api_key"]
            print(f"\n✅ API KEY CREATED!")
            print("="*60)
            print(api_key)
            print("="*60)
        else:
            print(f"Error: {api_key_resp.text}")
    else:
        print(f"❌ Login failed: {resp.text}")
        
except Exception as e:
    print(f"❌ Error: {e}")
