#!/usr/bin/env python3
"""
Google Dorking dengan Scrapling untuk mencari SLHI 2014-2016
Alternative to Google CSE API - menggunakan web scraping
"""

import time
import json
from pathlib import Path
from urllib.parse import quote_plus

print("="*70)
print("🔍 Google Dorking with Scrapling - SLHI 2014-2016")
print("="*70)

# Check if scrapling is installed
try:
    from scrapling import Fetcher
    print("✅ Scrapling found")
except ImportError:
    print("❌ Scrapling not installed")
    print("   Installing scrapling...")
    import subprocess
    subprocess.run(["pip", "install", "scrapling"], check=True)
    from scrapling import Fetcher
    print("✅ Scrapling installed")

# Priority queries - Top 20 most likely to find SLHI
queries = [
    # Tier 1: Exact match
    '"Status Lingkungan Hidup Indonesia 2014" filetype:pdf',
    '"Status Lingkungan Hidup Indonesia 2015" filetype:pdf',
    '"Status Lingkungan Hidup Indonesia 2016" filetype:pdf',
    '"SLHI 2014" filetype:pdf',
    '"SLHI 2015" filetype:pdf',
    '"SLHI 2016" filetype:pdf',
    
    # Tier 2: BPS domain
    'site:bps.go.id "SLHI 2014" filetype:pdf',
    'site:bps.go.id "SLHI 2015" filetype:pdf',
    'site:bps.go.id "SLHI 2016" filetype:pdf',
    
    # Tier 3: Alternative names
    '"statistik lingkungan hidup indonesia" 2014 filetype:pdf',
    '"statistik lingkungan hidup indonesia" 2015 filetype:pdf',
    '"statistik lingkungan hidup indonesia" 2016 filetype:pdf',
    
    # Tier 4: Publication pattern
    'site:bps.go.id "lingkungan hidup" 2014 filetype:pdf',
    'site:bps.go.id "lingkungan hidup" 2015 filetype:pdf',
    'site:bps.go.id "lingkungan hidup" 2016 filetype:pdf',
    
    # Tier 5: Third party hosts
    'site:issuu.com "lingkungan hidup indonesia" 2014',
    'site:issuu.com "lingkungan hidup indonesia" 2015',
    'site:issuu.com "lingkungan hidup indonesia" 2016',
    
    # Tier 6: Archive
    'site:web.archive.org "bps.go.id" "SLHI 2014"',
    'site:web.archive.org "bps.go.id" "SLHI 2015"',
]

output_dir = Path('docs/dorking_results')
output_dir.mkdir(exist_ok=True)

results_all = []

print(f"\n📝 Executing {len(queries)} queries...")
print(f"⏱️  Delay 3s between requests to avoid rate limiting\n")

for idx, query in enumerate(queries, 1):
    print(f"[{idx}/{len(queries)}] {query[:60]}...")
    
    try:
        # Build Google search URL
        search_url = f"https://www.google.com/search?q={quote_plus(query)}&num=20"
        
        # Fetch with Scrapling
        page = Fetcher.get(search_url)
        
        # Parse results
        search_results = []
        
        # Try to find search result divs (Google structure)
        result_divs = page.css('div.g')
        
        for result in result_divs:
            try:
                # Extract title
                title_elem = result.css_first('h3')
                title = title_elem.text if title_elem else 'No title'
                
                # Extract link
                link_elem = result.css_first('a')
                link = link_elem.attrib.get('href', '') if link_elem else ''
                
                # Extract snippet
                snippet_elem = result.css_first('div.VwiC3b, span.aCOpRe')
                snippet = snippet_elem.text if snippet_elem else 'No snippet'
                
                if link and 'http' in link:
                    search_results.append({
                        'title': title,
                        'url': link,
                        'snippet': snippet,
                        'query': query
                    })
            except Exception as e:
                continue
        
        if search_results:
            print(f"   ✅ Found {len(search_results)} results")
            results_all.extend(search_results)
            
            # Save per query
            query_file = output_dir / f"query_{idx:02d}.json"
            with open(query_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'query': query,
                    'results': search_results,
                    'count': len(search_results)
                }, f, indent=2, ensure_ascii=False)
        else:
            print(f"   ℹ️  No results")
        
        # Delay to avoid rate limiting
        if idx < len(queries):
            time.sleep(3)
    
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        continue

print("\n" + "="*70)
print(f"✅ Dorking complete!")
print(f"📊 Total results: {len(results_all)}")

# Save all results
output_file = output_dir / "all_results.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(results_all, f, indent=2, ensure_ascii=False)

print(f"💾 Saved to: {output_file}")

# Filter PDF results
pdf_results = [r for r in results_all if '.pdf' in r['url'].lower() or 'pdf' in r['title'].lower()]

if pdf_results:
    print(f"\n🎯 Found {len(pdf_results)} PDF results:")
    
    for r in pdf_results[:10]:  # Show top 10
        print(f"\n   📄 {r['title'][:60]}")
        print(f"      {r['url']}")
    
    # Save PDF list
    pdf_file = output_dir / "pdf_links.txt"
    with open(pdf_file, 'w', encoding='utf-8') as f:
        for r in pdf_results:
            f.write(f"{r['url']}\n")
    
    print(f"\n💾 PDF links saved to: {pdf_file}")
    print(f"\n📥 Download with:")
    print(f"   wget -i {pdf_file} -P data/raw/slhi_historical/")
else:
    print(f"\n⚠️  No PDF results found")

# Unique domains found
domains = {}
for r in results_all:
    from urllib.parse import urlparse
    domain = urlparse(r['url']).netloc
    if domain:
        domains[domain] = domains.get(domain, 0) + 1

if domains:
    print(f"\n🌐 Domains found:")
    for domain, count in sorted(domains.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"   {domain}: {count} results")

print("\n" + "="*70)
print("✅ NEXT STEPS:")
print("   1. Review results in docs/dorking_results/")
print("   2. Download PDFs from pdf_links.txt")
print("   3. Extract IKU data with pdfplumber")
print("="*70)
