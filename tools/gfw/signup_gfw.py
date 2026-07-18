"""
GFW API Sign Up & API Key Generation Script
============================================

Script untuk register akun GFW dan generate API key.

Usage:
    python signup_gfw.py

Author: CELIOS Research Division
Date: 14 Juni 2026
"""

import requests
import json
import sys

BASE_URL = "https://data-api.globalforestwatch.org"

def sign_up(name: str, email: str):
    """
    Register new user di GFW API.
    
    Args:
        name: Full name
        email: Email address
    
    Returns:
        Dict with access token atau error message
    """
    endpoint = f"{BASE_URL}/auth/sign-up"
    
    payload = {
        "name": name,
        "email": email
    }
    
    print("=" * 70)
    print("GFW API SIGN UP")
    print("=" * 70)
    print(f"Name: {name}")
    print(f"Email: {email}")
    print(f"Endpoint: {endpoint}")
    print("\nSending request...")
    
    try:
        response = requests.post(
            endpoint,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ SIGN UP SUCCESSFUL!")
            print("\nResponse:")
            print(json.dumps(data, indent=2))
            return data
        else:
            print(f"\n❌ SIGN UP FAILED!")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return None


def create_api_key(access_token: str, alias: str = "celios-deforestation"):
    """
    Create API key menggunakan access token.
    
    Args:
        access_token: Bearer token dari sign up
        alias: Alias untuk API key
    
    Returns:
        Dict dengan API key info
    """
    endpoint = f"{BASE_URL}/auth/apikey"
    
    payload = {
        "alias": alias,
        "organization": "CELIOS Research",
        "email": "research@celios.org"
    }
    
    print("\n" + "=" * 70)
    print("CREATING API KEY")
    print("=" * 70)
    print(f"Alias: {alias}")
    print(f"Endpoint: {endpoint}")
    print("\nSending request...")
    
    try:
        response = requests.post(
            endpoint,
            json=payload,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            },
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ API KEY CREATED!")
            print("\n🔑 YOUR API KEY:")
            print("=" * 70)
            
            if 'data' in data and 'attributes' in data['data']:
                api_key = data['data']['attributes'].get('api_key', 'NOT FOUND')
                print(f"\n{api_key}\n")
                print("=" * 70)
                print("\n📝 SAVE THIS API KEY!")
                print("This key is valid for 1 year.")
                print("\nTo use in scripts:")
                print(f"  export GFW_API_KEY='{api_key}'")
                print(f"  # or in Python:")
                print(f"  api_key = '{api_key}'")
            else:
                print(json.dumps(data, indent=2))
            
            return data
        else:
            print(f"\n❌ API KEY CREATION FAILED!")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return None


def login(email: str, password: str):
    """
    Login untuk mendapatkan access token.
    
    Args:
        email: Email address
        password: Password
    
    Returns:
        Dict with access token
    """
    endpoint = f"{BASE_URL}/auth/token"
    
    payload = {
        "grant_type": "password",
        "username": email,
        "password": password
    }
    
    print("=" * 70)
    print("GFW API LOGIN")
    print("=" * 70)
    print(f"Email: {email}")
    print(f"Endpoint: {endpoint}")
    print("\nSending request...")
    
    try:
        response = requests.post(
            endpoint,
            data=payload,  # Note: form-urlencoded, not JSON
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ LOGIN SUCCESSFUL!")
            return data
        else:
            print(f"\n❌ LOGIN FAILED!")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return None


def main():
    """Main execution."""
    print("\n" + "=" * 70)
    print("GFW API REGISTRATION WIZARD")
    print("=" * 70)
    
    # Ask: signup or login?
    print("\n[1] Sign Up (new account)")
    print("[2] Login (existing account)")
    print("[3] I already have API key")
    
    choice = input("\nPilih (1/2/3): ").strip()
    
    access_token = None
    
    if choice == "1":
        # Sign up
        print("\nMasukkan informasi untuk sign up:")
        name = input("Full Name: ").strip()
        email = input("Email: ").strip()
        
        if not name or not email:
            print("\n❌ Name dan email tidak boleh kosong!")
            sys.exit(1)
        
        result = sign_up(name, email)
        
        if result and 'access_token' in result:
            access_token = result['access_token']
        
    elif choice == "2":
        # Login
        print("\nMasukkan credentials:")
        email = input("Email: ").strip()
        password = input("Password: ").strip()
        
        if not email or not password:
            print("\n❌ Email dan password tidak boleh kosong!")
            sys.exit(1)
        
        result = login(email, password)
        
        if result and 'access_token' in result:
            access_token = result['access_token']
    
    elif choice == "3":
        # Already have API key
        api_key = input("Paste your API key: ").strip()
        
        if api_key:
            print("\n✅ API key received!")
            print(f"\nSave this to .env file:")
            print(f"GFW_API_KEY={api_key}")
            
            # Test API key
            print("\nTesting API key...")
            test_endpoint = f"{BASE_URL}/dataset/umd_tree_cover_loss/latest/fields"
            test_resp = requests.get(test_endpoint, headers={"x-api-key": api_key}, timeout=30)
            
            if test_resp.status_code == 200:
                print("✅ API key valid!")
            else:
                print(f"⚠️ API key test failed: {test_resp.status_code}")
        
        sys.exit(0)
    
    else:
        print("\n❌ Invalid choice!")
        sys.exit(1)
    
    # If no token yet, ask manually
    if not access_token:
        print("\n⚠️ Access token tidak ditemukan.")
        print("Apakah kamu sudah punya access token? (y/n)")
        has_token = input().strip().lower()
        
        if has_token == 'y':
            access_token = input("Paste access token: ").strip()
        else:
            print("\n❌ Cannot proceed without access token.")
            sys.exit(1)
    
    result = None
    # Create API key
    if access_token:
        api_key_result = create_api_key(access_token)
        
        if api_key_result:
            print("\n✅ SETUP COMPLETE!")
            print("API key sudah siap digunakan untuk fetch data deforestasi.")
        else:
            print("\n❌ Failed to create API key.")
            print("Kamu bisa coba manual via:")
            print(f"  curl -X POST {BASE_URL}/auth/apikey \\")
            print(f"    -H 'Authorization: Bearer {access_token}' \\")
            print("    -H 'Content-Type: application/json' \\")
            print("    -d '{\"alias\":\"celios-research\"}'")


if __name__ == "__main__":
    main()
