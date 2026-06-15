import csv

# Read MinerbaOne details
companies = set()
sulawesi_provinces = ['Sulawesi Utara', 'Sulawesi Tengah', 'Sulawesi Selatan', 
                      'Sulawesi Tenggara', 'Sulawesi Barat', 'Gorontalo']

with open('tools/scrapling/output/full/minerbaone_details.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        prov = row.get('provinsi', '')
        if any(sulprov in prov for sulprov in sulawesi_provinces):
            companies.add(row['nama_perusahaan'])

print(f"Total unique companies di Sulawesi region: {len(companies)}")
print(f"\nSample 30 companies:")
for i, company in enumerate(sorted(companies)[:30], 1):
    print(f"{i}. {company}")

print(f"\n... dan {len(companies) - 30} lainnya")
