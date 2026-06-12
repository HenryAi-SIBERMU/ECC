#!/usr/bin/env python3
"""
TanahKita.id Scraper
CELIOS ECC Intelligence System

Scrape data konflik lahan dari https://tanahkita.id/data-konflik

Usage:
    python scrape_tanahkita.py
    python scrape_tanahkita.py --max-pages 5 --delay 1.0
    python scrape_tanahkita.py --resume output/checkpoint.json
"""

import argparse
import re
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
from urllib.parse import urljoin, urlencode

from bs4 import BeautifulSoup
from tqdm import tqdm

from scraper_base import BaseScraper


class TanahKitaScraper(BaseScraper):
    """Scraper untuk tanahkita.id data konflik"""
    
    def __init__(
        self,
        delay: float = 0.8,
        max_pages: Optional[int] = None,
        verbose: bool = False,
        checkpoint_path: Optional[str] = None
    ):
        super().__init__(name="tanahkita", delay=delay, verbose=verbose)
        
        self.base_url = self.config.get("tanahkita", {}).get(
            "base_url",
            "https://tanahkita.id/data-konflik"
        )
        self.max_pages = max_pages
        
        if checkpoint_path:
            self.checkpoint_path = Path(checkpoint_path)
            self.load_checkpoint(self.checkpoint_path)
    
    def _parse_table_row(self, row) -> Optional[Dict]:
        """
        Parse single table row menjadi dict
        
        Table structure can be either:
        - 8 columns (with nested table in col 4)
        - 7 columns (without nested table)
        
        8-column structure:
        0: No, 1: Tahun, 2: Judul, 3: Deskripsi, 
        4: Nested table, 5: Lokasi, 6: Status, 7: Detail
        
        7-column structure:
        0: No, 1: Tahun, 2: Judul, 3: Deskripsi,
        4: Lokasi, 5: Status, 6: Detail
        
        Args:
            row: BeautifulSoup table row element
            
        Returns:
            Dict dengan data konflik atau None jika parsing gagal
        """
        try:
            cols = row.find_all('td', recursive=False)
            
            # Accept both 7 and 8 columns
            if len(cols) not in [7, 8]:
                return None
            
            # Validate nomor kolom - must be digit
            nomor_text = cols[0].get_text(strip=True)
            if not nomor_text.isdigit():
                return None
            nomor = int(nomor_text)
            
            # Validate tahun kolom - must be digit
            tahun_text = cols[1].get_text(strip=True)
            if not tahun_text.isdigit():
                return None
            tahun = int(tahun_text)
            
            # Column 2: Judul
            judul = cols[2].get_text(strip=True)
            if not judul:  # Skip if judul empty
                return None
            
            # Column 3: Deskripsi
            deskripsi = cols[3].get_text(strip=True)
            
            # Determine column indices based on total columns
            if len(cols) == 8:
                # Has nested table in col 4, skip it
                lokasi_idx = 5
                status_idx = 6
                detail_idx = 7
            else:  # 7 columns
                lokasi_idx = 4
                status_idx = 5
                detail_idx = 6
            
            # Lokasi
            lokasi = cols[lokasi_idx].get_text(strip=True)
            
            # Status badge
            status = ""
            status_badge = cols[status_idx].find(class_='badge')
            if status_badge:
                status = status_badge.get_text(strip=True)
            else:
                status = cols[status_idx].get_text(strip=True)
            
            # Detail URL
            detail_url = None
            link = cols[detail_idx].find('a', href=True)
            if link:
                detail_url = urljoin(self.base_url, link['href'])
            
            return {
                "nomor": nomor,
                "tahun": tahun,
                "judul": judul,
                "deskripsi": deskripsi,
                "lokasi": lokasi,
                "status": status,
                "detail_url": detail_url,
                "scraped_at": datetime.now().astimezone().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error parsing row: {e}")
            return None
    
    def _get_total_pages(self, soup: BeautifulSoup) -> int:
        """
        Hitung total halaman dari pagination info
        
        Args:
            soup: BeautifulSoup object dari halaman pertama
            
        Returns:
            Total jumlah halaman
        """
        # Cari text "1 - 10 of 580 entries"
        pagination_text = soup.find(string=re.compile(r'of \d+ entries'))
        
        if pagination_text:
            match = re.search(r'of (\d+) entries', pagination_text)
            if match:
                total_entries = int(match.group(1))
                rows_per_page = self.config.get("tanahkita", {}).get("rows_per_page", 10)
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
            # Last button sebelum "next" biasanya nomor page terakhir
            for item in reversed(page_items):
                link = item.find('a')
                if link and link.get_text(strip=True).isdigit():
                    return int(link.get_text(strip=True))
        
        self.logger.warning("Cannot determine total pages, defaulting to 1")
        return 1
    
    def scrape_page(self, page_num: int) -> List[Dict]:
        """
        Scrape single page
        
        Args:
            page_num: Nomor halaman (1-indexed)
            
        Returns:
            List of dicts dengan data konflik
        """
        # Construct URL dengan offset (10 entries per page)
        # Page 1: /data/konflik
        # Page 2: /data/konflik/index/10
        # Page 3: /data/konflik/index/20
        if page_num == 1:
            url = self.base_url
        else:
            offset = (page_num - 1) * 10
            url = f"{self.base_url}/index/{offset}"
        
        try:
            response = self.fetch_page(url)
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Find table
            table = soup.find('table')
            if not table:
                self.logger.warning(f"No table found on page {page_num}")
                return []
            
            # Parse rows
            rows = table.find('tbody').find_all('tr') if table.find('tbody') else []
            page_data = []
            
            for row in rows:
                entry = self._parse_table_row(row)
                if entry:
                    page_data.append(entry)
            
            self.logger.info(f"Page {page_num}: scraped {len(page_data)} entries")
            return page_data
            
        except Exception as e:
            self.logger.error(f"Error scraping page {page_num}: {e}")
            return []
    
    def scrape_all(self) -> List[Dict]:
        """
        Scrape semua halaman
        
        Returns:
            List of dicts dengan semua data konflik
        """
        self.logger.info(f"Starting scrape: {self.base_url}")
        
        # Fetch first page untuk hitung total pages
        response = self.fetch_page(self.base_url)
        soup = BeautifulSoup(response.content, 'lxml')
        
        total_pages = self._get_total_pages(soup)
        
        # Apply max_pages limit jika ada
        if self.max_pages:
            total_pages = min(total_pages, self.max_pages)
            self.logger.info(f"Limiting to {total_pages} pages (max_pages set)")
        
        # Parse first page
        table = soup.find('table')
        if table:
            rows = table.find('tbody').find_all('tr') if table.find('tbody') else []
            for row in rows:
                entry = self._parse_table_row(row)
                if entry:
                    self.data.append(entry)
        
        # Scrape remaining pages dengan progress bar
        checkpoint_interval = self.config.get("tanahkita", {}).get(
            "checkpoint_interval",
            50
        )
        
        for page_num in tqdm(range(2, total_pages + 1), desc="Scraping pages"):
            page_data = self.scrape_page(page_num)
            self.data.extend(page_data)
            
            # Save checkpoint setiap N entries
            if len(self.data) % checkpoint_interval == 0 and self.checkpoint_path:
                self.save_checkpoint()
        
        self.logger.info(f"Scraping complete: {len(self.data)} entries")
        return self.data


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Scrape konflik lahan data dari tanahkita.id"
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        help="Maximum number of pages to scrape"
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.8,
        help="Delay between requests in seconds (default: 0.8)"
    )
    parser.add_argument(
        "--output",
        default="output/tanahkita_konflik.csv",
        help="Output file path (default: output/tanahkita_konflik.csv)"
    )
    parser.add_argument(
        "--checkpoint",
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
    scraper = TanahKitaScraper(
        delay=args.delay,
        max_pages=args.max_pages,
        verbose=args.verbose,
        checkpoint_path=checkpoint_path
    )
    
    # Scrape
    try:
        scraper.scrape_all()
        
        # Export
        output_path = Path(args.output)
        
        if output_path.suffix == '.csv':
            scraper.export_csv(output_path)
        elif output_path.suffix == '.json':
            scraper.export_json(output_path)
        else:
            # Default: export both
            scraper.export_csv(output_path.with_suffix('.csv'))
            scraper.export_json(output_path.with_suffix('.json'))
        
        # Final checkpoint
        if checkpoint_path:
            scraper.save_checkpoint()
        
        print(f"\n✅ Success! Scraped {len(scraper.data)} entries")
        print(f"📁 Output: {output_path}")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Scraping interrupted by user")
        if checkpoint_path:
            scraper.save_checkpoint()
            print(f"💾 Checkpoint saved: {checkpoint_path}")
        print(f"📊 Scraped {len(scraper.data)} entries so far")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        if checkpoint_path and scraper.data:
            scraper.save_checkpoint()
            print(f"💾 Emergency checkpoint saved: {checkpoint_path}")
        raise


if __name__ == "__main__":
    main()
