import csv

print("Reading MinerbaOne permits...")

sulawesi_permits = []
with open('tools/scrapling/output/full/minerbaone_permits.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    print(f"Columns: {header}\n")
    
    # Find column indices (strip BOM)
    header = [h.lstrip('\ufeff') for h in header]
    idx_id = header.index('id_badan_usaha')
    idx_lokasi = header.index('lokasi_perizinan')
    idx_komoditas = header.index('komoditas')
    
    for row in reader:
        lokasi = row[idx_lokasi].upper()
        komoditas = row[idx_komoditas]
        
        if ('SULAWESI' in lokasi or 'GORONTALO' in lokasi) and 'Nikel' in komoditas:
            sulawesi_permits.append({
                'id_badan_usaha': row[idx_id],
                'lokasi': row[idx_lokasi],
                'komoditas': komoditas
            })

print(f"Found {len(sulawesi_permits)} nickel permits in Sulawesi\n")

# Get unique company IDs
unique_companies = set([p['id_badan_usaha'] for p in sulawesi_permits])
print(f"Unique company IDs: {len(unique_companies)}\n")

# Now read company details
print("Reading company names...")
company_map = {}
with open('tools/scrapling/output/full/minerbaone_details.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    header = [h.lstrip('\ufeff') for h in header]  # Strip BOM
    
    idx_id = header.index('id_badan_usaha')
    idx_name = header.index('nama_badan_usaha')
    
    for row in reader:
        company_map[row[idx_id]] = row[idx_name]

print(f"Total companies in database: {len(company_map)}\n")

# Match
print("="*80)
print("SULAWESI NICKEL COMPANIES FROM MINERBAONE")
print("="*80)

matched_companies = []
for company_id in unique_companies:
    if company_id in company_map:
        matched_companies.append(company_map[company_id])

print(f"\nTotal matched: {len(matched_companies)}")
print(f"\nCompanies list (first 40):")
for i, name in enumerate(sorted(matched_companies)[:40], 1):
    print(f"{i}. {name}")

if len(matched_companies) > 40:
    print(f"\n... dan {len(matched_companies) - 40} lainnya")

# Save
output = 'tools/scrapling/output/sulawesi_nickel_companies_list.txt'
with open(output, 'w', encoding='utf-8') as f:
    for name in sorted(matched_companies):
        f.write(f"{name}\n")

print(f"\n✅ Saved to: {output}")
