"""
Extract Deforestasi Data dari SLHI PDFs
=======================================

Script untuk mengekstrak data deforestasi/tutupan hutan dari SLHI (Status Lingkungan
Hidup Indonesia) PDF reports menggunakan Camelot/Tabula.

Input: data/raw/klhk_sulut_kualitas_air/SLHI_*.pdf
Output: data/raw/klhk_slhi/deforestasi_sulawesi_extracted.csv

Author: CELIOS Research Division
Date: 14 Juni 2026
"""

import sys
from pathlib import Path
import pandas as pd
import camelot
import logging
import re
from typing import List, Dict, Optional

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SLHIDeforestationExtractor:
    """Extractor untuk data deforestasi dari SLHI PDFs."""
    
    SULAWESI_PROVINCES = [
        'Sulawesi Utara',
        'Sulawesi Tengah', 
        'Sulawesi Selatan',
        'Sulawesi Tenggara',
        'Gorontalo',
        'Sulawesi Barat'
    ]
    
    # Keywords untuk mencari tabel yang relevan
    TABLE_KEYWORDS = [
        'tutupan hutan',
        'kehilangan hutan',
        'deforestasi',
        'laju deforestasi',
        'forest cover',
        'forest loss',
        'luas hutan',
        'kawasan hutan'
    ]
    
    def __init__(self, input_dir: Path, output_dir: Path):
        """
        Initialize extractor.
        
        Args:
            input_dir: Directory containing SLHI PDFs
            output_dir: Output directory untuk hasil ekstraksi
        """
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Initialized SLHI Deforestation Extractor")
        logger.info(f"Input dir: {input_dir}")
        logger.info(f"Output dir: {output_dir}")
    
    def find_slhi_files(self) -> List[Path]:
        """Find all SLHI PDF files."""
        slhi_files = list(self.input_dir.glob("SLHI_*.pdf"))
        slhi_files.sort()
        
        logger.info(f"Found {len(slhi_files)} SLHI PDF files")
        for f in slhi_files:
            logger.info(f"  - {f.name}")
        
        return slhi_files
    
    def extract_year_from_filename(self, filename: str) -> Optional[int]:
        """Extract year dari nama file SLHI."""
        match = re.search(r'SLHI[_\s]*(\d{4})', filename)
        if match:
            return int(match.group(1))
        return None
    
    def extract_tables_from_pdf(
        self,
        pdf_path: Path,
        pages: str = 'all'
    ) -> List[pd.DataFrame]:
        """
        Extract semua tabel dari PDF.
        
        Args:
            pdf_path: Path ke PDF file
            pages: Pages to extract ('all' or '1,2,3')
        
        Returns:
            List of DataFrames
        """
        try:
            logger.info(f"Extracting tables from {pdf_path.name}...")
            
            # Try lattice method first (untuk tabel dengan garis)
            tables = camelot.read_pdf(
                str(pdf_path),
                pages=pages,
                flavor='lattice',
                suppress_stdout=True
            )
            
            if len(tables) == 0:
                # Fallback to stream method (tanpa garis)
                logger.info(f"  No lattice tables found, trying stream method...")
                tables = camelot.read_pdf(
                    str(pdf_path),
                    pages=pages,
                    flavor='stream',
                    suppress_stdout=True
                )
            
            logger.info(f"  Extracted {len(tables)} tables")
            
            return [table.df for table in tables]
            
        except Exception as e:
            logger.error(f"Error extracting from {pdf_path.name}: {e}")
            return []
    
    def is_deforestation_table(self, df: pd.DataFrame) -> bool:
        """
        Check apakah tabel berisi data deforestasi/tutupan hutan.
        
        Args:
            df: DataFrame to check
        
        Returns:
            True jika tabel relevan
        """
        # Convert all cells to lowercase string
        df_str = df.astype(str).apply(lambda x: x.str.lower())
        all_text = ' '.join(df_str.values.flatten())
        
        # Check for keywords
        keyword_found = any(kw in all_text for kw in self.TABLE_KEYWORDS)
        
        # Check for Sulawesi provinces
        sulawesi_found = any(
            prov.lower() in all_text 
            for prov in self.SULAWESI_PROVINCES
        )
        
        return keyword_found and sulawesi_found
    
    def extract_sulawesi_data(
        self,
        df: pd.DataFrame,
        year: int
    ) -> List[Dict]:
        """
        Extract data untuk provinsi Sulawesi dari tabel.
        
        Args:
            df: DataFrame tabel
            year: Tahun sumber data
        
        Returns:
            List of dicts dengan data per provinsi
        """
        extracted_data = []
        
        # Cari baris yang contain nama provinsi Sulawesi
        for idx, row in df.iterrows():
            row_str = ' '.join(row.astype(str)).lower()
            
            for province in self.SULAWESI_PROVINCES:
                if province.lower() in row_str:
                    # Found matching row
                    # Try to extract numerical values
                    numeric_values = []
                    for cell in row:
                        try:
                            # Clean dan parse numbers
                            cleaned = str(cell).replace(',', '').replace('.', '').strip()
                            if cleaned.isdigit():
                                numeric_values.append(float(cleaned))
                        except:
                            pass
                    
                    # Build data point
                    data_point = {
                        'province': province,
                        'year': year,
                        'data_source': f'SLHI_{year}',
                        'confidence_level': 'Medium',
                        'raw_row': str(row.values)
                    }
                    
                    # Assign numeric values (heuristic - needs manual validation)
                    if len(numeric_values) >= 1:
                        data_point['forest_cover_ha'] = numeric_values[0] if len(numeric_values) > 0 else None
                        data_point['forest_cover_pct'] = numeric_values[1] if len(numeric_values) > 1 else None
                        data_point['deforestation_ha'] = numeric_values[2] if len(numeric_values) > 2 else None
                    
                    extracted_data.append(data_point)
                    logger.info(f"    Extracted: {province} - {year}")
                    break
        
        return extracted_data
    
    def process_all_slhi(self) -> pd.DataFrame:
        """
        Process semua SLHI files dan extract deforestation data.
        
        Returns:
            DataFrame dengan semua extracted data
        """
        all_data = []
        slhi_files = self.find_slhi_files()
        
        for pdf_path in slhi_files:
            year = self.extract_year_from_filename(pdf_path.name)
            if not year:
                logger.warning(f"Could not extract year from {pdf_path.name}, skipping")
                continue
            
            logger.info(f"\n Processing {pdf_path.name} (Year: {year})...")
            
            # Extract tables
            tables = self.extract_tables_from_pdf(pdf_path)
            
            # Process each table
            relevant_tables = 0
            for i, df in enumerate(tables):
                if self.is_deforestation_table(df):
                    relevant_tables += 1
                    logger.info(f"  Table {i+1} appears relevant, extracting...")
                    
                    # Extract Sulawesi data
                    extracted = self.extract_sulawesi_data(df, year)
                    all_data.extend(extracted)
            
            logger.info(f"  Found {relevant_tables} relevant tables")
        
        # Consolidate to DataFrame
        if all_data:
            df_final = pd.DataFrame(all_data)
            logger.info(f"\n Total extracted data points: {len(df_final)}")
            return df_final
        else:
            logger.warning("No data extracted!")
            return pd.DataFrame()
    
    def save_results(self, df: pd.DataFrame, filename: str = 'deforestasi_sulawesi_slhi_extracted.csv'):
        """Save extraction results."""
        output_path = self.output_dir / filename
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        logger.info(f"\n✅ Results saved to: {output_path}")
        return output_path


def main():
    """Main execution."""
    logger.info("=" * 70)
    logger.info("EXTRACTING DEFORESTATION DATA FROM SLHI PDFS")
    logger.info("=" * 70)
    
    # Define paths
    input_dir = project_root / 'data' / 'raw' / 'klhk_sulut_kualitas_air'
    output_dir = project_root / 'data' / 'raw' / 'klhk_slhi'
    
    # Initialize extractor
    extractor = SLHIDeforestationExtractor(input_dir, output_dir)
    
    # Process all SLHI files
    df_extracted = extractor.process_all_slhi()
    
    if len(df_extracted) > 0:
        # Display summary
        logger.info("\n" + "=" * 70)
        logger.info("EXTRACTION SUMMARY")
        logger.info("=" * 70)
        logger.info(f"Total rows: {len(df_extracted)}")
        logger.info(f"Provinces covered: {df_extracted['province'].nunique()}")
        logger.info(f"Years covered: {sorted(df_extracted['year'].unique())}")
        
        # Display sample
        logger.info("\nSample extracted data:")
        print(df_extracted.head(10).to_string(index=False))
        
        # Save results
        output_file = extractor.save_results(df_extracted)
        
        logger.info("\n" + "=" * 70)
        logger.info("NEXT STEPS")
        logger.info("=" * 70)
        logger.info("1. Manual validation required:")
        logger.info("   - Check 'raw_row' column untuk verify extraction accuracy")
        logger.info("   - Adjust column mapping in extract_sulawesi_data() if needed")
        logger.info("\n2. Cross-validate dengan GFW data:")
        logger.info("   - Run: python scripts/consolidate_deforestasi.py")
        logger.info("\n3. If extraction quality is low:")
        logger.info("   - Consider manual PDF review untuk complex table structures")
        logger.info("   - Adjust page ranges atau table detection logic")
        
    else:
        logger.error("\n❌ No data extracted. Possible issues:")
        logger.error("1. Table detection keywords need adjustment")
        logger.error("2. PDF structure tidak sesuai dengan expected format")
        logger.error("3. Perlu manual inspection dari PDF files")


if __name__ == "__main__":
    main()
