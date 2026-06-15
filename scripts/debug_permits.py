import csv

with open('tools/scrapling/output/full/minerbaone_permits.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    
    count = 0
    for row in reader:
        lokasi = row.get('lokasi_perizinan', '')
        if count < 20:  # Show first 20 rows
            print(f"{lokasi} | {row.get('komoditas', '')}")
            count += 1
        
        # Check for Sulawesi
        if count == 20:
            print("\nSearching for Sulawesi...")
            
        if 'SULAWESI' in lokasi.upper() or 'SULTRA' in lokasi.upper() or 'SULTENG' in lokasi.upper():
            print(f"✅ FOUND: {lokasi} | {row.get('komoditas', '')}")
            break
