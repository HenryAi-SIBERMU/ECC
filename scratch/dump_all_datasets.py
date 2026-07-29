import json
import os

def main():
    # The correct path from scratch folder to crawl_results
    json_path = '../tools/gfw/crawl_results/datasets_list.json'
    
    if not os.path.exists(json_path):
        print(f"File not found: {json_path}")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    items = data.get('data', data) if isinstance(data, dict) else data
    
    datasets = []
    for item in items:
        ds_name = item.get('dataset', '')
        if ds_name and ds_name not in datasets:
            datasets.append(ds_name)
            
    datasets.sort()
    
    out_file = '../../brain/e4fefee7-85e6-412e-bc6a-613a92bebed0/ALL_GFW_DATASETS_RAW.md'
    
    with open(out_file, 'w', encoding='utf-8') as out:
        out.write(f"# 📡 KESELURUHAN {len(datasets)} DATASET GFW\n\n")
        out.write("Ini adalah daftar LENGKAP seluruh dataset/layer yang berhasil ditarik dari API GFW tanpa ada yang dipotong.\n\n")
        out.write("| No | Dataset ID (Layer GFW) |\n")
        out.write("|---|---|\n")
        
        for i, ds in enumerate(datasets, 1):
            out.write(f"| {i} | `{ds}` |\n")
            
    print(f"Total datasets found: {len(datasets)}")
    print(f"List written to: {out_file}")

if __name__ == '__main__':
    main()
