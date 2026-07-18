import csv

# First, read company names from details file
company_names = {}
with open('tools/scrapling/output/full/minerbaone_details.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        company_names[row['id_badan_usaha']] = row['nama_badan_usaha']

# Read MinerbaOne permits
sulawesi_keywords = ['SULAWESI', 'GORONTALO']
companies_sulawesi = set()
company_details = {}

with open('tools/scrapling/output/full/minerbaone_permits.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        lokasi = row.get('lokasi_perizinan', '').upper()
        if any(keyword in lokasi for keyword in sulawesi_keywords):
            company_id = row['id_badan_usaha']
            company_name = company_names.get(company_id, f'UNKNOWN_{company_id}')
            companies_sulawesi.add(company_name)
            
            # Store details
            if company_name not in company_details:
                company_details[company_name] = {
                    'id': row['id_badan_usaha'],
                    'lokasi': set(),
                    'komoditas': set(),
                    'count_permits': 0
                }
            
            company_details[company_name]['lokasi'].add(lokasi)
            company_details[company_name]['komoditas'].add(row.get('komoditas', 'N/A'))
            company_details[company_name]['count_permits'] += 1

print(f"="*80)
print(f"COMPANIES DI SULAWESI REGION (FROM MINERBAONE)")
print(f"="*80)
print(f"\nTotal unique companies: {len(companies_sulawesi)}")

# Categorize
nikel_companies = []
non_nikel_companies = []

for company, details in company_details.items():
    komoditas_str = ', '.join(details['komoditas'])
    if 'Nikel' in komoditas_str:
        nikel_companies.append((company, details))
    else:
        non_nikel_companies.append((company, details))

print(f"Companies dengan izin NIKEL: {len(nikel_companies)}")
print(f"Companies non-nikel: {len(non_nikel_companies)}")

print(f"\n{'='*80}")
print(f"TOP 30 COMPANIES WITH NICKEL PERMITS IN SULAWESI")
print(f"{'='*80}")

for i, (company, details) in enumerate(sorted(nikel_companies)[:30], 1):
    komoditas = ', '.join(details['komoditas'])
    lokasi = ', '.join(list(details['lokasi'])[:2])  # Show first 2 locations
    print(f"{i}. {company}")
    print(f"   Permits: {details['count_permits']} | Komoditas: {komoditas}")
    print(f"   Lokasi: {lokasi}")
    print()

if len(nikel_companies) > 30:
    print(f"... dan {len(nikel_companies) - 30} perusahaan nikel lainnya")

# Save to CSV
output_file = 'tools/scrapling/output/sulawesi_nickel_companies.csv'
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['company_name', 'id_badan_usaha', 'total_permits', 'komoditas', 'lokasi'])
    
    for company, details in sorted(nikel_companies):
        writer.writerow([
            company,
            details['id'],
            details['count_permits'],
            '; '.join(details['komoditas']),
            '; '.join(details['lokasi'])
        ])

print(f"\n{'='*80}")
print(f"✅ Company list saved: {output_file}")
print(f"{'='*80}")
