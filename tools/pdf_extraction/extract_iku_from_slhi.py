#!/usr/bin/env python3
"""
Ekstrak data IKU (Indeks Kualitas Udara) dari PDF SLHI
Target: Halaman yang mengandung data kualitas udara untuk Sulawesi
"""

import PyPDF2
from pathlib import Path

slhi_dir = Path("data/raw/sulut_kualitas_air")
output_dir = Path("data/raw/slhi_extracted")
output_dir.mkdir(parents=True, exist_ok=True)

slhi_files = sorted(slhi_dir.glob("SLHI_*.pdf"))

print("="*70)
print("📄 Ekstraksi Data IKU dari SLHI PDFs")
print("="*70)

keywords = ['kualitas udara', 'iku', 'pm2.5', 'pm10', 'indeks standar', 'sulawesi']

for pdf_path in slhi_files:
    year = pdf_path.stem.split("_")[1]
    print(f"\n📖 Processing: {pdf_path.name} (Tahun {year})")
    
    try:
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            total_pages = len(reader.pages)
            print(f"   Total pages: {total_pages}")
            
            # Find relevant pages
            relevant_pages = []
            for i in range(total_pages):
                text = reader.pages[i].extract_text().lower()
                
                # Check for keywords
                matches = [kw for kw in keywords if kw in text]
                
                # Priority: pages with IKU + Sulawesi
                if 'iku' in text and 'sulawesi' in text:
                    relevant_pages.append({
                        'page': i+1,
                        'priority': 'HIGH',
                        'matches': matches,
                        'text': reader.pages[i].extract_text()
                    })
                elif len(matches) >= 2:
                    relevant_pages.append({
                        'page': i+1,
                        'priority': 'MEDIUM',
                        'matches': matches,
                        'text': reader.pages[i].extract_text()
                    })
            
            if relevant_pages:
                print(f"   ✅ Found {len(relevant_pages)} relevant pages")
                
                # Save to text file
                output_file = output_dir / f"SLHI_{year}_IKU_extracted.txt"
                with open(output_file, 'w', encoding='utf-8') as out:
                    out.write(f"SLHI {year} - Ekstraksi Data Kualitas Udara\n")
                    out.write("="*70 + "\n\n")
                    
                    for page_info in sorted(relevant_pages, key=lambda x: (x['priority'] == 'MEDIUM', x['page'])):
                        out.write(f"\n{'='*70}\n")
                        out.write(f"Page {page_info['page']} [{page_info['priority']}]\n")
                        out.write(f"Matches: {', '.join(page_info['matches'])}\n")
                        out.write(f"{'='*70}\n\n")
                        out.write(page_info['text'])
                        out.write("\n\n")
                
                print(f"   💾 Saved to: {output_file}")
                
                # Show preview of HIGH priority pages
                high_priority = [p for p in relevant_pages if p['priority'] == 'HIGH']
                if high_priority:
                    print(f"   🎯 HIGH priority pages (IKU + Sulawesi): {[p['page'] for p in high_priority]}")
            else:
                print(f"   ℹ️  No relevant pages found")
    
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

print("\n" + "="*70)
print("✅ Ekstraksi selesai. Cek folder: data/raw/slhi_extracted/")
print("="*70)
