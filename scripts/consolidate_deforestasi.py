"""
Consolidate Deforestation Data dari Multiple Sources
====================================================

Merge data deforestasi dari:
1. Global Forest Watch (GFW) API - Primary source
2. SLHI PDFs (KLHK) - Government validation
3. SIMONTANA (future) - Detailed government data

Output: data/processed/sulawesi_deforestasi_2016_2024.csv

Author: CELIOS Research Division
Date: 14 Juni 2026
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
import logging
from typing import Dict, List

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DeforestationConsolidator:
    """Consolidator untuk merge deforestation data dari multiple sources."""
    
    SULAWESI_PROVINCES = [
        'Sulawesi Utara',
        'Sulawesi Tengah',
        'Sulawesi Selatan',
        'Sulawesi Tenggara',
        'Gorontalo',
        'Sulawesi Barat'
    ]
    
    def __init__(self, data_dir: Path):
        """Initialize consolidator."""
        self.data_dir = data_dir
        self.raw_gfw = data_dir / 'raw' / 'gfw'
        self.raw_slhi = data_dir / 'raw' / 'klhk_slhi'
        self.processed = data_dir / 'processed'
        
        logger.info("Initialized Deforestation Consolidator")
    
    def load_gfw_data(self) -> pd.DataFrame:
        """Load GFW data."""
        gfw_file = self.raw_gfw / 'sulawesi_deforestation_2016_2024.csv'
        
        if not gfw_file.exists():
            logger.warning(f"GFW data not found: {gfw_file}")
            return pd.DataFrame()
        
        df = pd.read_csv(gfw_file)
        logger.info(f"Loaded GFW data: {len(df)} rows")
        
        # Standardize column names
        df = df.rename(columns={
            'tree_cover_loss_ha': 'deforestation_rate_ha',
            'tree_cover_pct': 'forest_cover_pct'
        })
        
        df['source'] = 'GFW'
        return df
    
    def load_slhi_data(self) -> pd.DataFrame:
        """Load SLHI extracted data."""
        slhi_file = self.raw_slhi / 'deforestasi_sulawesi_slhi_extracted.csv'
        
        if not slhi_file.exists():
            logger.warning(f"SLHI data not found: {slhi_file}")
            return pd.DataFrame()
        
        df = pd.read_csv(slhi_file)
        logger.info(f"Loaded SLHI data: {len(df)} rows")
        
        # Standardize column names
        df = df.rename(columns={
            'forest_cover_ha': 'forest_cover_ha_slhi',
            'forest_cover_pct': 'forest_cover_pct_slhi',
            'deforestation_ha': 'deforestation_rate_ha'
        })
        
        df['source'] = 'SLHI'
        return df
    
    def merge_sources(
        self,
        df_gfw: pd.DataFrame,
        df_slhi: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Merge GFW dan SLHI data dengan strategi prioritas.
        
        Strategy:
        1. GFW sebagai primary (higher credibility, peer-reviewed)
        2. SLHI sebagai validation/gap-filling
        3. Keep both values untuk cross-validation analysis
        """
        if df_gfw.empty and df_slhi.empty:
            logger.error("No data available from any source!")
            return pd.DataFrame()
        
        # Use GFW as base jika tersedia
        if not df_gfw.empty:
            logger.info("Using GFW as primary data source")
            df_merged = df_gfw.copy()
            
            # Add SLHI data sebagai additional columns
            if not df_slhi.empty:
                logger.info("Merging SLHI data for cross-validation")
                
                # Prepare SLHI for merge
                df_slhi_merge = df_slhi[['province', 'year', 'deforestation_rate_ha', 'forest_cover_pct_slhi']].copy()
                df_slhi_merge = df_slhi_merge.rename(columns={
                    'deforestation_rate_ha': 'deforestation_rate_ha_slhi',
                    'forest_cover_pct_slhi': 'forest_cover_pct_slhi'
                })
                
                # Merge
                df_merged = df_merged.merge(
                    df_slhi_merge,
                    on=['province', 'year'],
                    how='left'
                )
                
                # Calculate discrepancy
                df_merged['deforestation_discrepancy_pct'] = (
                    (df_merged['deforestation_rate_ha'] - df_merged['deforestation_rate_ha_slhi']) / 
                    df_merged['deforestation_rate_ha'] * 100
                ).round(2)
        
        # Fallback ke SLHI jika GFW tidak tersedia
        else:
            logger.warning("GFW data not available, using SLHI as primary")
            df_merged = df_slhi.copy()
        
        return df_merged
    
    def fill_missing_years(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Fill missing years dengan interpolation untuk continuity.
        
        Note: Only for minor gaps, not for large missing ranges.
        """
        logger.info("Checking for missing years...")
        
        # Create complete year range per province
        all_combos = []
        for province in self.SULAWESI_PROVINCES:
            for year in range(2016, 2025):
                all_combos.append({'province': province, 'year': year})
        
        df_complete = pd.DataFrame(all_combos)
        
        # Merge dengan existing data
        df_filled = df_complete.merge(df, on=['province', 'year'], how='left')
        
        # Count missing
        missing = df_filled['deforestation_rate_ha'].isna().sum()
        logger.info(f"Missing data points: {missing} / {len(df_filled)}")
        
        if missing > 0:
            logger.info("Applying interpolation untuk minor gaps...")
            # Interpolate within each province
            df_filled = df_filled.sort_values(['province', 'year'])
            df_filled['deforestation_rate_ha'] = df_filled.groupby('province')['deforestation_rate_ha'].transform(
                lambda x: x.interpolate(method='linear', limit_area='inside')
            )
            
            # Mark interpolated values
            df_filled['is_interpolated'] = df_filled['data_source'].isna()
            df_filled.loc[df_filled['is_interpolated'], 'confidence_level'] = 'Low (Interpolated)'
        
        return df_filled
    
    def calculate_statistics(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate additional statistics."""
        logger.info("Calculating additional statistics...")
        
        # Calculate year-over-year change
        df = df.sort_values(['province', 'year'])
        df['deforestation_yoy_change_pct'] = df.groupby('province')['deforestation_rate_ha'].pct_change() * 100
        
        # Calculate cumulative deforestation (2016-2024)
        df['cumulative_deforestation_ha'] = df.groupby('province')['deforestation_rate_ha'].cumsum()
        
        return df
    
    def validate_data_quality(self, df: pd.DataFrame) -> Dict:
        """Validate data quality dan generate report."""
        logger.info("Validating data quality...")
        
        report = {
            'total_rows': len(df),
            'provinces_covered': df['province'].nunique(),
            'years_covered': sorted(df['year'].unique().tolist()),
            'missing_values': df['deforestation_rate_ha'].isna().sum(),
            'completeness_pct': (1 - df['deforestation_rate_ha'].isna().sum() / len(df)) * 100
        }
        
        # Check for outliers (>3 std dev)
        if 'deforestation_rate_ha' in df.columns and df['deforestation_rate_ha'].notna().sum() > 0:
            mean = df['deforestation_rate_ha'].mean()
            std = df['deforestation_rate_ha'].std()
            outliers = df[np.abs(df['deforestation_rate_ha'] - mean) > 3 * std]
            report['outliers'] = len(outliers)
        
        # Cross-validation check (if both sources available)
        if 'deforestation_rate_ha_slhi' in df.columns:
            df_both = df.dropna(subset=['deforestation_rate_ha', 'deforestation_rate_ha_slhi'])
            if len(df_both) > 0:
                correlation = df_both[['deforestation_rate_ha', 'deforestation_rate_ha_slhi']].corr().iloc[0, 1]
                report['gfw_slhi_correlation'] = round(correlation, 3)
                
                avg_discrepancy = df_both['deforestation_discrepancy_pct'].abs().mean()
                report['avg_discrepancy_pct'] = round(avg_discrepancy, 2)
        
        return report
    
    def consolidate(self) -> pd.DataFrame:
        """Main consolidation pipeline."""
        logger.info("=" * 70)
        logger.info("CONSOLIDATING DEFORESTATION DATA")
        logger.info("=" * 70)
        
        # Load data
        df_gfw = self.load_gfw_data()
        df_slhi = self.load_slhi_data()
        
        # Merge sources
        df_merged = self.merge_sources(df_gfw, df_slhi)
        
        if df_merged.empty:
            logger.error("Consolidation failed: no data available")
            return df_merged
        
        # Fill missing years
        df_filled = self.fill_missing_years(df_merged)
        
        # Calculate statistics
        df_final = self.calculate_statistics(df_filled)
        
        # Reorder columns
        base_cols = [
            'province', 'year', 
            'deforestation_rate_ha', 'forest_cover_pct',
            'data_source', 'confidence_level'
        ]
        other_cols = [c for c in df_final.columns if c not in base_cols]
        df_final = df_final[base_cols + other_cols]
        
        # Validate
        quality_report = self.validate_data_quality(df_final)
        
        # Display report
        logger.info("\n" + "=" * 70)
        logger.info("DATA QUALITY REPORT")
        logger.info("=" * 70)
        for key, value in quality_report.items():
            logger.info(f"{key}: {value}")
        
        return df_final
    
    def save_consolidated(self, df: pd.DataFrame) -> Path:
        """Save consolidated data."""
        self.processed.mkdir(parents=True, exist_ok=True)
        
        output_file = self.processed / 'sulawesi_deforestasi_2016_2024.csv'
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        
        logger.info(f"\n✅ Consolidated data saved to: {output_file}")
        return output_file


def main():
    """Main execution."""
    data_dir = project_root / 'data'
    
    consolidator = DeforestationConsolidator(data_dir)
    df_final = consolidator.consolidate()
    
    if not df_final.empty:
        # Display sample
        logger.info("\n" + "=" * 70)
        logger.info("SAMPLE CONSOLIDATED DATA (First 15 rows)")
        logger.info("=" * 70)
        print(df_final.head(15).to_string(index=False))
        
        # Save
        output_file = consolidator.save_consolidated(df_final)
        
        # Summary per province
        logger.info("\n" + "=" * 70)
        logger.info("PER-PROVINCE SUMMARY")
        logger.info("=" * 70)
        
        summary = df_final.groupby('province').agg({
            'deforestation_rate_ha': ['mean', 'sum', 'count'],
            'cumulative_deforestation_ha': 'max',
            'year': ['min', 'max']
        }).round(2)
        
        print(summary)
        
        logger.info("\n" + "=" * 70)
        logger.info("NEXT STEPS")
        logger.info("=" * 70)
        logger.info("1. Review consolidated data for anomalies")
        logger.info("2. Use data for Checkpoint 4 analysis:")
        logger.info("   - Luas Industri vs Deforestasi crosstab")
        logger.info("   - Temporal correlation mining expansion vs forest loss")
        logger.info("3. Create visualization in pages/2_Kualitas_Lingkungan.py")
        logger.info("4. Document findings in research report")
        
    else:
        logger.error("\n❌ Consolidation failed. Please check:")
        logger.error("1. GFW data: python tools/gfw/fetch_sulawesi_deforestation.py")
        logger.error("2. SLHI data: python tools/pdf_extraction/extract_deforestasi_slhi.py")


if __name__ == "__main__":
    main()
