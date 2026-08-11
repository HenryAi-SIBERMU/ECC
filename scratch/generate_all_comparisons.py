import pandas as pd
import numpy as np
import sys

def generate_comparison_table(v2_path, v3_path, title, value_col):
    try:
        v2 = pd.read_csv(v2_path)
        v3 = pd.read_csv(v3_path)
    except FileNotFoundError:
        return f"File not found for {title}\n"

    if 'year' in v2.columns:
        v2 = v2.dropna(subset=['year'])
        v2 = v2[(v2['year'] >= 2014) & (v2['year'] <= 2023)]
    if 'year' in v3.columns:
        v3 = v3.dropna(subset=['year'])
        v3 = v3[(v3['year'] >= 2014) & (v3['year'] <= 2023)]

    if 'is__umd_regional_primary_forest_2001' in v2.columns:
        v2 = v2[v2['is__umd_regional_primary_forest_2001'] == True]
    if 'is__umd_regional_primary_forest_2001' in v3.columns:
        v3 = v3[v3['is__umd_regional_primary_forest_2001'] == True]
    
    if 'wdpa_protected_areas__iucn_cat' in v2.columns:
        v2 = v2[v2['wdpa_protected_areas__iucn_cat'] != 0]
    if 'wdpa_protected_areas__iucn_cat' in v3.columns:
        v3 = v3[v3['wdpa_protected_areas__iucn_cat'] != 0]

    v2_sum = v2.groupby('province')[value_col].sum()
    v3_sum = v3.groupby('province')[value_col].sum()

    all_provs = sorted(list(set(v2_sum.index) | set(v3_sum.index)))
    
    md = f"## {title}\n\n"
    md += "| Provinsi | V2 Lama (BBox Salah) | V3 Resmi (GADM) | Selisih Absolut | Perubahan (%) |\n"
    md += "| :--- | :---: | :---: | :---: | :---: |\n"

    total_v2 = 0
    total_v3 = 0

    for prov in all_provs:
        val_v2 = v2_sum.get(prov, 0)
        val_v3 = v3_sum.get(prov, 0)
        diff = val_v3 - val_v2
        pct = (diff / val_v2 * 100) if val_v2 != 0 else (np.inf if val_v3 > 0 else 0)
        
        total_v2 += val_v2
        total_v3 += val_v3

        if pct == np.inf:
            pct_str = "+100.00%"
        else:
            pct_str = f"{pct:+.2f}%"

        md += f"| **{prov}** | {val_v2:,.2f} ha | **{val_v3:,.2f} ha** | {diff:+,.2f} ha | **{pct_str}** |\n"

    tot_diff = total_v3 - total_v2
    tot_pct = (tot_diff / total_v2 * 100) if total_v2 != 0 else 0
    md += f"| **TOTAL SULAWESI** | **{total_v2:,.2f} ha** | **{total_v3:,.2f} ha** | **{tot_diff:+,.2f} ha** | **{tot_pct:+.2f}%** |\n\n"
    
    return md

output_md = "# Laporan Analisis Forensik Keseluruhan Dataset GFW (V1/V2 vs V3)\n\n"
output_md += "Dokumen ini mencatat hasil evaluasi dan perbandingan forensik antara seluruh dataset GFW lama (V2) dengan dataset terbaru (V3) yang menggunakan Geostore ID resmi.\n\n"

output_md += generate_comparison_table(
    'data/raw/klhk_gfw/mega_fetch_v2/tree_cover_loss_sulawesi_2001_2025.csv',
    'data/raw/klhk_gfw/mega_fetch_v3/tree_cover_loss_sulawesi_v3.csv',
    '📊 1. Total Kehilangan Tutupan Pohon (Tree Cover Loss 2014-2023)',
    'tree_cover_loss_ha'
)

output_md += generate_comparison_table(
    'data/raw/klhk_gfw/mega_fetch_v2/primary_forest_loss_sulawesi_2001_2025.csv',
    'data/raw/klhk_gfw/mega_fetch_v3/primary_forest_loss_sulawesi_v3.csv',
    '🌳 2. Kehilangan Hutan Primer (Primary Forest Loss 2014-2023)',
    'area__ha'
)

output_md += generate_comparison_table(
    'data/raw/klhk_gfw/mega_fetch_v2/loss_in_protected_areas_sulawesi_2001_2025.csv',
    'data/raw/klhk_gfw/mega_fetch_v3/loss_in_protected_areas_sulawesi_v3.csv',
    '🛡️ 3. Kehilangan di Kawasan Lindung (Loss in Protected Areas 2014-2023)',
    'area__ha'
)

output_md += generate_comparison_table(
    'data/raw/klhk_gfw/mega_fetch_v2/loss_by_land_cover_sulawesi_2001_2025.csv',
    'data/raw/klhk_gfw/mega_fetch_v3/loss_by_land_cover_sulawesi_v3.csv',
    '🌿 4. Kehilangan Berdasarkan Tutupan Lahan (Loss by Land Cover 2014-2023)',
    'area__ha'
)

with open('scratch/all_comparisons_fixed.md', 'w', encoding='utf-8') as f:
    f.write(output_md)
