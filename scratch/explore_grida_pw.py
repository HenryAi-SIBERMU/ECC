import os
import json
from playwright.sync_api import sync_playwright

def run():
    print("Membuka browser untuk melacak API calls dari GRID-Arendal...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Simpan URL API yang dipanggil
        api_endpoints = []
        
        def handle_response(response):
            # Cek apakah respon adalah JSON / CSV
            if response.request.resource_type in ["fetch", "xhr"]:
                url = response.url
                if "json" in url or "api" in url or "csv" in url or "geojson" in url:
                    print(f"[*] Ditemukan data endpoint: {url}")
                    api_endpoints.append(url)
                    
        page.on("response", handle_response)
        
        try:
            page.goto("https://tailing.grida.no/", wait_until="networkidle", timeout=30000)
            page.wait_for_timeout(5000) # Tunggu 5 detik tambahan
        except Exception as e:
            print(f"Error navigating: {e}")
            
        print("\nKesimpulan Endpoint Ditemukan:")
        for ep in api_endpoints:
            print(ep)
            
        browser.close()

if __name__ == '__main__':
    run()
