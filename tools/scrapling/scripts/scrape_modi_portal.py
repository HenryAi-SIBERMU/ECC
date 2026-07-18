#!/usr/bin/env python3
"""
MODI Portal Scraper (modi.esdm.go.id)
CELIOS ECC Intelligence System

Scrape perusahaan mining data dari MODI ESDM Portal
Target: https://modi.esdm.go.id/portal

Usage:
    python scrape_modi_portal.py
    python scrape_modi_portal.py --max-pages 5 --delay 1.5
    python scrape_modi_portal.py --resume output/checkpoint_modi.json
"""

import argparse
import re
import sys
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from tqdm import tqdm
from scrapling.fetchers import StealthyFetcher

# Add parent directory to path for scraper_base import
sys.path.insert(0, str(Path(__file__).parent))
from scraper_base import BaseScraper


class MODIPortalScraper(BaseScraper):
    """Scraper untuk MODI portal (JavaScript SPA)"""
    
    def __init__(
        self,
        delay: float = 1.5,
        max_pages: Optional[int] = None,
        verbose: bool = False,
        checkpoint_path: Optional[str] = None,
        headless: bool = True
    ):
        super().__init__(name="modi", delay=delay, verbose=verbose)
        
        self.base_url = self.config.get("modi", {}).get(
            "base_url",
            "https://modi.esdm.go.id/portal"
        )
        self.max_pages = max_pages
        self.headless = headless
        
        # Data storage for different tables
        self.companies: List[Dict] = []
        self.company_details: List[Dict] = []
        self.directors: List[Dict] = []
        self.shareholders: List[Dict] = []
        self.permits: List[Dict] = []
        
        if checkpoint_path:
            self.checkpoint_path = Path(checkpoint_path)
            self.load_checkpoint(self.checkpoint_path)
    
    def _fetch_js_page(self, url: str, wait_selector: Optional[str] = None) -> BeautifulSoup:
        """
        Fetch page with JavaScript rendering using StealthyFetcher
        
        Args:
            url: URL to fetch
            wait_selector: CSS selector to wait for (optional)
            
        Returns:
            BeautifulSoup object
        """
        self.logger.debug(f"Fetching JS page: {url}")
        
        try:
            # Use StealthyFetcher for JavaScript rendering
            page = StealthyFetcher.fetch(
                url,
                headless=self.headless,
                network_idle=True,
                wait_selector=wait_selector,
                wait_selector_state='attached' if wait_selector else None
            )
            
            self._rate_limit()
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(page.html_content, 'lxml')
            return soup
            
        except Exception as e:
            self.logger.error(f"Error fetching JS page {url}: {e}")
            raise
    
    def _parse_listing_row(self, row) -> Optional[Dict]:
        """
        Parse single listing table row
        
        Expected columns:
        0: No, 1: Nama Badan Usaha, 2: Jenis Badan Usaha, 
        3: Jenis Perizinan, 4: Alamat, 5: Aksi (Detail button)
        
        Args:
            row: BeautifulSoup table row element
            
        Returns:
            Dict dengan data perusahaan atau None
        """
        try:
            cols = row.find_all('td', recursive=False)
            
            if len(cols) < 6:
                return None
            
            # Validate nomor kolom
            nomor_text = cols[0].get_text(strip=True)
            if not nomor_text.isdigit():
                return None
            nomor = int(nomor_text)
            
            # Extract data
            nama = cols[1].get_text(strip=True)
            if not nama:
                return None
            
            jenis_badan_usaha = cols[2].get_text(strip=True)
            jenis_perizinan = cols[3].get_text(strip=True)
            alamat = cols[4].get_text(strip=True)
            
            # Extract detail URL and company_id
            detail_url = None
            company_id = None
            detail_link = cols[5].find('a', href=True)
            
            if detail_link:
                href = detail_link['href']
                detail_url = urljoin(self.base_url, href)
                
                # Extract company_id from URL: /detailPerusahaan/{id}
                match = re.search(r'/detailPerusahaan/(\d+)', href)
                if match:
                    company_id = int(match.group(1))
            
            return {
                "nomor": nomor,
                "nama_badan_usaha": nama,
                "jenis_badan_usaha": jenis_badan_usaha,
                "jenis_perizinan": jenis_perizinan,
                "alamat": alamat,
                "company_id": company_id,
                "detail_url": detail_url,
                "scraped_at": datetime.now().astimezone().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error parsing listing row: {e}")
            return None
    
    def _get_total_pages(self, soup: BeautifulSoup) -> int:
        """
        Hitung total halaman dari pagination info
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            Total jumlah halaman
        """
        # Look for text like "Menampilkan data 1 sampai 10 dari 7527 data"
        pagination_text = soup.find(string=re.compile(r'dari \d+ data'))
        
        if pagination_text:
            match = re.search(r'dari (\d+) data', pagination_text)
            if match:
                total_entries = int(match.group(1))
                rows_per_page = self.config.get("modi", {}).get("rows_per_page", 10)
                total_pages = (total_entries + rows_per_page - 1) // rows_per_page
                
                self.logger.info(
                    f"Found {total_entries} entries, "
                    f"{total_pages} pages (@ {rows_per_page} per page)"
                )
                return total_pages
        
        # Fallback: hitung dari pagination buttons
        pagination = soup.find('ul', class_=re.compile(r'pagination'))
        if pagination:
            page_items = pagination.find_all('li')
            for item in reversed(page_items):
                link = item.find('a')
                if link and link.get_text(strip=True).isdigit():
                    return int(link.get_text(strip=True))
        
        self.logger.warning("Cannot determine total pages, defaulting to 1")
        return 1
    
    def scrape_listing_page(self, page_num: int) -> List[Dict]:
        """
        Scrape single listing page
        
        Args:
            page_num: Nomor halaman (1-indexed)
            
        Returns:
            List of dicts dengan data perusahaan
        """
        # Construct URL (need to determine actual URL pattern)
        # Assuming: /portal?page=1, /portal?page=2, etc.
        if page_num == 1:
            url = self.base_url
        else:
            url = f"{self.base_url}?page={page_num}"
        
        try:
            soup = self._fetch_js_page(url, wait_selector='table')
            
            # Find main table
            table = soup.find('table')
            if not table:
                self.logger.warning(f"No table found on page {page_num}")
                return []
            
            # Parse rows
            rows = table.find('tbody').find_all('tr') if table.find('tbody') else []
            page_data = []
            
            for row in rows:
                entry = self._parse_listing_row(row)
                if entry:
                    page_data.append(entry)
            
            self.logger.info(f"Page {page_num}: scraped {len(page_data)} entries")
            return page_data
            
        except Exception as e:
            self.logger.error(f"Error scraping page {page_num}: {e}")
            return []
    
    def _parse_detail_page(self, soup: BeautifulSoup, company_id: int) -> Dict:
        """
        Parse detail page and extract all nested data
        
        Args:
            soup: BeautifulSoup object dari detail page
            company_id: ID perusahaan
            
        Returns:
            Dict dengan semua detail data
        """
        result = {
            'company_detail': None,
            'directors': [],
            'shareholders': [],
            'permits': []
        }
        
        try:
            # Section 1: Informasi Badan Usaha
            detail = self._parse_company_detail(soup, company_id)
            if detail:
                result['company_detail'] = detail
            
            # Section 2: Susunan Direksi (find table in this section)
            directors = self._parse_directors_table(soup, company_id)
            result['directors'] = directors
            
            # Section 3: Pemegang Saham
            shareholders = self._parse_shareholders_table(soup, company_id)
            result['shareholders'] = shareholders
            
            # Section 4: Daftar Perizinan (MOST IMPORTANT!)
            permits = self._parse_permits_table(soup, company_id)
            result['permits'] = permits
            
        except Exception as e:
            self.logger.error(f"Error parsing detail page for company {company_id}: {e}")
        
        return result
    
    def _parse_company_detail(self, soup: BeautifulSoup, company_id: int) -> Optional[Dict]:
        """Parse Informasi Badan Usaha section"""
        try:
            # Look for section with "Informasi Badan Usaha" heading
            # Extract fields like Nama, Kode, Jenis, NPWP, Alamat, etc.
            # This will need to be adjusted based on actual HTML structure
            
            detail = {
                'company_id': company_id,
                'nama_badan_usaha': '',
                'kode_badan_usaha': company_id,
                'jenis_badan_usaha': '',
                'kelurahan': '',
                'npwp': '',
                'rt_rw': '',
                'kode_pos': '',
                'alamat': '',
                'scraped_at': datetime.now().astimezone().isoformat()
            }
            
            # Extract from page (adjust selectors based on actual structure)
            # This is a placeholder - will need refinement after seeing real HTML
            
            return detail
            
        except Exception as e:
            self.logger.error(f"Error parsing company detail: {e}")
            return None
    
    def _parse_directors_table(self, soup: BeautifulSoup, company_id: int) -> List[Dict]:
        """Parse Susunan Direksi table"""
        directors = []
        
        try:
            # Find directors table (adjust selector based on actual structure)
            # Look for table with columns: No, Nama Direksi, Mulai Menjabat, Akhir Menjabat, Jabatan
            
            # Placeholder logic - will need refinement
            tables = soup.find_all('table')
            
            for table in tables:
                # Check if this is directors table by looking at headers
                headers = [th.get_text(strip=True) for th in table.find_all('th')]
                
                if 'Nama Direksi' in headers or 'Jabatan' in headers:
                    rows = table.find('tbody').find_all('tr') if table.find('tbody') else []
                    
                    for row in rows:
                        cols = row.find_all('td')
                        if len(cols) >= 5:
                            director = {
                                'company_id': company_id,
                                'nama_direksi': cols[1].get_text(strip=True),
                                'mulai_menjabat': cols[2].get_text(strip=True),
                                'akhir_menjabat': cols[3].get_text(strip=True),
                                'jabatan': cols[4].get_text(strip=True)
                            }
                            directors.append(director)
                    break
            
        except Exception as e:
            self.logger.error(f"Error parsing directors: {e}")
        
        return directors
    
    def _parse_shareholders_table(self, soup: BeautifulSoup, company_id: int) -> List[Dict]:
        """Parse Pemegang Saham table"""
        shareholders = []
        
        try:
            # Find shareholders table
            # Columns: No, Jenis Kepemilikan, Nama, Kewarganegaraan, Asal Negara, Persentase Saham
            
            tables = soup.find_all('table')
            
            for table in tables:
                headers = [th.get_text(strip=True) for th in table.find_all('th')]
                
                if 'Persentase Saham' in headers or 'Kewarganegaraan' in headers:
                    rows = table.find('tbody').find_all('tr') if table.find('tbody') else []
                    
                    for row in rows:
                        cols = row.find_all('td')
                        if len(cols) >= 6:
                            shareholder = {
                                'company_id': company_id,
                                'jenis_kepemilikan': cols[1].get_text(strip=True),
                                'nama': cols[2].get_text(strip=True),
                                'kewarganegaraan': cols[3].get_text(strip=True),
                                'asal_negara': cols[4].get_text(strip=True),
                                'persentase_saham': self._parse_float(cols[5].get_text(strip=True))
                            }
                            shareholders.append(shareholder)
                    break
            
        except Exception as e:
            self.logger.error(f"Error parsing shareholders: {e}")
        
        return shareholders
    
    def _parse_permits_table(self, soup: BeautifulSoup, company_id: int) -> List[Dict]:
        """Parse Daftar Perizinan table (MOST IMPORTANT!)"""
        permits = []
        
        try:
            # Find permits table
            # Columns: No, Nomor Izin, Jenis Izin, Tahun Kedaluarsa, Golongan, 
            #          Komoditas, Luas (ha), Tanggal Berlaku, Tanggal Berakhir, 
            #          Status CNC, Lokasi, Kode WIUP
            
            tables = soup.find_all('table')
            
            for table in tables:
                headers = [th.get_text(strip=True) for th in table.find_all('th')]
                
                if 'Nomor Izin' in headers or 'Luas (ha)' in headers or 'Komoditas' in headers:
                    rows = table.find('tbody').find_all('tr') if table.find('tbody') else []
                    
                    for row in rows:
                        cols = row.find_all('td')
                        if len(cols) >= 12:
                            permit = {
                                'company_id': company_id,
                                'nomor_izin': cols[1].get_text(strip=True),
                                'jenis_izin': cols[2].get_text(strip=True),
                                'tahun_kedaluarsa': cols[3].get_text(strip=True),
                                'golongan': cols[4].get_text(strip=True),
                                'komoditas': cols[5].get_text(strip=True),
                                'luas_ha': self._parse_float(cols[6].get_text(strip=True)),
                                'tanggal_berlaku': cols[7].get_text(strip=True),
                                'tanggal_berakhir': cols[8].get_text(strip=True),
                                'status_cnc': cols[9].get_text(strip=True),
                                'lokasi': cols[10].get_text(strip=True),
                                'kode_wiup': cols[11].get_text(strip=True)
                            }
                            permits.append(permit)
                    break
            
        except Exception as e:
            self.logger.error(f"Error parsing permits: {e}")
        
        return permits
    
    def _parse_float(self, text: str) -> Optional[float]:
        """Parse float dari text, handle format Indonesia"""
        try:
            # Remove whitespace
            text = text.strip()
            if not text or text == '-':
                return None
            
            # Replace comma with dot for decimal
            text = text.replace(',', '.')
            
            # Remove non-numeric except dot
            text = re.sub(r'[^\d.]', '', text)
            
            return float(text) if text else None
        except:
            return None
    
    def scrape_detail_page(self, company_id: int) -> Dict:
        """
        Scrape single detail page
        
        Args:
            company_id: ID perusahaan
            
        Returns:
            Dict dengan semua detail data
        """
        url = f"{self.base_url}/detailPerusahaan/{company_id}"
        
        try:
            soup = self._fetch_js_page(url, wait_selector='table')
            result = self._parse_detail_page(soup, company_id)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error scraping detail page {company_id}: {e}")
            return {
                'company_detail': None,
                'directors': [],
                'shareholders': [],
                'permits': []
            }
    
    def scrape_all(self) -> Dict[str, List[Dict]]:
        """
        Scrape semua data (listing + details)
        
        Returns:
            Dict dengan 5 lists: companies, company_details, directors, shareholders, permits
        """
        self.logger.info(f"Starting MODI scrape: {self.base_url}")
        
        # Step 1: Scrape listing pages
        self.logger.info("=" * 60)
        self.logger.info("PHASE 1: Scraping listing pages")
        self.logger.info("=" * 60)
        
        # Fetch first page untuk hitung total pages
        soup = self._fetch_js_page(self.base_url, wait_selector='table')
        total_pages = self._get_total_pages(soup)
        
        # Apply max_pages limit
        if self.max_pages:
            total_pages = min(total_pages, self.max_pages)
            self.logger.info(f"Limiting to {total_pages} pages (max_pages set)")
        
        # Parse first page
        table = soup.find('table')
        if table:
            rows = table.find('tbody').find_all('tr') if table.find('tbody') else []
            for row in rows:
                entry = self._parse_listing_row(row)
                if entry:
                    self.companies.append(entry)
        
        # Scrape remaining pages
        for page_num in tqdm(range(2, total_pages + 1), desc="Scraping listing"):
            page_data = self.scrape_listing_page(page_num)
            self.companies.extend(page_data)
        
        self.logger.info(f"Listing complete: {len(self.companies)} companies")
        
        # Step 2: Scrape detail pages
        self.logger.info("=" * 60)
        self.logger.info("PHASE 2: Scraping detail pages")
        self.logger.info("=" * 60)
        
        checkpoint_interval = self.config.get("modi", {}).get("checkpoint_interval", 100)
        
        for idx, company in enumerate(tqdm(self.companies, desc="Scraping details")):
            company_id = company.get('company_id')
            
            if not company_id:
                continue
            
            # Scrape detail
            detail_data = self.scrape_detail_page(company_id)
            
            # Store data
            if detail_data['company_detail']:
                self.company_details.append(detail_data['company_detail'])
            
            self.directors.extend(detail_data['directors'])
            self.shareholders.extend(detail_data['shareholders'])
            self.permits.extend(detail_data['permits'])
            
            # Save checkpoint
            if (idx + 1) % checkpoint_interval == 0 and self.checkpoint_path:
                self.save_checkpoint()
        
        self.logger.info(f"Detail scraping complete!")
        self.logger.info(f"  Companies: {len(self.companies)}")
        self.logger.info(f"  Details: {len(self.company_details)}")
        self.logger.info(f"  Directors: {len(self.directors)}")
        self.logger.info(f"  Shareholders: {len(self.shareholders)}")
        self.logger.info(f"  Permits: {len(self.permits)}")
        
        return {
            'companies': self.companies,
            'company_details': self.company_details,
            'directors': self.directors,
            'shareholders': self.shareholders,
            'permits': self.permits
        }
    
    def save_checkpoint(self, checkpoint_path: Optional[Path] = None):
        """Override to save all data tables"""
        if checkpoint_path is None:
            checkpoint_path = self.checkpoint_path
        
        if checkpoint_path is None:
            return
        
        checkpoint_data = {
            "scraper": self.name,
            "timestamp": datetime.now().isoformat(),
            "companies": self.companies,
            "company_details": self.company_details,
            "directors": self.directors,
            "shareholders": self.shareholders,
            "permits": self.permits
        }
        
        checkpoint_path = Path(checkpoint_path)
        checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
        
        import json
        with open(checkpoint_path, 'w', encoding='utf-8') as f:
            json.dump(checkpoint_data, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"Checkpoint saved: {checkpoint_path}")
    
    def load_checkpoint(self, checkpoint_path: Path):
        """Override to load all data tables"""
        try:
            import json
            with open(checkpoint_path, 'r', encoding='utf-8') as f:
                checkpoint = json.load(f)
            
            self.companies = checkpoint.get("companies", [])
            self.company_details = checkpoint.get("company_details", [])
            self.directors = checkpoint.get("directors", [])
            self.shareholders = checkpoint.get("shareholders", [])
            self.permits = checkpoint.get("permits", [])
            
            self.logger.info(
                f"Resumed from checkpoint: {len(self.companies)} companies loaded"
            )
            
        except FileNotFoundError:
            self.logger.warning("No checkpoint found, starting fresh")
    
    def export_all(self, output_dir: str = "output"):
        """Export all data tables to separate CSV files"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        try:
            import pandas as pd
            
            # Export each table
            tables = {
                'companies': self.companies,
                'company_details': self.company_details,
                'directors': self.directors,
                'shareholders': self.shareholders,
                'permits': self.permits
            }
            
            for table_name, data in tables.items():
                if data:
                    df = pd.DataFrame(data)
                    csv_path = output_path / f"modi_{table_name}.csv"
                    df.to_csv(csv_path, index=False, encoding='utf-8-sig')
                    self.logger.info(f"Exported {len(data)} {table_name} to {csv_path}")
            
            # Also export combined JSON
            json_path = output_path / "modi_complete.json"
            import json
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(tables, f, ensure_ascii=False, indent=2)
            self.logger.info(f"Exported combined data to {json_path}")
            
        except ImportError:
            self.logger.error("pandas not installed, cannot export CSV")


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Scrape mining company data dari MODI portal"
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        help="Maximum number of listing pages to scrape"
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=1.5,
        help="Delay between requests in seconds (default: 1.5)"
    )
    parser.add_argument(
        "--output",
        default="output",
        help="Output directory path (default: output/)"
    )
    parser.add_argument(
        "--checkpoint",
        default="output/checkpoint_modi.json",
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
    parser.add_argument(
        "--no-headless",
        action="store_true",
        help="Show browser window (for debugging)"
    )
    
    args = parser.parse_args()
    
    # Create scraper
    checkpoint_path = args.resume or args.checkpoint
    scraper = MODIPortalScraper(
        delay=args.delay,
        max_pages=args.max_pages,
        verbose=args.verbose,
        checkpoint_path=checkpoint_path,
        headless=not args.no_headless
    )
    
    # Scrape
    try:
        scraper.scrape_all()
        
        # Export all tables
        scraper.export_all(args.output)
        
        # Final checkpoint
        if checkpoint_path:
            scraper.save_checkpoint()
        
        print(f"\n✅ Success! Scraped data:")
        print(f"   📊 Companies: {len(scraper.companies)}")
        print(f"   📋 Details: {len(scraper.company_details)}")
        print(f"   👔 Directors: {len(scraper.directors)}")
        print(f"   💼 Shareholders: {len(scraper.shareholders)}")
        print(f"   📜 Permits: {len(scraper.permits)}")
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
