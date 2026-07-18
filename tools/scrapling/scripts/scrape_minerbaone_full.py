#!/usr/bin/env python3
"""
MinerbaOne Detail Scraper - Sample
Scrape detail + permits untuk sample companies

Usage:
    python sample_detail_minerbaone.py --sample 10
"""

import argparse
import sys
import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import pandas as pd
import time

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))
from scraper_base import BaseScraper


class MinerbaOneDetailScraper(BaseScraper):
    """Scraper untuk detail + permits"""
    
    def __init__(self, delay: float = 1.0, verbose: bool = False, checkpoint_path: Optional[str] = None):
        super().__init__(name="minerbaone_detail", delay=delay, verbose=verbose)
        self.base_url = "https://minerbaone.esdm.go.id"
        
        # Storage
        self.details = []
        self.direksi = []
        self.pemegang_saham = []
        self.permits = []
        
        # Checkpoint
        self.checkpoint_path = Path(checkpoint_path) if checkpoint_path else None
        self.checkpoint_interval = 100  # Save every 100 companies
        self.companies_processed = 0
    
    def fetch_company_detail(self, company_id: str) -> Dict:
        """Fetch detail info (direksi, pemegang saham)"""
        url = f"{self.base_url}/api/common/v2/publik/badan-usaha/{company_id}"
        
        try:
            response = self.fetch_page(url)
            data = response.json()
            
            if data.get('code') == 200 and 'data' in data:
                return data['data']
            
        except Exception as e:
            self.logger.error(f"Error fetching detail for {company_id}: {e}")
        
        return {}
    
    def fetch_company_permits(self, company_id: str) -> List[Dict]:
        """Fetch permits/perizinan"""
        url = f"{self.base_url}/api/common/v2/publik/badan-usaha/{company_id}/list-perizinan"
        
        params = {
            'limit': 100,
            'page': 1
        }
        
        all_permits = []
        
        try:
            while True:
                response = self.fetch_page(url, params=params)
                data = response.json()
                
                if data.get('code') == 200 and 'data' in data:
                    permits_data = data['data'].get('data', [])
                    
                    if not permits_data:
                        break
                    
                    all_permits.extend(permits_data)
                    
                    # Check if there's more pages
                    if data['data'].get('next_page_url'):
                        params['page'] += 1
                    else:
                        break
                else:
                    break
                    
        except Exception as e:
            self.logger.error(f"Error fetching permits for {company_id}: {e}")
        
        return all_permits
    
    def scrape_company(self, company_id: str, company_name: str) -> Dict:
        """Scrape detail + permits untuk 1 company"""
        
        self.logger.info(f"Scraping: {company_name} ({company_id})")
        
        result = {
            'company_id': company_id,
            'company_name': company_name,
            'detail_found': False,
            'permits_found': 0
        }
        
        # 1. Fetch detail (direksi, pemegang saham)
        detail = self.fetch_company_detail(company_id)
        
        if detail:
            result['detail_found'] = True
            
            # Extract detail info
            detail_record = {
                'id_badan_usaha': company_id,
                'nama_badan_usaha': detail.get('nama_badan_usaha'),
                'kode_badan_usaha': detail.get('kode_badan_usaha'),
                'nib': detail.get('nib'),
                'npwp_badan_usaha': detail.get('npwp_badan_usaha'),
                'no_telp': detail.get('no_telp'),
                'email': detail.get('email'),
                'alamat': detail.get('alamat'),
                'kode_pos': detail.get('kode_pos'),
                'rt': detail.get('rt'),
                'rw': detail.get('rw'),
                'jenis_badan_usaha': detail.get('jenis_badan_usaha', {}).get('jenis_badan_usaha'),
                'scraped_at': datetime.now().isoformat()
            }
            self.details.append(detail_record)
            
            # Extract direksi
            for direktur in detail.get('direksi', []):
                direksi_record = {
                    'id_badan_usaha': company_id,
                    'nama_direksi': direktur.get('nama_direksi'),
                    'jabatan': direktur.get('jabatan', {}).get('nama_jabatan'),
                    'tanggal_berlaku': direktur.get('tanggal_berlaku'),
                    'tanggal_berakhir': direktur.get('tanggal_berakhir')
                }
                self.direksi.append(direksi_record)
            
            # Extract pemegang saham
            for pemegang in detail.get('pemegang_saham', []):
                saham_record = {
                    'id_badan_usaha': company_id,
                    'nama_pemegang_saham': pemegang.get('nama_pemegang_saham'),
                    'persentase_saham': pemegang.get('persentase_saham'),
                    'kewarganegaraan': pemegang.get('kewarganegaraan'),
                    'negara': pemegang.get('negara'),
                    'jenis_pemegang_saham': pemegang.get('jenis_pemegang_saham'),
                    'alamat': pemegang.get('alamat')
                }
                self.pemegang_saham.append(saham_record)
        
        # 2. Fetch permits
        permits = self.fetch_company_permits(company_id)
        
        if permits:
            result['permits_found'] = len(permits)
            
            for permit in permits:
                # Safe navigation for nested fields
                jenis_perizinan_obj = permit.get('jenis_perizinan') or {}
                tahap_kegiatan_obj = permit.get('tahap_kegiatan') or {}
                komoditas_obj = permit.get('komoditas') or {}
                golongan_obj = permit.get('golongan') or {}
                status_cnc_obj = permit.get('status_cnc') or {}
                wiup_obj = permit.get('wiup') or {}
                
                permit_record = {
                    'id_badan_usaha': company_id,
                    'id_perizinan': permit.get('id_perizinan'),
                    'nomor_izin': permit.get('nomor_izin'),
                    'jenis_perizinan': jenis_perizinan_obj.get('jenis_perizinan'),
                    'tahap_kegiatan': tahap_kegiatan_obj.get('nama_tahap_kegiatan'),
                    'komoditas': komoditas_obj.get('nama_komoditas'),
                    'golongan': golongan_obj.get('nama_golongan'),
                    'luas_ha': permit.get('luas_ha'),  # ⭐ KEY DATA!
                    'tanggal_berlaku': permit.get('tanggal_berlaku'),
                    'tanggal_berakhir': permit.get('tanggal_berakhir'),
                    'lokasi_perizinan': permit.get('lokasi_perizinan'),
                    'status_cnc': status_cnc_obj.get('status_cnc'),
                    'kode_wiup': wiup_obj.get('nomor_wiup'),
                    'scraped_at': datetime.now().isoformat()
                }
                self.permits.append(permit_record)
        
        return result
    
    def scrape_all(self):
        """Scrape ALL companies (full dataset)"""
        
        # Load companies from Opsi 1
        companies_file = Path("output/minerbaone_companies.csv")
        
        if not companies_file.exists():
            self.logger.error(f"❌ Companies file not found: {companies_file}")
            return
        
        df = pd.read_csv(companies_file)
        total_companies = len(df)
        
        self.logger.info(f"\n{'='*60}")
        self.logger.info(f"Starting FULL scrape: {total_companies} companies")
        self.logger.info(f"Delay: {self.delay}s per request")
        self.logger.info(f"Estimated time: ~{(total_companies * 2 * self.delay / 3600):.1f} hours")
        self.logger.info(f"Checkpoint: every {self.checkpoint_interval} companies")
        self.logger.info(f"{'='*60}\n")
        
        # Progress tracking
        from tqdm import tqdm
        
        for idx, row in tqdm(df.iterrows(), total=total_companies, desc="Scraping companies"):
            company_id = str(row['id_badan_usaha'])
            company_name = row['nama_badan_usaha']
            
            try:
                result = self.scrape_company(company_id, company_name)
                self.companies_processed += 1
                
                # Checkpoint save
                if self.companies_processed % self.checkpoint_interval == 0:
                    if self.checkpoint_path:
                        self.save_checkpoint()
                        self.logger.info(
                            f"💾 Checkpoint: {self.companies_processed}/{total_companies} "
                            f"({self.companies_processed/total_companies*100:.1f}%)"
                        )
                
            except KeyboardInterrupt:
                self.logger.warning("\n⚠️  Interrupted by user!")
                if self.checkpoint_path:
                    self.save_checkpoint()
                    self.logger.info(f"💾 Emergency checkpoint saved")
                raise
            
            except Exception as e:
                self.logger.error(f"❌ Error scraping {company_name}: {e}")
                continue
        
        self.logger.info(f"\n{'='*60}")
        self.logger.info("✅ FULL SCRAPE COMPLETE!")
        self.logger.info(f"{'='*60}")
        self.logger.info(f"Companies processed: {self.companies_processed}")
        self.logger.info(f"Details: {len(self.details)}")
        self.logger.info(f"Direksi: {len(self.direksi)}")
        self.logger.info(f"Pemegang Saham: {len(self.pemegang_saham)}")
        self.logger.info(f"Permits: {len(self.permits)}")
    
    def save_checkpoint(self):
        """Save checkpoint"""
        if not self.checkpoint_path:
            return
        
        checkpoint_data = {
            'timestamp': datetime.now().isoformat(),
            'companies_processed': self.companies_processed,
            'details': self.details,
            'direksi': self.direksi,
            'pemegang_saham': self.pemegang_saham,
            'permits': self.permits
        }
        
        self.checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.checkpoint_path, 'w', encoding='utf-8') as f:
            json.dump(checkpoint_data, f, ensure_ascii=False)
        
        self.logger.debug(f"Checkpoint saved: {self.checkpoint_path}")
        """Scrape sample companies"""
        
        # Load companies from Opsi 1
        companies_file = Path("output/minerbaone_companies.csv")
        
        if not companies_file.exists():
            self.logger.error(f"❌ Companies file not found: {companies_file}")
            return
        
        df = pd.read_csv(companies_file)
        self.logger.info(f"📊 Loaded {len(df)} companies from Opsi 1")
        
        # Get sample (diverse selection)
        sample_df = pd.concat([
            df.head(5),  # First 5
            df.iloc[100:100+sample_size-5]  # Some from middle
        ])
        
        self.logger.info(f"\n{'='*60}")
        self.logger.info(f"Starting sample scrape: {len(sample_df)} companies")
        self.logger.info(f"{'='*60}\n")
        
        for idx, row in sample_df.iterrows():
            company_id = str(row['id_badan_usaha'])
            company_name = row['nama_badan_usaha']
            
            result = self.scrape_company(company_id, company_name)
            
            self.logger.info(
                f"  ✅ Detail: {result['detail_found']}, "
                f"Permits: {result['permits_found']}"
            )
        
        self.logger.info(f"\n{'='*60}")
        self.logger.info("Sample scrape complete!")
        self.logger.info(f"{'='*60}")
        self.logger.info(f"Details: {len(self.details)}")
        self.logger.info(f"Direksi: {len(self.direksi)}")
        self.logger.info(f"Pemegang Saham: {len(self.pemegang_saham)}")
        self.logger.info(f"Permits: {len(self.permits)}")
    
    def export_all(self, output_dir: str = "output/sample"):
        """Export to separate CSVs"""
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Export each table
        tables = {
            'details': self.details,
            'direksi': self.direksi,
            'pemegang_saham': self.pemegang_saham,
            'permits': self.permits
        }
        
        for table_name, data in tables.items():
            if data:
                df = pd.DataFrame(data)
                csv_path = output_path / f"minerbaone_{table_name}.csv"
                df.to_csv(csv_path, index=False, encoding='utf-8-sig')
                self.logger.info(f"📄 {table_name}: {len(data)} rows → {csv_path}")
        
        self.logger.info(f"\n✅ All files exported to {output_dir}/")


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Full detail scraper for MinerbaOne (all 7,527 companies)"
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="Delay between requests in seconds (default: 1.0)"
    )
    parser.add_argument(
        "--output",
        default="output/full",
        help="Output directory (default: output/full/)"
    )
    parser.add_argument(
        "--checkpoint",
        default="output/checkpoint_detail.json",
        help="Checkpoint file path"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    print("="*60)
    print("MinerbaOne Detail Scraper - FULL DATASET")
    print("="*60)
    print(f"Target: 7,527 companies")
    print(f"Delay: {args.delay}s per request")
    print(f"Estimated time: ~{(7527 * 2 * args.delay / 3600):.1f} hours")
    print("="*60)
    print("\n⚠️  This will take several hours!")
    print("💡 You can press Ctrl+C to pause anytime (checkpoint auto-saves)")
    print("="*60)
    
    scraper = MinerbaOneDetailScraper(
        delay=args.delay, 
        verbose=args.verbose,
        checkpoint_path=args.checkpoint
    )
    
    try:
        # Scrape all
        scraper.scrape_all()
        
        # Export
        scraper.export_all(args.output)
        
        print("\n" + "="*60)
        print("✅ FULL SCRAPE COMPLETE!")
        print("="*60)
        print(f"Check {args.output}/ folder for CSV files:")
        print("  - minerbaone_details.csv")
        print("  - minerbaone_direksi.csv")
        print("  - minerbaone_pemegang_saham.csv")
        print("  - minerbaone_permits.csv")
        print("="*60)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Scraping interrupted by user")
        if scraper.checkpoint_path:
            scraper.save_checkpoint()
            print(f"💾 Checkpoint saved: {scraper.checkpoint_path}")
        
        # Export partial data
        scraper.export_all(args.output)
        print(f"\n📊 Partial data exported:")
        print(f"  Companies processed: {scraper.companies_processed}")
        print(f"  Details: {len(scraper.details)}")
        print(f"  Direksi: {len(scraper.direksi)}")
        print(f"  Pemegang Saham: {len(scraper.pemegang_saham)}")
        print(f"  Permits: {len(scraper.permits)}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        
        if scraper.checkpoint_path:
            scraper.save_checkpoint()
            print(f"💾 Emergency checkpoint saved")


if __name__ == "__main__":
    main()
