#!/usr/bin/env python3
"""
BPS PAD Data Processor
CELIOS ECC Intelligence System

Process downloaded PAD CSV files and consolidate into single dataset
"""

import sys
from pathlib import Path
from datetime import datetime
import pandas as pd
import numpy as np
import logging
import json

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Province mapping
PROVINCES = {
    "7100": "Sulawesi Utara",
    "7200": "Sulawesi Tengah",
    "7300": "Sulawesi Selatan",
    "7400": "Sulawesi Tenggara",
    "7500": "Gorontalo",
    "7600": "Sulawesi Barat"
}


class PADProcessor:
    """Processor for BPS PAD downloaded files"""
    
    def __init__(self, downloads_dir: str = "downloads", output_dir: str = "output"):
        self.downloads_dir = Path(downloads_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        self.data = []
        self.stats = {
            'files_processed': 0,
            'total_rows': 0,
            'provinces': [],
            'year_range': None,
            'missing_files': []
        }
    
    def find_downloaded_files(self):
        """Find all downloaded PAD CSV files"""
        logger.info("🔍 Scanning for downloaded files...")
        
        files_found = {}
        for prov_code, prov_name in PROVINCES.items():
            # Try multiple filename patterns
            patterns = [
                f"pad_{prov_code}_*.csv",
                f"pad_{prov_name.lower().replace(' ', '_')}_*.csv",
                f"*{prov_code}*.csv"
            ]
            
            found = False
            for pattern in patterns:
                matches = list(self.downloads_dir.glob(pattern))
                if matches:
                    files_found[prov_code] = matches[0]
                    logger.info(f"  ✅ {prov_name}: {matches[0].name}")
                    found = True
                    break
            
            if not found:
                logger.warning(f"  ❌ {prov_name}: NOT FOUND")
                self.stats['missing_files'].append(prov_name)
        
        return files_found
    
    def read_pad_file(self, filepath: Path, prov_code: str):
        """
        Read and standardize PAD file
        
        Args:
            filepath: Path to CSV file
            prov_code: Province code (e.g., '7300')
            
        Returns:
            DataFrame with standardized columns
        """
        logger.info(f"📖 Reading: {filepath.name}")
        
        try:
            # Try different encodings
            for encoding in ['utf-8-sig', 'utf-8', 'cp1252', 'iso-8859-1']:
                try:
                    df = pd.read_csv(filepath, encoding=encoding)
                    break
                except UnicodeDecodeError:
                    continue
            
            logger.info(f"  📊 Shape: {df.shape}")
            logger.info(f"  📋 Columns: {list(df.columns[:5])}... (showing first 5)")
            
            # Add metadata
            df['province_code'] = prov_code
            df['province_name'] = PROVINCES[prov_code]
            df['source_file'] = filepath.name
            df['processed_at'] = datetime.now().isoformat()
            
            # Clean data
            df = self.clean_dataframe(df)
            
            self.stats['files_processed'] += 1
            self.stats['total_rows'] += len(df)
            self.stats['provinces'].append(PROVINCES[prov_code])
            
            return df
            
        except Exception as e:
            logger.error(f"  ❌ Error reading file: {e}")
            return None
    
    def clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and standardize DataFrame"""
        
        # Remove completely empty rows
        df = df.dropna(how='all')
        
        # Remove rows where all data columns are empty (keep header rows)
        # This is conservative - adjust based on actual data
        
        # Strip whitespace from string columns
        str_cols = df.select_dtypes(include=['object']).columns
        df[str_cols] = df[str_cols].apply(lambda x: x.str.strip() if x.dtype == 'object' else x)
        
        # Convert numeric columns
        for col in df.columns:
            if col not in ['province_code', 'province_name', 'source_file', 'processed_at']:
                # Try to convert to numeric
                df[col] = pd.to_numeric(df[col], errors='ignore')
        
        return df
    
    def process_all(self):
        """Process all downloaded files"""
        logger.info("="*80)
        logger.info("BPS PAD Data Processor")
        logger.info("="*80)
        
        # Find files
        files = self.find_downloaded_files()
        
        if not files:
            logger.error("\n❌ No files found in downloads/ folder!")
            logger.error("Please download files following PANDUAN_DOWNLOAD_MANUAL_PAD.md")
            return None
        
        logger.info(f"\n✅ Found {len(files)} / {len(PROVINCES)} provinces")
        
        # Process each file
        logger.info("\n" + "="*80)
        logger.info("Processing Files")
        logger.info("="*80)
        
        all_data = []
        for prov_code, filepath in files.items():
            df = self.read_pad_file(filepath, prov_code)
            if df is not None:
                all_data.append(df)
        
        if not all_data:
            logger.error("\n❌ No data could be processed!")
            return None
        
        # Consolidate
        logger.info("\n" + "="*80)
        logger.info("Consolidating Data")
        logger.info("="*80)
        
        consolidated = pd.concat(all_data, ignore_index=True)
        logger.info(f"✅ Consolidated shape: {consolidated.shape}")
        
        # Save
        output_file = self.output_dir / f"pad_sulawesi_consolidated_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        consolidated.to_csv(output_file, index=False, encoding='utf-8-sig')
        
        logger.info(f"✅ Saved: {output_file}")
        
        # Save stats
        self.stats['year_range'] = self.detect_year_range(consolidated)
        stats_file = self.output_dir / "processing_stats.json"
        with open(stats_file, 'w') as f:
            json.dump(self.stats, f, indent=2)
        
        logger.info(f"✅ Stats: {stats_file}")
        
        return consolidated
    
    def detect_year_range(self, df: pd.DataFrame):
        """Detect year range from data"""
        # Look for year columns
        year_cols = [col for col in df.columns if str(col).isdigit() and 2000 <= int(col) <= 2030]
        
        if year_cols:
            years = sorted([int(col) for col in year_cols])
            return {'min': years[0], 'max': years[-1], 'count': len(years)}
        
        # Look for year in data
        for col in df.columns:
            if 'tahun' in str(col).lower() or 'year' in str(col).lower():
                try:
                    years = df[col].dropna().unique()
                    years = [int(y) for y in years if str(y).isdigit()]
                    if years:
                        return {'min': min(years), 'max': max(years), 'count': len(years)}
                except:
                    pass
        
        return None
    
    def print_summary(self):
        """Print processing summary"""
        logger.info("\n" + "="*80)
        logger.info("PROCESSING SUMMARY")
        logger.info("="*80)
        logger.info(f"Files processed: {self.stats['files_processed']} / {len(PROVINCES)}")
        logger.info(f"Total rows: {self.stats['total_rows']:,}")
        logger.info(f"Provinces: {', '.join(self.stats['provinces'])}")
        
        if self.stats['year_range']:
            yr = self.stats['year_range']
            logger.info(f"Year range: {yr['min']}-{yr['max']} ({yr['count']} years)")
        
        if self.stats['missing_files']:
            logger.warning(f"\n⚠️  Missing files: {', '.join(self.stats['missing_files'])}")
            logger.warning("   Download these provinces to complete dataset")
        
        logger.info("="*80)


def main():
    """Main function"""
    processor = PADProcessor()
    
    try:
        result = processor.process_all()
        
        if result is not None:
            processor.print_summary()
            
            print(f"\n✅ SUCCESS!")
            print(f"📁 Output: output/pad_sulawesi_consolidated_*.csv")
            print(f"📊 Total rows: {len(result):,}")
            print(f"📋 Columns: {len(result.columns)}")
            
            return 0
        else:
            print(f"\n❌ FAILED - No data processed")
            return 1
            
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Processing interrupted by user")
        return 1
        
    except Exception as e:
        logger.error(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
