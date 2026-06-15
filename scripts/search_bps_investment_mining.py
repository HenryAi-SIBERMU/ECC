"""
Search BPS API for investment data - mining/pertambangan sector
"""
import sys
sys.path.append('tools/bpsapi')

from bps_client import BPSClient
import json

print("="*80)
print("SEARCHING BPS API FOR MINING INVESTMENT DATA")
print("="*80)

api_key = "06fd644648629502353deaed29fc6383"
client = BPSClient(api_key=api_key, verbose=False)

# Search keywords
keywords = [
    "investasi pertambangan",
    "invest", 
    "tambang",
    "mining",
    "nikel",
    "nickel",
    "PMDN pertambangan",
    "PMA pertambangan"
]

print("\n🔍 Searching national tables (domain 0000)...")
all_tables = []

# Search multiple pages
for page in range(1, 6):  # Check first 5 pages
    print(f"   Page {page}...", end=" ")
    tables = client.list_dynamic_tables(domain="0000", page=page)
    all_tables.extend(tables)
    print(f"{len(tables)} tables")
    
    if len(tables) == 0:
        break

print(f"\n✅ Total tables found: {len(all_tables)}")

# Filter by keywords
print(f"\n🎯 Filtering by keywords: {keywords}")
matched_tables = []

for table in all_tables:
    title = table.get('title', '').lower()
    subcat = table.get('subcat', '').lower()
    
    for keyword in keywords:
        if keyword.lower() in title or keyword.lower() in subcat:
            matched_tables.append(table)
            break

print(f"✅ Matched {len(matched_tables)} relevant tables\n")

print("="*80)
print("RELEVANT TABLES FOR MINING INVESTMENT")
print("="*80)

for i, table in enumerate(matched_tables[:20], 1):  # Show first 20
    print(f"\n{i}. {table.get('title', 'N/A')}")
    print(f"   Var ID: {table.get('var', 'N/A')}")
    print(f"   Subject: {table.get('subcat', 'N/A')}")
    print(f"   Updated: {table.get('turth', 'N/A')}")

if len(matched_tables) > 20:
    print(f"\n... dan {len(matched_tables) - 20} tabel lainnya")

# Try to get SAMPLE DATA from first matched table
if matched_tables:
    print("\n" + "="*80)
    print("SAMPLE DATA FROM FIRST TABLE")
    print("="*80)
    
    first_table = matched_tables[0]
    var_id = first_table.get('var')
    
    print(f"\nFetching data for: {first_table.get('title')}")
    print(f"Var ID: {var_id}")
    
    try:
        sample_data = client.get_dynamic_table(var=var_id, domain="0000")
        
        if sample_data:
            print(f"✅ Found {len(sample_data)} data entries")
            print("\nSample (first 5 entries):")
            for i, entry in enumerate(sample_data[:5], 1):
                print(f"\n{i}. {json.dumps(entry, indent=2, ensure_ascii=False)}")
        else:
            print("❌ No data available for this table")
    
    except Exception as e:
        print(f"❌ Error fetching data: {e}")

# Check Sulawesi provinces
print("\n" + "="*80)
print("CHECKING SULAWESI PROVINCES")
print("="*80)

sulawesi_provinces = [
    ("7100", "Sulawesi Utara"),
    ("7200", "Sulawesi Tengah"),
    ("7300", "Sulawesi Selatan"),
    ("7400", "Sulawesi Tenggara"),
    ("7500", "Gorontalo"),
    ("7600", "Sulawesi Barat")
]

for code, name in sulawesi_provinces:
    print(f"\n📍 {name} (Code: {code})")
    tables = client.list_dynamic_tables(domain=code, page=1)
    print(f"   Total tables available: {len(tables)}")
    
    # Filter for investment
    inv_tables = [t for t in tables if any(k in t.get('title', '').lower() for k in ['invest', 'modal', 'pmdn', 'pma'])]
    if inv_tables:
        print(f"   Investment-related: {len(inv_tables)}")
        for t in inv_tables[:3]:
            print(f"   - {t.get('title', 'N/A')} (Var: {t.get('var', 'N/A')})")

print("\n" + "="*80)
print("✅ SEARCH COMPLETE")
print("="*80)
