"""
VALIDATOR: OSINT Sources URLs (Python Simple Version)
======================================================
Validasi semua URL di metadata JSON tanpa Puppeteer
Cek HTTP status codes untuk semua sources
"""

import json
import requests
from pathlib import Path
from datetime import datetime
import time

# Configuration
JSON_FILES = [
    'data/raw/osint_logistik_pelabuhan/sources_card1_25_sumber.json',
    'data/raw/osint_logistik_pelabuhan/sources_card2_perpres_kppip.json',
    'data/raw/osint_logistik_pelabuhan/sources_card3_gni_website.json'
]

OUTPUT_REPORT = 'data/raw/osint_logistik_pelabuhan/URL_VALIDATION_REPORT.json'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def check_url(url, timeout=10):
    """Check if URL is accessible"""
    try:
        response = requests.head(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        return {
            'url': url,
            'status': response.status_code,
            'accessible': 200 <= response.status_code < 400,
            'redirected': len(response.history) > 0,
            'final_url': response.url if response.history else url,
            'error': None
        }
    except requests.exceptions.Timeout:
        return {
            'url': url,
            'status': None,
            'accessible': False,
            'error': 'TIMEOUT'
        }
    except requests.exceptions.ConnectionError:
        return {
            'url': url,
            'status': None,
            'accessible': False,
            'error': 'CONNECTION_ERROR'
        }
    except Exception as e:
        return {
            'url': url,
            'status': None,
            'accessible': False,
            'error': str(e)
        }

def validate_json_file(json_path):
    """Validate all URLs in a JSON file"""
    print(f"\n📄 Validating: {json_path}")
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    sources = data.get('sources', [])
    results = []
    
    for source in sources:
        source_id = source.get('id')
        org = source.get('organization') or source.get('document_title', 'Unknown')
        main_url = source.get('url')
        alt_url = source.get('alternative_url')
        archived_url = source.get('archived_url')
        
        print(f"  [{source_id}] Checking {org}...")
        
        # Check main URL
        main_result = check_url(main_url)
        status_icon = '✅' if main_result['accessible'] else '❌'
        print(f"    ├─ Main URL: {status_icon} ({main_result['status'] or main_result['error']})")
        
        # Check alternative URL
        alt_result = None
        if alt_url and alt_url != main_url:
            alt_result = check_url(alt_url)
            status_icon = '✅' if alt_result['accessible'] else '❌'
            print(f"    ├─ Alt URL: {status_icon} ({alt_result['status'] or alt_result['error']})")
        
        # Check archived URL if main is down
        archive_result = None
        if not main_result['accessible'] and archived_url:
            # Skip generic archive.org patterns
            if 'web.archive.org/web/*' in archived_url or 'Manual download' in archived_url:
                print(f"    └─ Archive URL: ⏭️  SKIPPED (generic or manual)")
            else:
                archive_result = check_url(archived_url)
                status_icon = '✅' if archive_result['accessible'] else '❌'
                print(f"    └─ Archive URL: {status_icon} ({archive_result['status'] or archive_result['error']})")
        
        # Recommendation
        recommendation = get_recommendation(main_result, alt_result, archive_result)
        
        results.append({
            'source_id': source_id,
            'organization': org,
            'main_url': main_result,
            'alternative_url': alt_result,
            'archived_url': archive_result,
            'recommendation': recommendation
        })
        
        # Rate limiting
        time.sleep(0.5)
    
    return {
        'file': json_path,
        'total_sources': len(sources),
        'results': results
    }

def get_recommendation(main, alt, archive):
    """Generate recommendation based on results"""
    if main['accessible']:
        return "✅ URL utama masih aktif"
    elif alt and alt['accessible']:
        return "⚠️  URL utama mati, gunakan URL alternatif"
    elif archive and archive['accessible']:
        return "⚠️  URL utama & alternatif mati, gunakan archive"
    else:
        return "❌ SEMUA URL MATI - Perlu dorking ulang atau ganti sumber"

def main():
    print('🚀 Starting OSINT Sources Validation...\n')
    print('=' * 60)
    
    all_results = []
    
    for json_file in JSON_FILES:
        try:
            result = validate_json_file(json_file)
            all_results.append(result)
        except Exception as e:
            print(f"❌ Error processing {json_file}: {e}")
            all_results.append({
                'file': json_file,
                'error': str(e)
            })
    
    # Generate summary
    print('\n' + '=' * 60)
    print('📊 VALIDATION SUMMARY\n')
    
    total_sources = 0
    accessible_sources = 0
    dead_sources = 0
    dead_list = []
    
    for file_result in all_results:
        if 'results' in file_result:
            print(f"\n📁 {Path(file_result['file']).name}")
            print(f"   Total sources: {file_result['total_sources']}")
            
            file_accessible = 0
            file_dead = 0
            
            for r in file_result['results']:
                total_sources += 1
                is_accessible = (r['main_url']['accessible'] or 
                               (r['alternative_url'] and r['alternative_url']['accessible']))
                
                if is_accessible:
                    accessible_sources += 1
                    file_accessible += 1
                else:
                    dead_sources += 1
                    file_dead += 1
                    dead_list.append({
                        'file': Path(file_result['file']).name,
                        'id': r['source_id'],
                        'org': r['organization'],
                        'recommendation': r['recommendation']
                    })
            
            print(f"   ✅ Accessible: {file_accessible}")
            print(f"   ❌ Dead: {file_dead}")
    
    print('\n' + '=' * 60)
    print(f"✅ Accessible: {accessible_sources}/{total_sources} ({accessible_sources/total_sources*100:.1f}%)")
    print(f"❌ Dead Links: {dead_sources}/{total_sources} ({dead_sources/total_sources*100:.1f}%)")
    print('=' * 60)
    
    if dead_list:
        print('\n🔴 DEAD SOURCES DETAIL:\n')
        for dead in dead_list:
            print(f"  [{dead['file']}] ID {dead['id']}: {dead['org']}")
            print(f"    → {dead['recommendation']}\n")
    
    # Save report
    report = {
        'validation_date': datetime.now().isoformat(),
        'summary': {
            'total_sources': total_sources,
            'accessible': accessible_sources,
            'dead': dead_sources,
            'success_rate': f"{accessible_sources/total_sources*100:.2f}%"
        },
        'dead_sources': dead_list,
        'files': all_results
    }
    
    with open(OUTPUT_REPORT, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Report saved: {OUTPUT_REPORT}\n")
    
    # Exit with error if too many dead links
    if dead_sources / total_sources > 0.5:
        print("⚠️  WARNING: More than 50% sources are dead!")
        print("   → Perlu dorking ulang untuk update sumber\n")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())
