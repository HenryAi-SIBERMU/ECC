import pandas as pd
from pathlib import Path
import sys

sys.stdout.reconfigure(encoding='utf-8')

def main():
    print("Building clean v2_Papua_Deforestation_by_LandCover_Concession.xlsx...")
    
    workspace_dir = Path(__file__).resolve().parents[3]
    raw_dir = workspace_dir / "data" / "raw" / "klhk_gfw" / "mega_fetch_papua"
    
    lc_file = raw_dir / "loss_by_land_cover_papua_6_prov.csv"
    cat_file = raw_dir / "tree_cover_by_category_papua_6_prov.csv"
    
    out_dirs = [
        workspace_dir / "data" / "processed" / "gfw papua"
    ]
    
    # 1. Process Land Cover (ESA 2015)
    df_lc = pd.read_csv(lc_file)
    df_lc['year'] = pd.to_numeric(df_lc['year'], errors='coerce')
    df_lc = df_lc[(df_lc['year'] >= 2016) & (df_lc['year'] <= 2026)].copy()
    
    # Filter out Sparse vegetation as requested
    df_lc = df_lc[df_lc['esa_land_cover_2015__class'] != 'Sparse vegetation'].copy()
    df_lc = df_lc.rename(columns={'esa_land_cover_2015__class': 'kategori', 'area__ha': 'loss_area_ha'})
    
    # Aggregated Pivot
    df_lc_agg = df_lc.groupby(['year', 'kategori'])['loss_area_ha'].sum().reset_index()
    pivot_lc = df_lc_agg.pivot(index='year', columns='kategori', values='loss_area_ha').reset_index()
    pivot_lc.columns.name = None
    pivot_lc.rename(columns=lambda x: f"{x} (ha)" if x != 'year' else 'year', inplace=True)
    
    cols_lc = ['year', 'Agriculture (ha)', 'Forest (ha)', 'Grassland (ha)', 'Settlement (ha)', 'Water (ha)']
    for c in cols_lc:
        if c not in pivot_lc.columns:
            pivot_lc[c] = 0.0
    pivot_lc = pivot_lc[cols_lc].fillna(0.0)
    
    # Raw Land Cover Tidy
    raw_lc = df_lc[['year', 'province', 'kategori', 'loss_area_ha']].sort_values(by=['year', 'province', 'kategori']).reset_index(drop=True)
    
    # 2. Process Plantations / Concession
    df_cat = pd.read_csv(cat_file)
    df_plant = df_cat[df_cat['category_type'] == 'gfw_plantations__type'].copy()
    df_plant = df_plant[df_plant['gfw_plantations__type'].notna() & (~df_plant['gfw_plantations__type'].isin(['Unknown', 'nan']))].copy()
    df_plant = df_plant.rename(columns={'gfw_plantations__type': 'kategori', 'area__ha': 'loss_area_ha'})
    
    # Total Plantations
    df_plant_agg = df_plant.groupby('kategori')['loss_area_ha'].sum().reset_index()
    pivot_plant = df_plant_agg.set_index('kategori').T.reset_index(drop=True)
    pivot_plant.columns.name = None
    pivot_plant.rename(columns=lambda x: f"{x} (ha)", inplace=True)
    
    # Raw Plantations Tidy
    raw_plant = df_plant[['province', 'kategori', 'loss_area_ha']].sort_values(by=['province', 'kategori']).reset_index(drop=True)
    
    # Write to Excel
    for out_dir in out_dirs:
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / "v2" / "v2_Papua_Deforestation_by_LandCover_Concession.xlsx"
        
        with pd.ExcelWriter(out_file, engine='openpyxl') as writer:
            pivot_lc.to_excel(writer, sheet_name='Total Tutupan Lahan (ESA 2015)', index=False)
            raw_lc.to_excel(writer, sheet_name='Raw Tutupan Lahan (ESA 2', index=False)
            pivot_plant.to_excel(writer, sheet_name='Total Tipe Konsesi (Plantations)', index=False)
            raw_plant.to_excel(writer, sheet_name='Raw Tipe Konsesi (Planta', index=False)
            
        print(f"✅ SUCCESS! Created: {out_file}")

if __name__ == '__main__':
    main()
