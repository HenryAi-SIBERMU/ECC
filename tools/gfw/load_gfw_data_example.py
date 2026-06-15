"""
EXAMPLE: Loading GFW Data for Analysis
========================================

Quick reference untuk load 19 dashboard cards dari file CSV yang ada.

Author: CELIOS Research
Date: 14 Juni 2026
"""

import pandas as pd
from pathlib import Path

# Base path
BASE = Path("data/raw/klhk_gfw")


def load_card_1_tree_cover_loss():
    """Card #1: Tree Cover Loss"""
    file = BASE / "mega_fetch_v2/tree_cover_loss_sulawesi_2001_2025.csv"
    df = pd.read_csv(file)
    print(f"✅ Card #1: {len(df)} rows")
    return df


def load_card_2_primary_forest_loss():
    """Card #2: Primary Forest Loss"""
    file = BASE / "mega_fetch_v2/primary_forest_loss_sulawesi_2001_2025.csv"
    df = pd.read_csv(file)
    print(f"✅ Card #2: {len(df)} rows")
    return df


def load_card_3_tree_cover_by_category():
    """Card #3: Tree Cover by Land Category"""
    file = BASE / "mega_fetch_v2/tree_cover_by_category_sulawesi_2001_2025.csv"
    df = pd.read_csv(file)
    print(f"✅ Card #3: {len(df)} rows")
    return df


def load_card_4_primary_forest_by_category():
    """Card #4: Primary Forest by Land Category (FILTER from #3)"""
    df = load_card_3_tree_cover_by_category()
    
    # Filter by is_primary flag
    if 'is_primary' in df.columns:
        primary = df[df['is_primary'] == True].copy()
    elif 'is__umd_regional_primary_forest_2001' in df.columns:
        primary = df[df['is__umd_regional_primary_forest_2001'] == True].copy()
    else:
        print("⚠️ Card #4: No is_primary column found!")
        return pd.DataFrame()
    
    print(f"⚠️ Card #4: {len(primary)} rows (filtered from #3)")
    return primary


def load_card_5_loss_by_category():
    """Card #5: Tree Cover Loss by Land Category"""
    file = BASE / "complete_fetch/loss_by_category_sulawesi_2001_2025.csv"
    df = pd.read_csv(file)
    print(f"✅ Card #5: {len(df)} rows")
    return df


def load_card_7_loss_by_driver():
    """Card #7: Tree Cover Loss by Driver (THE GOLDEN FILE!)"""
    file = BASE / "land_api_fetch/loss_by_driver_sulawesi_2001_2025.csv"
    df = pd.read_csv(file)
    print(f"✅ Card #7: {len(df)} rows")
    print(f"   Drivers: {df['driver'].unique()}")
    print(f"   Provinces: {df['province'].unique()}")
    return df


def load_card_6_primary_loss_by_driver():
    """Card #6: Primary Forest Loss by Driver (FILTER from #7)"""
    df = load_card_7_loss_by_driver()
    
    # Filter by is_primary flag
    if 'is_primary' in df.columns:
        primary = df[df['is_primary'] == True].copy()
    elif 'is__umd_regional_primary_forest_2001' in df.columns:
        primary = df[df['is__umd_regional_primary_forest_2001'] == True].copy()
    else:
        print("⚠️ Card #6: No is_primary column found!")
        return pd.DataFrame()
    
    print(f"⚠️ Card #6: {len(primary)} rows (filtered from #7)")
    return primary


def load_card_8_co2_emissions():
    """Card #8: CO2 Emissions (COLUMN from #7)"""
    df = load_card_7_loss_by_driver()
    
    # Select CO2 columns
    co2_cols = ['province', 'year', 'driver', 'area_ha', 'co2_emissions_mg']
    
    if 'co2_emissions_mg' in df.columns:
        co2 = df[co2_cols].copy()
    elif 'gross_carbon_emissions_Mg' in df.columns:
        co2 = df[['province', 'year', 'driver', 'area_ha', 'gross_carbon_emissions_Mg']].copy()
        co2.rename(columns={'gross_carbon_emissions_Mg': 'co2_emissions_mg'}, inplace=True)
    else:
        print("⚠️ Card #8: No CO2 column found!")
        return pd.DataFrame()
    
    # Remove nulls
    co2 = co2.dropna(subset=['co2_emissions_mg'])
    
    print(f"✅ Card #8: {len(co2)} rows with CO2 data")
    return co2


def load_card_10_loss_in_protected_areas():
    """Card #10: Tree Cover Loss in Protected Areas"""
    file = BASE / "mega_fetch_v2/loss_in_protected_areas_sulawesi_2001_2025.csv"
    df = pd.read_csv(file)
    print(f"✅ Card #10: {len(df)} rows")
    return df


def load_card_14_tree_cover_extent_2000():
    """Card #14: Tree Cover Extent 2000"""
    file = BASE / "complete_fetch/tree_cover_extent_sulawesi_2001_2025.csv"
    df = pd.read_csv(file)
    
    # Filter year 2000
    if 'year' in df.columns:
        extent_2000 = df[df['year'] == 2000].copy()
    else:
        print("⚠️ Card #14: No year column found!")
        return pd.DataFrame()
    
    print(f"✅ Card #14: {len(extent_2000)} rows (year 2000)")
    return extent_2000


def load_card_15_tree_cover_extent_2010():
    """Card #15: Tree Cover Extent 2010"""
    file = BASE / "complete_fetch/tree_cover_extent_sulawesi_2001_2025.csv"
    df = pd.read_csv(file)
    
    # Filter year 2010
    if 'year' in df.columns:
        extent_2010 = df[df['year'] == 2010].copy()
    else:
        print("⚠️ Card #15: No year column found!")
        return pd.DataFrame()
    
    print(f"✅ Card #15: {len(extent_2010)} rows (year 2010)")
    return extent_2010


def load_card_17_tree_cover_gain():
    """Card #17: Tree Cover Gain"""
    file = BASE / "mega_fetch_v2/tree_cover_gain_sulawesi_2001_2025.csv"
    df = pd.read_csv(file)
    print(f"✅ Card #17: {len(df)} rows")
    return df


def load_card_18_deforestation_rate():
    """Card #18: Deforestation Rate"""
    file = BASE / "complete_fetch/deforestation_rate_sulawesi_2001_2025.csv"
    df = pd.read_csv(file)
    print(f"✅ Card #18: {len(df)} rows")
    return df


def load_card_19_forest_cover_change():
    """Card #19: Forest Cover Change"""
    file = BASE / "complete_fetch/forest_cover_change_sulawesi_2001_2025.csv"
    df = pd.read_csv(file)
    print(f"✅ Card #19: {len(df)} rows")
    return df


# ============================================================================
# ANALYSIS EXAMPLES
# ============================================================================

def example_1_mining_impact():
    """
    EXAMPLE 1: Analyze mining impact via commodity-driven deforestation
    """
    print("\n" + "="*70)
    print("EXAMPLE 1: Mining Impact Analysis")
    print("="*70)
    
    # Load driver data
    df = load_card_7_loss_by_driver()
    
    # Filter commodity-driven deforestation (includes mining + plantations)
    commodity = df[df['driver'] == 'Commodity driven deforestation'].copy()
    
    print(f"\n📊 COMMODITY-DRIVEN DEFORESTATION:")
    print(f"   Total area: {commodity['area_ha'].sum():,.0f} ha")
    print(f"   Years: {commodity['year'].min()}-{commodity['year'].max()}")
    print(f"   Provinces: {commodity['province'].nunique()}")
    
    # By province
    by_province = commodity.groupby('province')['area_ha'].sum().sort_values(ascending=False)
    print(f"\n   BY PROVINCE:")
    for prov, area in by_province.items():
        print(f"     {prov}: {area:,.0f} ha")
    
    # By year
    by_year = commodity.groupby('year')['area_ha'].sum().sort_values(ascending=False)
    print(f"\n   TOP 5 YEARS:")
    for year, area in by_year.head(5).items():
        print(f"     {year}: {area:,.0f} ha")
    
    return commodity


def example_2_primary_forest_drivers():
    """
    EXAMPLE 2: What's destroying PRIMARY forests?
    """
    print("\n" + "="*70)
    print("EXAMPLE 2: Primary Forest Destruction Drivers")
    print("="*70)
    
    # Load primary forest driver data
    df = load_card_6_primary_loss_by_driver()
    
    print(f"\n📊 PRIMARY FOREST LOSS BY DRIVER:")
    
    # By driver
    by_driver = df.groupby('driver')['area_ha'].sum().sort_values(ascending=False)
    total = by_driver.sum()
    
    for driver, area in by_driver.items():
        pct = (area / total) * 100
        print(f"   {driver}: {area:,.0f} ha ({pct:.1f}%)")
    
    return df


def example_3_protected_area_violations():
    """
    EXAMPLE 3: Deforestation in protected areas
    """
    print("\n" + "="*70)
    print("EXAMPLE 3: Protected Area Violations")
    print("="*70)
    
    # Load protected area data
    df = load_card_10_loss_in_protected_areas()
    
    print(f"\n📊 LOSS IN PROTECTED AREAS:")
    print(f"   Total area: {df['area_ha'].sum() if 'area_ha' in df.columns else 'N/A'}")
    
    # By province
    if 'province' in df.columns and 'area_ha' in df.columns:
        by_province = df.groupby('province')['area_ha'].sum().sort_values(ascending=False)
        print(f"\n   BY PROVINCE:")
        for prov, area in by_province.items():
            print(f"     {prov}: {area:,.0f} ha")
    
    return df


def example_4_co2_emissions():
    """
    EXAMPLE 4: CO2 emissions from deforestation
    """
    print("\n" + "="*70)
    print("EXAMPLE 4: CO2 Emissions")
    print("="*70)
    
    # Load CO2 data
    df = load_card_8_co2_emissions()
    
    print(f"\n📊 CO2 EMISSIONS:")
    print(f"   Total: {df['co2_emissions_mg'].sum():,.0f} Mg CO2")
    
    # By driver
    by_driver = df.groupby('driver')['co2_emissions_mg'].sum().sort_values(ascending=False)
    print(f"\n   BY DRIVER:")
    for driver, co2 in by_driver.items():
        print(f"     {driver}: {co2:,.0f} Mg CO2")
    
    return df


def example_5_deforestation_rate():
    """
    EXAMPLE 5: Deforestation rate over time
    """
    print("\n" + "="*70)
    print("EXAMPLE 5: Deforestation Rate Trends")
    print("="*70)
    
    # Load deforestation rate
    df = load_card_18_deforestation_rate()
    
    if 'year' in df.columns and 'deforestation_rate_pct' in df.columns:
        by_year = df.groupby('year')['deforestation_rate_pct'].mean().sort_values(ascending=False)
        
        print(f"\n📊 AVERAGE DEFORESTATION RATE BY YEAR:")
        print(f"   Highest 5 years:")
        for year, rate in by_year.head(5).items():
            print(f"     {year}: {rate:.2f}%")
    
    return df


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("\n" + "="*70)
    print("GFW DATA LOADING EXAMPLES")
    print("="*70)
    print("Loading all available cards...\n")
    
    # Load all cards
    cards = {
        1: load_card_1_tree_cover_loss(),
        2: load_card_2_primary_forest_loss(),
        3: load_card_3_tree_cover_by_category(),
        4: load_card_4_primary_forest_by_category(),
        5: load_card_5_loss_by_category(),
        6: load_card_6_primary_loss_by_driver(),
        7: load_card_7_loss_by_driver(),
        8: load_card_8_co2_emissions(),
        10: load_card_10_loss_in_protected_areas(),
        14: load_card_14_tree_cover_extent_2000(),
        15: load_card_15_tree_cover_extent_2010(),
        17: load_card_17_tree_cover_gain(),
        18: load_card_18_deforestation_rate(),
        19: load_card_19_forest_cover_change()
    }
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    total_rows = sum(len(df) for df in cards.values() if not df.empty)
    loaded = len([df for df in cards.values() if not df.empty])
    print(f"✅ Loaded {loaded}/14 cards")
    print(f"📊 Total rows: {total_rows:,}")
    
    # Run examples
    example_1_mining_impact()
    example_2_primary_forest_drivers()
    example_3_protected_area_violations()
    example_4_co2_emissions()
    example_5_deforestation_rate()
    
    print("\n" + "="*70)
    print("DONE!")
    print("="*70)


if __name__ == "__main__":
    main()
