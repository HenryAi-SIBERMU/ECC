#!/usr/bin/env python3
"""
MinerbaOne ESDM Scraper
CELIOS ECC Intelligence System

Scrape data perusahaan tambang dari MinerbaOne API
Target: https://minerbaone.esdm.go.id/api/common/v2/publik/badan-usaha

Usage:
    python scrape_minerbaone.py
    python scrape_minerbaone.py --max-pages 5 --delay 0.5
    python scrape_minerbaone.py --resume output/checkpoint_minerbaone.json
"""

import argparse
import sys
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

from tqdm import tqdm

# Add parent directory to path for scraper_base import
sys.path.insert(0, str(Path(__file__).parent))
from scraper_base import BaseScraper


class MinerbaOneScraper(BaseScraper):
    """Scraper untuk MinerbaOne API"""
    
    def __init__(
        self,
        delay: float = 0.5,
        max_pages: Optional[int] = None,
        items_per_page: int = 100,
        verbose: bool = False,
        checkpoint_path: Optional[str] = None
    ):
        super().__init__(name="minerbaone", delay=delay, verbose=verbose)
        
        self.api_url = "https://minerbaone.esdm.go.id/api/common/v2/publik/badan-usaha"
        self.max_pages = max_pages
        self.items_per_page = items_per_page
        
        # Data storage
        self.companies: List[Dict] = []
        
        if checkpoint_path:
            self.checkpoint_path = Path(checkpoint_path)
            self.load_checkpoint(self.checkpoint_path)
    
    def fetch_page_data(self, page_num: int) -> Dict:
        """
        Fetch data dari API untuk satu halaman
        
        Args:
            page_num: Nomor halaman (1-indexed)
            
        Returns:
            Dict dengan response API
        """
        params = {
            'sort': 'nama_badan_usaha',
            'page': page_num,
            'limit': self.items_per_page,
            'search': ''
        }
        
        try:
            response = self.fetch_page(self.api_url, params=params)
            data = response.json()
            
            return data
            
        except Exception as e:
            self.logger.error(f"Error fetching page {page_num}: {e}")
            return {}
    
    def scrape_page(self, page_num: int) -> List[Dict]:
        """
        Scrape single page dan extract data
        
        Args:
            page_num: Nomor halaman
            
        Returns:
            List of companies
        """
        data = self.fetch_page_data(page_num)
        
        if not data:
            return []
        
        # Debug: save first page response
        if page_num == 1:
            import json
            debug_path = Path("output/minerbaone_api_response.json")
            debug_path.parent.mkdir(exist_ok=True)
            with open(debug_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Debug: API response saved to {debug_path}")
        
        # Extract companies dari response
        # API structure: {"message": "Success", "data": {"current_page": 1, "data": [...]}}
        companies = []
        
        if isinstance(data, dict):
            # MinerbaOne specific: data.data contains the actual list
            if 'data' in data and isinstance(data['data'], dict):
                items = data['data'].get('data', [])
            # Fallback: try common keys
            elif 'data' in data:
                items = data['data'] if isinstance(data['data'], list) else []
            else:
                items = (
                    data.get('results') or 
                    data.get('items') or 
                    data.get('records') or
                    []
                )
        elif isinstance(data, list):
            items = data
        else:
            items = []
        
        for item in items:
            # Handle both dict and primitive types
            if isinstance(item, dict):
                item['scraped_at'] = datetime.now().astimezone().isoformat()
                
                # Add detail_url based on id_badan_usaha
                if 'id_badan_usaha' in item:
                    item['detail_url'] = f"https://minerbaone.esdm.go.id/publik/badan-usaha/{item['id_badan_usaha']}"
                
                companies.append(item)
            else:
                # If item is string/primitive, wrap it
                companies.append({
                    'raw_data': item,
                    'scraped_at': datetime.now().astimezone().isoformat()
                })
        
        self.logger.info(f"Page {page_num}: scraped {len(companies)} companies")
        
        return companies
    
    def get_total_info(self) -> Dict:
        """
        Get total count dari API (fetch page 1)
        
        Returns:
            Dict dengan info total entries dan pages
        """
        data = self.fetch_page_data(1)
        
        if not data:
            return {'total_entries': 0, 'total_pages': 1}
        
        # MinerbaOne API structure: {"data": {"total": 1234, "last_page": 123, ...}}
        if isinstance(data, dict) and 'data' in data and isinstance(data['data'], dict):
            pagination_data = data['data']
            total_entries = pagination_data.get('total', 0)
            last_page = pagination_data.get('last_page', 1)
            
            return {
                'total_entries': total_entries,
                'total_pages': last_page
            }
        
        # Fallback: extract total dari response
        total_entries = (
            data.get('total') or
            data.get('count') or
            data.get('totalCount') or
            data.get('total_count') or
            len(data.get('data', []))
        )
        
        total_pages = (total_entries + self.items_per_page - 1) // self.items_per_page
        
        return {
            'total_entries': total_entries,
            'total_pages': total_pages
        }
    
    def scrape_all(self) -> List[Dict]:
        """
        Scrape semua data dari API
        
        Returns:
            List of all companies
        """
        self.logger.info(f"Starting MinerbaOne scrape: {self.api_url}")
        
        # Get total info
        info = self.get_total_info()
        total_entries = info['total_entries']
        total_pages = info['total_pages']
        
        self.logger.info(
            f"Found {total_entries} entries, "
            f"{total_pages} pages (@ {self.items_per_page} per page)"
        )
        
        # Apply max_pages limit
        if self.max_pages:
            total_pages = min(total_pages, self.max_pages)
            self.logger.info(f"Limiting to {total_pages} pages (max_pages set)")
        
        # Scrape all pages dengan progress bar
        checkpoint_interval = 10  # Save every 10 pages
        
        for page_num in tqdm(range(1, total_pages + 1), desc="Scraping pages"):
            page_data = self.scrape_page(page_num)
            self.companies.extend(page_data)
            
            # Save checkpoint
            if page_num % checkpoint_interval == 0 and self.checkpoint_path:
                self.save_checkpoint()
        
        self.logger.info(f"Scraping complete: {len(self.companies)} companies")
        
        return self.companies
    
    def save_checkpoint(self, checkpoint_path: Optional[Path] = None):
        """Save checkpoint"""
        if checkpoint_path is None:
            checkpoint_path = self.checkpoint_path
        
        if checkpoint_path is None:
            return
        
        checkpoint_data = {
            "scraper": self.name,
            "timestamp": datetime.now().isoformat(),
            "companies_scraped": len(self.companies),
            "companies": self.companies
        }
        
        checkpoint_path = Path(checkpoint_path)
        checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
        
        import json
        with open(checkpoint_path, 'w', encoding='utf-8') as f:
            json.dump(checkpoint_data, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"Checkpoint saved: {checkpoint_path}")
    
    def load_checkpoint(self, checkpoint_path: Path):
        """Load checkpoint"""
        try:
            import json
            with open(checkpoint_path, 'r', encoding='utf-8') as f:
                checkpoint = json.load(f)
            
            self.companies = checkpoint.get("companies", [])
            
            self.logger.info(
                f"Resumed from checkpoint: {len(self.companies)} companies loaded"
            )
            
        except FileNotFoundError:
            self.logger.warning("No checkpoint found, starting fresh")
    
    def export_all(self, output_dir: str = "output"):
        """Export data to CSV and JSON"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        try:
            import pandas as pd
            
            # Export CSV
            if self.companies:
                df = pd.DataFrame(self.companies)
                csv_path = output_path / "minerbaone_companies.csv"
                df.to_csv(csv_path, index=False, encoding='utf-8-sig')
                self.logger.info(f"Exported {len(self.companies)} companies to {csv_path}")
            
            # Export JSON
            json_path = output_path / "minerbaone_companies.json"
            import json
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(self.companies, f, ensure_ascii=False, indent=2)
            self.logger.info(f"Exported to {json_path}")
            
        except ImportError:
            self.logger.error("pandas not installed, cannot export CSV")


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Scrape mining company data dari MinerbaOne API"
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        help="Maximum number of pages to scrape"
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.5,
        help="Delay between requests in seconds (default: 0.5)"
    )
    parser.add_argument(
        "--items-per-page",
        type=int,
        default=100,
        help="Items per page (default: 100, max mungkin 100)"
    )
    parser.add_argument(
        "--output",
        default="output",
        help="Output directory path (default: output/)"
    )
    parser.add_argument(
        "--checkpoint",
        default="output/checkpoint_minerbaone.json",
        help="Checkpoint file path for pause/resume"
    )
    parser.add_argument(
        "--resume",
        help="Resume from checkpoint file"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    # Create scraper
    checkpoint_path = args.resume or args.checkpoint
    scraper = MinerbaOneScraper(
        delay=args.delay,
        max_pages=args.max_pages,
        items_per_page=args.items_per_page,
        verbose=args.verbose,
        checkpoint_path=checkpoint_path
    )
    
    # Scrape
    try:
        scraper.scrape_all()
        
        # Export
        scraper.export_all(args.output)
        
        # Final checkpoint
        if checkpoint_path:
            scraper.save_checkpoint()
        
        print(f"\n✅ Success! Scraped {len(scraper.companies)} companies")
        print(f"📁 Output: {args.output}/")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Scraping interrupted by user")
        if checkpoint_path:
            scraper.save_checkpoint()
            print(f"💾 Checkpoint saved: {checkpoint_path}")
        print(f"📊 Scraped {len(scraper.companies)} companies so far")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        if checkpoint_path and scraper.companies:
            scraper.save_checkpoint()
            print(f"💾 Emergency checkpoint saved: {checkpoint_path}")
        raise


if __name__ == "__main__":
    main()
