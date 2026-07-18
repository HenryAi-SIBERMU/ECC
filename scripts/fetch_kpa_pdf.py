import os
import sys
import subprocess
from pathlib import Path
import time

# Pastikan direktori data/raw ada
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / 'data' / 'raw'
os.makedirs(RAW_DIR, exist_ok=True)

print("Memeriksa dependensi Scrapling...")
try:
    from scrapling import StealthyFetcher
except ImportError:
    print("Scrapling belum terinstall. Menginstall sekarang (ini hanya butuh beberapa detik)...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "scrapling", "lxml"])
    from scrapling import StealthyFetcher

def scrape_kpa_reports():
    print("\n[+] Menginisiasi StealthyFetcher untuk menembus proteksi Anti-Bot KPA...")
    # StealthyFetcher secara otomatis meniru browser asli (Chrome/Playwright)
    fetcher = StealthyFetcher()
    
    url = "https://www.kpa.or.id/publikasi/laporan-tahunan/"
    print(f"[+] Menghubungi URL: {url}")
    
    try:
        # Fetch halaman dengan proteksi
        page = fetcher.get(url)
        
        print("\n[+] Berhasil menembus WAF (Web Application Firewall)!")
        print("[+] Mengekstrak daftar laporan...")
        
        # Cari semua elemen <a>
        links = page.css("a")
        
        report_links = []
        for link in links:
            href = link.attrib.get("href", "")
            text = link.text.strip()
            
            if href and ("catahu" in href.lower() or "catatan-akhir-tahun" in href.lower() or "laporan-tahunan" in href.lower() or "pdf" in href.lower()):
                if text:
                    report_links.append({"judul": text, "url": href})
        
        print(f"\n✅ Ditemukan {len(report_links)} kandidat link Laporan CATAHU KPA:")
        for idx, item in enumerate(report_links[:15], 1):
            print(f"{idx}. {item['judul']} -> {item['url']}")
            
        if not report_links:
            print("❌ Tidak ada link CATAHU yang ditemukan. Coba simpan HTML untuk di-debug.")
            with open(RAW_DIR / "debug_kpa.html", "w", encoding="utf-8") as f:
                f.write(page.text)
            
    except Exception as e:
        print(f"❌ Gagal melakukan scraping: {e}")

if __name__ == "__main__":
    scrape_kpa_reports()
