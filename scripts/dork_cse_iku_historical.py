#!/usr/bin/env python3
"""
Google Custom Search Engine (CSE) Dorking untuk SLHI 2014-2018
Menggunakan Google CSE API untuk comprehensive search
"""

import os
import json
import time
from pathlib import Path
from dotenv import load_dotenv
import requests

# Load API credentials
load_dotenv()
API_KEY = os.getenv('GOOGLE_API_KEY')
CSE_ID = os.getenv('GOOGLE_CSE_ID')

if not API_KEY or not CSE_ID:
    print("❌ ERROR: GOOGLE_API_KEY atau GOOGLE_CSE_ID tidak ditemukan di .env")
    print("   Tambahkan ke file .env:")
    print("   GOOGLE_API_KEY=your_api_key")
    print("   GOOGLE_CSE_ID=your_cse_id")
    exit(1)

print("="*80)
print("🔍 Google CSE Dorking - SLHI 2014-2018 Historical Data")
print("="*80)
print(f"✅ API Key: {API_KEY[:20]}...")
print(f"✅ CSE ID: {CSE_ID}")

# Priority queries - Focus on 2014-2018
queries = [
    # Tier 1: Exact SLHI match
    '"Status Lingkungan Hidup Indonesia 2014" filetype:pdf',
    '"Status Lingkungan Hidup Indonesia 2015" filetype:pdf',
    '"Status Lingkungan Hidup Indonesia 2016" filetype:pdf',
    '"Status Lingkungan Hidup Indonesia 2017" filetype:pdf',
    '"Status Lingkungan Hidup Indonesia 2018" filetype:pdf',
    
    # Tier 2: SLHI abbreviation
    '"SLHI 2014" filetype:pdf',
    '"SLHI 2015" filetype:pdf',
    '"SLHI 2016" filetype:pdf',
    '"SLHI 2017" filetype:pdf',
    '"SLHI 2018" filetype:pdf',
    
    # Tier 3: BPS domain specific
    'site:bps.go.id "SLHI" 2014 filetype:pdf',
    'site:bps.go.id "SLHI" 2015 filetype:pdf',
    'site:bps.go.id "SLHI" 2016 filetype:pdf',
    'site:bps.go.id "SLHI" 2017 filetype:pdf',
    'site:bps.go.id "SLHI" 2018 filetype:pdf',
    
    # Tier 4: Alternative naming
    '"statistik lingkungan hidup indonesia" 2014 filetype:pdf',
    '"statistik lingkungan hidup indonesia" 2015 filetype:pdf',
    '"statistik lingkungan hidup indonesia" 2016 filetype:pdf',
    
    # Tier 5: KLHK domain
    'site:menlhk.go.id "SLHI" 2014..2018 filetype:pdf',
    'site:kemenlh.go.id "lingkungan hidup" 2014..2018 filetype:pdf',
    
    # Tier 6: IKU specific
    '"indeks kualitas udara" "sulawesi" 2014..2018 site:bps.go.id',
    '"IKU" provinsi 2014..2018 filetype:xlsx',
    
    # Tier 7: Provincial BPS
    'site:sulutprov.bps.go.id "lingkungan" 2014..2018',
    'site:sulsel.bps.go.id "lingkungan" 2014..2018',
    
    # Tier 8: Archive.org
    'site:web.archive.org "bps.go.id" "SLHI 2014"',
    'site:web.archive.org "bps.go.id" "SLHI 2015"',
    'site:web.archive.org "bps.go.id" "SLHI 2016"',
    
    # Tier 9: Third party hosts
    'site:issuu.com "lingkungan hidup indonesia" 2014',
    'site:issuu.com "lingkungan hidup indonesia" 2015',
]

def search_cse(query, start=1):
    """
    Search using Google Custom Search Engine API
    Returns: dict with search results
    """
    url = "https://www.googleapis.com/customsearch/v1"
    
    params = {
        'key': API_KEY,
        'cx': CSE_ID,
        'q': query,
        'start': start,
        'num': 10  # Max 10 per request
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"   ⚠️  Error: {str(e)}")
        return None

# Create output directory
output_dir = Path('docs/cse_dorking_results')
output_dir.mkdir(exist_ok=True)

all_results = []
pdf_links = []
unique_urls = set()

print(f"\n🚀 Executing {len(queries)} queries...")
print(f"⏱️  Rate limit: 1 query per second")
print(f"📊 Fetching 10 results per query\n")

for idx, query in enumerate(queries, 1):
    print(f"[{idx}/{len(queries)}] {query[:65]}...")
    
    data = search_cse(query)
    
    if data and 'items' in data:
        results = data['items']
        print(f"   ✅ Found {len(results)} results")
        
        for item in results:
            url = item.get('link', '')
            title = item.get('title', 'No title')
            snippet = item.get('snippet', 'No snippet')
            
            # Skip duplicates
            if url in unique_urls:
                continue
            unique_urls.add(url)
            
            result_entry = {
                'query': query,
                'title': title,
                'url': url,
                'snippet': snippet,
                'displayLink': item.get('displayLink', ''),
                'fileFormat': item.get('fileFormat', '')
            }
            
            all_results.append(result_entry)
            
            # Track PDFs
            if '.pdf' in url.lower() or item.get('fileFormat') == 'PDF':
                pdf_links.append(url)
        
        # Save per-query results
        query_file = output_dir / f"query_{idx:02d}.json"
        with open(query_file, 'w', encoding='utf-8') as f:
            json.dump({
                'query': query,
                'results': results,
                'count': len(results)
            }, f, indent=2, ensure_ascii=False)
    
    elif data and 'error' in data:
        error = data['error']
        print(f"   ❌ API Error: {error.get('message', 'Unknown error')}")
        if error.get('code') == 429:
            print(f"   ⚠️  Rate limit exceeded. Sleeping 60s...")
            time.sleep(60)
    else:
        print(f"   ℹ️  No results")
    
    # Rate limiting - 1 query per second (free tier limit)
    if idx < len(queries):
        time.sleep(1.1)

print("\n" + "="*80)
print(f"✅ Dorking complete!")
print(f"📊 Total unique results: {len(all_results)}")
print(f"📄 PDF results: {len(pdf_links)}")

# Save all results
all_results_file = output_dir / "all_results.json"
with open(all_results_file, 'w', encoding='utf-8') as f:
    json.dump(all_results, f, indent=2, ensure_ascii=False)

print(f"💾 All results: {all_results_file}")

# Save PDF links
if pdf_links:
    pdf_file = output_dir / "pdf_links.txt"
    with open(pdf_file, 'w', encoding='utf-8') as f:
        for link in pdf_links:
            f.write(f"{link}\n")
    
    print(f"💾 PDF links: {pdf_file}")
    
    print(f"\n🎯 Top 10 PDF Results:")
    for i, link in enumerate(pdf_links[:10], 1):
        print(f"   {i}. {link}")
    
    # Create download script
    download_script = output_dir / "download_pdfs.bat"
    with open(download_script, 'w', encoding='utf-8') as f:
        f.write("@echo off\n")
        f.write("echo Downloading SLHI PDFs...\n")
        f.write("mkdir data\\raw\\slhi_historical 2>nul\n")
        f.write("cd data\\raw\\slhi_historical\n\n")
        for link in pdf_links:
            filename = link.split('/')[-1]
            if not filename.endswith('.pdf'):
                filename = f"slhi_{filename}.pdf"
            f.write(f'curl -L -o "{filename}" "{link}"\n')
        f.write("\necho Done!\n")
        f.write("pause\n")
    
    print(f"💾 Download script: {download_script}")

# Summary by domain
domains = {}
for r in all_results:
    domain = r.get('displayLink', 'unknown')
    domains[domain] = domains.get(domain, 0) + 1

if domains:
    print(f"\n🌐 Results by domain:")
    for domain, count in sorted(domains.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"   {domain}: {count} results")

# Check for SLHI specific results
slhi_results = [r for r in all_results if 'slhi' in r['title'].lower() or 'slhi' in r['url'].lower()]
if slhi_results:
    print(f"\n🎯 SLHI-specific results: {len(slhi_results)}")
    for r in slhi_results[:5]:
        print(f"   📄 {r['title'][:60]}")
        print(f"      {r['url']}")

print("\n" + "="*80)
print("✅ NEXT STEPS:")
print("   1. Review results in docs/cse_dorking_results/")
print("   2. Run download_pdfs.bat to download PDFs")
print("   3. Extract IKU data with pdfplumber")
print("="*80)
