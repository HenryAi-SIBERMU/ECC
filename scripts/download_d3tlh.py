import os
import requests
from bs4 import BeautifulSoup
import sys

def download_d3tlh_pdf():
    output_dir = os.path.join("data", "raw", "D3TLH")
    os.makedirs(output_dir, exist_ok=True)
    
    print("Mencari via DuckDuckGo...")
    try:
        search_url = "https://html.duckduckgo.com/html/?q=filetype:pdf+Peraturan+Menteri+Lingkungan+Hidup+Nomor+17+Tahun+2009+Daya+Dukung"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        resp = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        for a in soup.find_all('a', class_='result__url'):
            link = a.get('href')
            if link and link.endswith('.pdf'):
                print(f"Menemukan PDF: {link}")
                if link.startswith('//'):
                    link = 'https:' + link
                
                try:
                    pdf_resp = requests.get(link, headers=headers, timeout=20)
                    if pdf_resp.status_code == 200:
                        filepath = os.path.join(output_dir, "PermenLH_17_2009_Pedoman_D3TLH.pdf")
                        with open(filepath, 'wb') as f:
                            f.write(pdf_resp.content)
                        print(f"BERHASIL didownload: {filepath}")
                        sys.exit(0)
                except Exception as e:
                    print(f"Gagal download dari link: {e}")
    except Exception as e:
        print(f"Pencarian gagal: {e}")
        
    print("Semua usaha download gagal.")

if __name__ == "__main__":
    download_d3tlh_pdf()
