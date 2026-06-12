#!/usr/bin/env python3
"""
Variable ID Discovery Script
CELIOS ECC Intelligence System

Helper script to find variable IDs for ekspor and PAD data
"""

import sys
import json
from bps_client import BPSClient


def search_tables(client: BPSClient, search_term: str, domain: str = "7300"):
    """
    Search for tables containing specific keywords
    
    Args:
        client: BPSClient instance
        search_term: Keyword to search (e.g., "ekspor", "pad")
        domain: Domain code to search in
    """
    print(f"\n🔍 Searching for '{search_term}' in domain {domain}...")
    
    # Try different pages to find relevant tables
    found_tables = []
    
    for page in range(1, 6):  # Check first 5 pages
        try:
            response = client._make_request("list", params={
                "model": "data",
                "domain": domain,
                "page": page,
                "lang": "ind"
            })
            
            if response and isinstance(response, dict):
                data_content = response.get("datacontent", response.get("data", []))
                
                if not data_content:
                    break
                
                # Search for matching titles
                for item in data_content:
                    title = item.get("title", "").lower()
                    if search_term.lower() in title:
                        found_tables.append({
                            "var_id": item.get("var", item.get("var_id", "N/A")),
                            "title": item.get("title", "N/A"),
                            "subject": item.get("subcat", item.get("subj", "N/A")),
                            "page": page
                        })
                
                print(f"  Page {page}: scanned {len(data_content)} items")
                
        except Exception as e:
            print(f"  ⚠️  Error on page {page}: {e}")
            continue
    
    if found_tables:
        print(f"\n✅ Found {len(found_tables)} matching tables:")
        for i, table in enumerate(found_tables, 1):
            print(f"\n{i}. {table['title']}")
            print(f"   Var ID: {table['var_id']}")
            print(f"   Subject: {table['subject']}")
            print(f"   Page: {table['page']}")
    else:
        print(f"\n❌ No tables found for '{search_term}'")
    
    return found_tables


def main():
    """Main discovery function"""
    print("="*80)
    print("BPS API Variable ID Discovery")
    print("="*80)
    
    # Initialize client
    api_key = "06fd644648629502353deaed29fc6383"
    client = BPSClient(api_key=api_key, verbose=False)
    
    # Test connection
    if not client.test_connection():
        print("❌ Failed to connect to BPS API")
        sys.exit(1)
    
    # Search for ekspor data
    print("\n" + "="*80)
    print("SEARCHING FOR EKSPOR DATA")
    print("="*80)
    ekspor_tables = search_tables(client, "ekspor", domain="7300")  # Sulawesi Selatan
    
    # Search for PAD data
    print("\n" + "="*80)
    print("SEARCHING FOR PAD DATA")
    print("="*80)
    pad_tables = search_tables(client, "pendapatan asli daerah", domain="7300")
    
    # Also search for alternative PAD terms
    if not pad_tables:
        print("\nTrying alternative search: 'PAD'")
        pad_tables = search_tables(client, "pad", domain="7300")
    
    # Save results
    results = {
        "ekspor": ekspor_tables,
        "pad": pad_tables
    }
    
    with open("output/discovered_variables.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print("\n" + "="*80)
    print("✅ Discovery complete! Results saved to output/discovered_variables.json")
    print("="*80)


if __name__ == "__main__":
    main()
