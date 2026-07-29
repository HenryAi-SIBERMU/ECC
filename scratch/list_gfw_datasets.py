import json

def main():
    try:
        with open('../../tools/gfw/crawl_results/datasets_list.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # The structure is usually {'data': [{'dataset': '...', 'version': '...'}, ...]}
        # Or maybe it's a list directly. Let's handle both.
        items = data.get('data', data) if isinstance(data, dict) else data
        
        # We'll just collect the unique dataset names from the JSON
        datasets = []
        for item in items:
            ds_name = item.get('dataset', '')
            if ds_name and ds_name not in datasets:
                datasets.append(ds_name)
                
        # Group them roughly by keywords
        grouped = {
            'Deforestation & Loss': [],
            'Emissions & Biomass': [],
            'Alerts (Fire/GLAD)': [],
            'Concessions (Tambang/Sawit/Kayu)': [],
            'Land Cover & Protected Areas': [],
            'Others': []
        }
        
        for ds in sorted(datasets):
            d = ds.lower()
            if 'loss' in d or 'deforestation' in d or 'gain' in d:
                grouped['Deforestation & Loss'].append(ds)
            elif 'co2' in d or 'biomass' in d or 'carbon' in d or 'whrc' in d:
                grouped['Emissions & Biomass'].append(ds)
            elif 'alert' in d or 'fire' in d or 'glad' in d or 'viirs' in d:
                grouped['Alerts (Fire/GLAD)'].append(ds)
            elif 'concession' in d or 'plantation' in d or 'mining' in d or 'oil_palm' in d or 'moratorium' in d:
                grouped['Concessions (Tambang/Sawit/Kayu)'].append(ds)
            elif 'land_cover' in d or 'protected' in d or 'wdpa' in d or 'peat' in d or 'mangrove' in d or 'intact' in d:
                grouped['Land Cover & Protected Areas'].append(ds)
            else:
                grouped['Others'].append(ds)
                
        with open('../../tools/gfw/crawl_results/ALL_GFW_DATASETS_TABLE.md', 'w') as out:
            out.write("# 📡 KESELURUHAN DATASET GLOBAL FOREST WATCH\n\n")
            out.write("Berikut adalah daftar asli (raw dataset IDs) yang berhasil diekstrak langsung dari server GFW menggunakan script internal *crawler*.\n\n")
            
            for category, dlist in grouped.items():
                if not dlist: continue
                if category == 'Others': continue # Skip others to not clutter
                out.write(f"### {category}\n")
                out.write("| Dataset ID (Layer API GFW) | Keterangan Potensi |\n")
                out.write("| :--- | :--- |\n")
                for ds in dlist:
                    out.write(f"| `{ds}` | Dataset aktif di server GFW |\n")
                out.write("\n")
                
        print("Success writing table to ALL_GFW_DATASETS_TABLE.md")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
