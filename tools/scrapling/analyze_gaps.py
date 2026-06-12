"""
Analisis GAP untuk Investment, Capacity Input, Capacity Output
"""
import pandas as pd
import numpy as np

print("="*100)
print("ANALISIS GAP DATA - ESDM MASTER SULAWESI NIKEL")
print("="*100)

# Load Indonesian-named dataset
df = pd.read_csv('../../data/processed/esdm_master_sulawesi_nikel_2016_2026_id.csv')
print(f"\nTotal records: {len(df):,}\n")

# ============================================================================
# GAP 1: INVESTASI
# ============================================================================
print("="*100)
print("GAP 1: INVESTASI (investasi_miliar_rp)")
print("="*100)

has_investasi = df['investasi_miliar_rp'].notna()
no_investasi = ~has_investasi

print(f"\n📊 Coverage:")
print(f"  ✅ Ada data: {has_investasi.sum():,} ({has_investasi.sum()/len(df)*100:.1f}%)")
print(f"  ❌ Missing:  {no_investasi.sum():,} ({no_investasi.sum()/len(df)*100:.1f}%)")

print(f"\n💰 Investasi yang ada:")
print(f"  Total: {df['investasi_miliar_rp'].sum():.1f} Miliar Rp")
print(f"  Min:   {df['investasi_miliar_rp'].min():.1f} Miliar Rp")
print(f"  Max:   {df['investasi_miliar_rp'].max():.1f} Miliar Rp")
print(f"  Mean:  {df['investasi_miliar_rp'].mean():.1f} Miliar Rp")

print(f"\n🔍 Profil records DENGAN investasi:")
with_inv = df[has_investasi]
print(f"  Provinsi:")
for prov in with_inv['provinsi'].value_counts().items():
    print(f"    {prov[0]:25s}: {prov[1]:2,} records")
print(f"\n  Punya kapasitas juga: {with_inv['kapasitas_input_ton_tahun'].notna().sum()}/{len(with_inv)}")

print(f"\n🔍 Profil records TANPA investasi:")
without_inv = df[no_investasi]
print(f"  Provinsi:")
for prov in without_inv['provinsi'].value_counts().items():
    print(f"    {prov[0]:25s}: {prov[1]:3,} records")
print(f"  Punya kapasitas: {without_inv['kapasitas_input_ton_tahun'].notna().sum()}/{len(without_inv)}")
print(f"  Punya luas lahan: {without_inv['luas_hektar'].notna().sum()}/{len(without_inv)}")

# ============================================================================
# GAP 2: KAPASITAS INPUT
# ============================================================================
print("\n" + "="*100)
print("GAP 2: KAPASITAS INPUT (kapasitas_input_ton_tahun)")
print("="*100)

has_cap_input = df['kapasitas_input_ton_tahun'].notna()
no_cap_input = ~has_cap_input

print(f"\n📊 Coverage:")
print(f"  ✅ Ada data: {has_cap_input.sum():,} ({has_cap_input.sum()/len(df)*100:.1f}%)")
print(f"  ❌ Missing:  {no_cap_input.sum():,} ({no_cap_input.sum()/len(df)*100:.1f}%)")

print(f"\n🏭 Kapasitas input yang ada:")
print(f"  Total: {df['kapasitas_input_ton_tahun'].sum():,.0f} ton/tahun")
print(f"  Min:   {df['kapasitas_input_ton_tahun'].min():,.0f} ton/tahun")
print(f"  Max:   {df['kapasitas_input_ton_tahun'].max():,.0f} ton/tahun")
print(f"  Mean:  {df['kapasitas_input_ton_tahun'].mean():,.0f} ton/tahun")

print(f"\n🔍 Profil records DENGAN kapasitas input:")
with_cap = df[has_cap_input]
print(f"  Provinsi:")
for prov in with_cap['provinsi'].value_counts().items():
    print(f"    {prov[0]:25s}: {prov[1]:2,} records")
print(f"  Sumber data CGS: {(with_cap['sumber_data'].str.contains('cgs', case=False, na=False)).sum()}/{len(with_cap)}")
print(f"  Confidence high: {(with_cap['kepercayaan_kapasitas'] == 'high').sum()}")
print(f"  Confidence medium: {(with_cap['kepercayaan_kapasitas'] == 'medium').sum()}")

print(f"\n🔍 Profil records TANPA kapasitas input:")
without_cap = df[no_cap_input]
print(f"  Provinsi:")
for prov in without_cap['provinsi'].value_counts().items():
    print(f"    {prov[0]:25s}: {prov[1]:3,} records")
print(f"  Punya luas lahan: {without_cap['luas_hektar'].notna().sum()}/{len(without_cap)}")
print(f"  Tahap operasi:")
for tahap in without_cap['tahap_operasi'].value_counts().head(3).items():
    print(f"    {tahap[0]}: {tahap[1]}")

# ============================================================================
# GAP 3: KAPASITAS OUTPUT
# ============================================================================
print("\n" + "="*100)
print("GAP 3: KAPASITAS OUTPUT (kapasitas_output_ton_tahun)")
print("="*100)

has_cap_output = df['kapasitas_output_ton_tahun'].notna()
no_cap_output = ~has_cap_output

print(f"\n📊 Coverage:")
print(f"  ✅ Ada data: {has_cap_output.sum():,} ({has_cap_output.sum()/len(df)*100:.1f}%)")
print(f"  ❌ Missing:  {no_cap_output.sum():,} ({no_cap_output.sum()/len(df)*100:.1f}%)")

print(f"\n🏭 Kapasitas output yang ada:")
print(f"  Total: {df['kapasitas_output_ton_tahun'].sum():,.0f} ton/tahun")
print(f"  Min:   {df['kapasitas_output_ton_tahun'].min():,.0f} ton/tahun")
print(f"  Max:   {df['kapasitas_output_ton_tahun'].max():,.0f} ton/tahun")
print(f"  Mean:  {df['kapasitas_output_ton_tahun'].mean():,.0f} ton/tahun")

print(f"\n📦 Jenis produk output:")
for product in df['jenis_produk_output'].value_counts().items():
    print(f"  {product[0]}: {product[1]:2,} records")

# ============================================================================
# CROSS-ANALYSIS
# ============================================================================
print("\n" + "="*100)
print("CROSS-ANALYSIS")
print("="*100)

print(f"\n🔗 Korelasi antar variabel:")
print(f"\n  Records dengan INVESTASI ({has_investasi.sum()}):")
print(f"    - Punya kapasitas input: {(has_investasi & has_cap_input).sum()} ({(has_investasi & has_cap_input).sum()/has_investasi.sum()*100:.1f}%)")
print(f"    - Punya kapasitas output: {(has_investasi & has_cap_output).sum()} ({(has_investasi & has_cap_output).sum()/has_investasi.sum()*100:.1f}%)")

print(f"\n  Records dengan KAPASITAS INPUT ({has_cap_input.sum()}):")
print(f"    - Punya investasi: {(has_cap_input & has_investasi).sum()} ({(has_cap_input & has_investasi).sum()/has_cap_input.sum()*100:.1f}%)")
print(f"    - Punya kapasitas output: {(has_cap_input & has_cap_output).sum()} ({(has_cap_input & has_cap_output).sum()/has_cap_input.sum()*100:.1f}%)")

print(f"\n  Records dengan KAPASITAS OUTPUT ({has_cap_output.sum()}):")
print(f"    - Punya investasi: {(has_cap_output & has_investasi).sum()} ({(has_cap_output & has_investasi).sum()/has_cap_output.sum()*100:.1f}%)")
print(f"    - Punya kapasitas input: {(has_cap_output & has_cap_input).sum()} ({(has_cap_output & has_cap_input).sum()/has_cap_output.sum()*100:.1f}%)")

print(f"\n  Records LENGKAP (investasi + cap_input + cap_output): {(has_investasi & has_cap_input & has_cap_output).sum()}")
print(f"  Records TIDAK ADA SATUPUN: {(no_investasi & no_cap_input & no_cap_output).sum()}")

# ============================================================================
# REKOMENDASI STRATEGI GAP FILLING
# ============================================================================
print("\n" + "="*100)
print("REKOMENDASI STRATEGI GAP FILLING")
print("="*100)

print(f"""
📋 SUMMARY GAP:
  - Investasi missing: {no_investasi.sum():,} records ({no_investasi.sum()/len(df)*100:.1f}%)
  - Kapasitas input missing: {no_cap_input.sum():,} records ({no_cap_input.sum()/len(df)*100:.1f}%)
  - Kapasitas output missing: {no_cap_output.sum():,} records ({no_cap_output.sum()/len(df)*100:.1f}%)

💡 STRATEGI GAP FILLING:

══════════════════════════════════════════════════════════════════════════════════════════════
OPSI 1: SKIP GAP FILLING (Conservative)
══════════════════════════════════════════════════════════════════════════════════════════════
Rationale:
  - 333 records sudah punya luas_hektar (100%) → cukup untuk environmental impact
  - 69 records punya kapasitas (20.7%) → cukup untuk sample smelter analysis
  - Investment dari PMDN tidak reliable (agregat semua sektor, bukan mining-specific)
  
Pros:
  ✅ Data quality tinggi (no estimation, no assumption)
  ✅ Transparan (jelas mana yang real data, mana yang kosong)
  ✅ Cepat (tidak perlu effort tambahan)
  
Cons:
  ❌ Analisis ekonomi terbatas (tidak bisa estimate total investasi)
  ❌ Analisis produksi terbatas (hanya 20.7% sample)

══════════════════════════════════════════════════════════════════════════════════════════════
OPSI 2: FILL INVESTMENT ONLY (Partial Fill)
══════════════════════════════════════════════════════════════════════════════════════════════
Method:
  1. Untuk records DENGAN kapasitas → allocate PMDN proportional by capacity
  2. Untuk records TANPA kapasitas → allocate PMDN proportional by luas_hektar
  3. Assumption: 30-40% PMDN provinsi untuk mining sector
  
Coverage improvement:
  - Investasi: dari {has_investasi.sum()} → ~300 records (90%+)
  
Pros:
  ✅ Semua records dapat estimasi investment
  ✅ Method transparan (documented allocation)
  ✅ Bisa analisis ekonomi regional
  
Cons:
  ⚠️ Estimasi, bukan actual data
  ⚠️ Assumption 30-40% mining bisa salah
  ⚠️ PMDN tidak include PMA (foreign investment)

══════════════════════════════════════════════════════════════════════════════════════════════
OPSI 3: FILL CAPACITY (Advanced - High Effort)
══════════════════════════════════════════════════════════════════════════════════════════════
Method:
  1. Estimate capacity based on luas_hektar (rule of thumb: X ton/ha)
  2. Group by provinsi/kabupaten, use average capacity per hectare
  3. Only for SMELTERS (tahap_operasi = OPERASI PRODUKSI)
  
Coverage improvement:
  - Kapasitas: dari {has_cap_input.sum()} → ~100 records (30%+)
  
Pros:
  ✅ Lebih banyak records dengan capacity
  ✅ Bisa estimate produksi regional
  
Cons:
  ⚠️ Estimasi kasar (capacity ≠ linear dengan luas)
  ⚠️ High uncertainty
  ⚠️ Risk of over/under estimation

══════════════════════════════════════════════════════════════════════════════════════════════
OPSI 4: HYBRID (Recommended untuk ECC)
══════════════════════════════════════════════════════════════════════════════════════════════
Method:
  1. SKIP capacity filling (terlalu uncertain)
  2. FILL investment dengan method proportional (luas_hektar based)
  3. DOCUMENT clearly: mana real data, mana estimasi
  
Output:
  - 3 kolom investasi:
    * investasi_miliar_rp_real (actual data, 26 records)
    * investasi_miliar_rp_estimasi (filled, 307 records)
    * investasi_miliar_rp_confidence (real/estimated)
  
Pros:
  ✅ Balance antara completeness & quality
  ✅ Transparan (ada flag real vs estimated)
  ✅ Cukup untuk environmental + economic analysis
  
Cons:
  🟡 Tetap ada uncertainty di investment

══════════════════════════════════════════════════════════════════════════════════════════════
""")

print("="*100)
print("DISKUSI: Mau pilih opsi yang mana?")
print("="*100)
print("""
Pertanyaan untuk diskusi:
1. Apakah investment data PERLU di-fill? (untuk environmental impact, mungkin tidak perlu)
2. Apakah capacity PERLU di-fill? (risiko estimasi salah tinggi)
3. Apakah lebih baik TRANSPARAN (ada gap) atau COMPLETE (ada estimasi)?
4. Confidence level minimum yang acceptable?
""")
