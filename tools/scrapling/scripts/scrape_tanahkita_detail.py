#!/usr/bin/env python3
"""
TanahKita Detail Scraper
Scrape halaman detail konflik dari TanahKita.id termasuk ekstraksi kriminalisasi dari narasi

Usage:
    python scrape_tanahkita_detail.py --test 2   # Test dengan 2 halaman
    python scrape_tanahkita_detail.py --all      # Run semua 178 kasus
"""

import argparse
import sys
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import pandas as pd
import time
from bs4 import BeautifulSoup

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))
from scraper_base import BaseScraper


class TanahKitaDetailScraper(BaseScraper):
    """Scraper untuk halaman detail TanahKita.id"""
    
    def __init__(self, delay: float = 1.5, verbose: bool = False, checkpoint_path: Optional[str] = None):
        super().__init__(name="tanahkita_detail", delay=delay, verbose=verbose)
        self.base_url = "https://tanahkita.id"
        
        # Storage
        self.details = []
        
        # Checkpoint
        self.checkpoint_path = Path(checkpoint_path) if checkpoint_path else None
        self.checkpoint_interval = 10  # Save every 10 cases
        self.cases_processed = 0
        
        # Regex patterns untuk kriminalisasi
        self.kriminalisasi_patterns = {
            'kriminalisasi': r'kriminalisas[i]',
            'ditangkap': r'ditangkap|penangkapan|penahanan|ditahan|tangkap',
            'aparat': r'polisi|polda|polres|polsek|polhut|TNI|tentara|satpol\s*pp|aparat',
            'kekerasan': r'kekerasan|intimidasi|ancaman|teror|diusir|dipukul|penganiayaan',
            'korban_fisik': r'luka|terluka|tewas|meninggal|cedera|dipukul|disiksa'
        }
        
        # Regex untuk ekstraksi angka
        self.number_patterns = {
            'ditangkap': r'(\d+)\s*(?:orang)?\s*(?:warga|petani|masyarakat|aktivis)?\s*(?:di)?(?:tangkap|ditahan|ditangkap)',
            'luka': r'(\d+)\s*(?:orang)?\s*(?:luka|terluka|cedera)',
            'tewas': r'(\d+)\s*(?:orang)?\s*(?:tewas|meninggal|terbunuh)'
        }
    
    def fix_detail_url(self, url: str) -> str:
        """
        Fix bug URL: /data/data/konflik/ → /data/konflik/
        """
        if '/data/data/konflik/' in url:
            fixed = url.replace('/data/data/konflik/', '/data/konflik/')
            self.logger.debug(f"URL fixed: {url} → {fixed}")
            return fixed
        return url
    
    def extract_text_from_table(self, soup: BeautifulSoup, label: str) -> Optional[str]:
        """
        Extract teks dari tabel HTML dengan label tertentu
        TanahKita uses format: <tr><td>Label</td><td>:</td><td>Value</td></tr>
        """
        try:
            # Find all rows
            rows = soup.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 3:
                    # First cell is label
                    cell_text = cells[0].get_text(strip=True)
                    if label.lower() in cell_text.lower():
                        # Third cell is value (cells[1] is ":")
                        value = cells[2].get_text(strip=True)
                        return value if value else None
            return None
        except Exception as e:
            self.logger.error(f"Error extracting {label}: {e}")
            return None
    
    def parse_luas_ha(self, text: str) -> Optional[float]:
        """
        Parse luas lahan dari text seperti "1250 Ha" atau "0,00 Ha"
        Return: float atau None
        """
        if not text:
            return None
        
        try:
            # Extract angka dari text (support format Indonesia: 1.250,50)
            # Remove "Ha" dan whitespace
            clean_text = text.replace('Ha', '').replace('ha', '').strip()
            
            # Replace Indonesian decimal separator
            clean_text = clean_text.replace('.', '').replace(',', '.')
            
            # Extract first number found
            match = re.search(r'[\d.]+', clean_text)
            if match:
                return float(match.group())
        except:
            pass
        
        return None
    
    def parse_dampak_jiwa(self, text: str) -> Optional[int]:
        """
        Parse dampak masyarakat dari text seperti "150 Jiwa"
        Return: int atau None
        """
        if not text:
            return None
        
        try:
            # Extract angka dari text
            match = re.search(r'(\d+)', text)
            if match:
                return int(match.group(1))
        except:
            pass
        
        return None
    
    def extract_narasi(self, soup: BeautifulSoup) -> str:
        """
        Extract narasi lengkap dari halaman detail
        Look for the main content area after the data table
        """
        try:
            # Strategy 1: Find the section after "DATA DETIL" title
            # The narrative is usually in a div/section after the table
            
            # Look for heading "Kronologi" or "Narasi" or large text blocks
            headings = soup.find_all(['h2', 'h3', 'h4'])
            for heading in headings:
                heading_text = heading.get_text(strip=True).lower()
                if any(keyword in heading_text for keyword in ['kronologi', 'narasi', 'deskripsi', 'detail']):
                    # Get all following siblings until next heading
                    narasi_parts = []
                    for sibling in heading.find_next_siblings():
                        if sibling.name in ['h1', 'h2', 'h3', 'h4']:
                            break
                        text = sibling.get_text(strip=True)
                        if text:
                            narasi_parts.append(text)
                    if narasi_parts:
                        return '\n'.join(narasi_parts)
            
            # Strategy 2: Find the table, then get content after it
            tables = soup.find_all('table')
            if tables:
                # Get content after first table
                main_table = tables[0]
                narasi_parts = []
                for sibling in main_table.find_all_next(['p', 'div']):
                    text = sibling.get_text(strip=True)
                    if len(text) > 100:  # Only long paragraphs
                        narasi_parts.append(text)
                        if len('\n'.join(narasi_parts)) > 500:  # Got enough
                            break
                if narasi_parts:
                    return '\n'.join(narasi_parts)
            
            # Strategy 3: Find all paragraphs and combine
            paragraphs = soup.find_all('p')
            if paragraphs:
                all_text = '\n'.join([p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 50])
                if len(all_text) > 200:
                    return all_text
            
            # Strategy 4: Fallback - get text from main content area
            content_areas = soup.find_all(['div'], class_=re.compile(r'content|main|body|detail', re.I))
            for area in content_areas:
                text = area.get_text(separator='\n', strip=True)
                if len(text) > 300:
                    return text
            
            return ""
            
        except Exception as e:
            self.logger.error(f"Error extracting narasi: {e}")
            return ""
    
    def detect_kriminalisasi(self, narasi: str) -> Tuple[bool, List[str], Dict[str, int], List[str]]:
        """
        Detect kriminalisasi dari narasi text menggunakan regex
        
        Returns:
            - indikasi_kriminalisasi (bool)
            - bukti_teks (list of matching sentences)
            - jumlah (dict: ditangkap, luka, tewas)
            - aktor (list of actors: Polisi, TNI, etc)
        """
        if not narasi:
            return False, [], {'ditangkap': 0, 'luka': 0, 'tewas': 0}, []
        
        narasi_lower = narasi.lower()
        bukti_sentences = []
        aktor_list = []
        jumlah = {'ditangkap': 0, 'luka': 0, 'tewas': 0}
        
        # Split narasi menjadi kalimat
        sentences = re.split(r'[.!?\n]+', narasi)
        
        # 1. Cek pattern kriminalisasi
        found_kriminalisasi = False
        for pattern_name, pattern in self.kriminalisasi_patterns.items():
            if re.search(pattern, narasi_lower):
                found_kriminalisasi = True
                
                # Ambil kalimat yang mengandung pattern
                for sentence in sentences:
                    if re.search(pattern, sentence.lower()):
                        bukti_sentences.append(sentence.strip())
        
        # 2. Extract aktor (Polisi, TNI, Satpol PP)
        if re.search(r'\bpolisi\b|\bpolda\b|\bpolres\b|\bpolhut\b|polisi\s*hutan', narasi_lower, re.I):
            aktor_list.append('Polisi')
        if re.search(r'\bTNI\b|\btentara\b', narasi_lower, re.I):
            aktor_list.append('TNI')
        if re.search(r'satpol\s*pp', narasi_lower, re.I):
            aktor_list.append('Satpol PP')
        
        # 3. Extract jumlah korban
        for key, pattern in self.number_patterns.items():
            matches = re.findall(pattern, narasi_lower)
            if matches:
                # Ambil angka terbesar yang ditemukan
                numbers = [int(m) for m in matches if m.isdigit()]
                if numbers:
                    jumlah[key] = max(numbers)
        
        # Remove duplicates dari bukti
        bukti_sentences = list(set(bukti_sentences))[:5]  # Max 5 kalimat bukti
        aktor_list = list(set(aktor_list))
        
        return found_kriminalisasi, bukti_sentences, jumlah, aktor_list
    
    def scrape_detail_page(self, row: pd.Series) -> Dict:
        """
        Scrape 1 halaman detail konflik
        """
        nomor = row['nomor']
        judul = row['judul']
        detail_url = row['detail_url']
        
        self.logger.info(f"[{nomor}] Scraping: {judul[:50]}...")
        
        # Fix URL bug
        fixed_url = self.fix_detail_url(detail_url)
        
        result = {
            'nomor': nomor,
            'luas_ha': None,
            'dampak_jiwa': None,
            'nilai_investasi': None,
            'aktor_pemerintah': False,
            'aktor_perusahaan': False,
            'aktor_masyarakat': False,
            'narasi_lengkap': "",
            'indikasi_kriminalisasi': False,
            'bukti_teks_kriminalisasi': "",
            'jumlah_ditangkap': 0,
            'jumlah_luka': 0,
            'jumlah_tewas': 0,
            'aktor_kriminalisasi': "",
            'detail_scraped_at': datetime.now().isoformat(),
            'scraping_success': False,
            'error_message': None
        }
        
        try:
            # Fetch page
            response = self.fetch_page(fixed_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 1. Extract structured data dari tabel
            luas_text = self.extract_text_from_table(soup, 'Luas')
            if luas_text:
                result['luas_ha'] = self.parse_luas_ha(luas_text)
            
            dampak_text = self.extract_text_from_table(soup, 'Dampak')
            if dampak_text:
                result['dampak_jiwa'] = self.parse_dampak_jiwa(dampak_text)
            
            investasi_text = self.extract_text_from_table(soup, 'Investasi')
            if investasi_text:
                result['nilai_investasi'] = investasi_text
            
            # 2. Extract aktor keterlibatan
            aktor_text = self.extract_text_from_table(soup, 'Aktor')
            if aktor_text:
                aktor_lower = aktor_text.lower()
                result['aktor_pemerintah'] = 'pemerintah' in aktor_lower
                result['aktor_perusahaan'] = 'perusahaan' in aktor_lower
                result['aktor_masyarakat'] = 'masyarakat' in aktor_lower
            
            # 3. Extract narasi lengkap
            narasi = self.extract_narasi(soup)
            result['narasi_lengkap'] = narasi
            
            # 4. Detect kriminalisasi dari narasi
            found_krim, bukti, jumlah, aktor = self.detect_kriminalisasi(narasi)
            result['indikasi_kriminalisasi'] = found_krim
            result['bukti_teks_kriminalisasi'] = ' | '.join(bukti)
            result['jumlah_ditangkap'] = jumlah['ditangkap']
            result['jumlah_luka'] = jumlah['luka']
            result['jumlah_tewas'] = jumlah['tewas']
            result['aktor_kriminalisasi'] = ', '.join(aktor)
            
            result['scraping_success'] = True
            
            self.logger.info(
                f"  ✅ Luas: {result['luas_ha']} Ha | "
                f"Dampak: {result['dampak_jiwa']} jiwa | "
                f"Kriminalisasi: {result['indikasi_kriminalisasi']}"
            )
            
        except Exception as e:
            result['error_message'] = str(e)
            self.logger.error(f"  ❌ Error: {e}")
        
        return result
    
    def scrape_all(self, test_mode: bool = False, test_limit: int = 2):
        """
        Scrape semua kasus atau test mode
        """
        # Load data konflik
        konflik_file = Path("data/raw/kpa_ylbhi_tanahkita/tanahkita_konflik.csv")
        
        if not konflik_file.exists():
            self.logger.error(f"❌ File not found: {konflik_file}")
            return
        
        df = pd.read_csv(konflik_file)
        
        if test_mode:
            df = df.head(test_limit)
            self.logger.info(f"🧪 TEST MODE: scraping {test_limit} kasus pertama")
        
        total_cases = len(df)
        
        self.logger.info(f"\n{'='*60}")
        self.logger.info(f"TanahKita Detail Scraper")
        self.logger.info(f"{'='*60}")
        self.logger.info(f"Total cases: {total_cases}")
        self.logger.info(f"Delay: {self.delay}s per request")
        self.logger.info(f"Estimated time: ~{(total_cases * self.delay / 60):.1f} minutes")
        self.logger.info(f"{'='*60}\n")
        
        # Progress tracking
        from tqdm import tqdm
        
        for idx, row in tqdm(df.iterrows(), total=total_cases, desc="Scraping details"):
            try:
                result = self.scrape_detail_page(row)
                self.details.append(result)
                self.cases_processed += 1
                
                # Checkpoint save
                if self.cases_processed % self.checkpoint_interval == 0:
                    if self.checkpoint_path:
                        self.save_checkpoint()
                
            except KeyboardInterrupt:
                self.logger.warning("\n⚠️  Interrupted by user!")
                if self.checkpoint_path:
                    self.save_checkpoint()
                raise
            
            except Exception as e:
                self.logger.error(f"❌ Error processing case {row['nomor']}: {e}")
                continue
        
        self.logger.info(f"\n{'='*60}")
        self.logger.info("✅ SCRAPING COMPLETE!")
        self.logger.info(f"{'='*60}")
        self.logger.info(f"Cases processed: {self.cases_processed}")
        self.logger.info(f"Success: {sum(1 for d in self.details if d['scraping_success'])}")
        self.logger.info(f"Failed: {sum(1 for d in self.details if not d['scraping_success'])}")
        self.logger.info(f"Kriminalisasi detected: {sum(1 for d in self.details if d['indikasi_kriminalisasi'])}")
    
    def save_checkpoint(self):
        """Save checkpoint"""
        if not self.checkpoint_path:
            return
        
        checkpoint_data = {
            'timestamp': datetime.now().isoformat(),
            'cases_processed': self.cases_processed,
            'details': self.details
        }
        
        self.checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.checkpoint_path, 'w', encoding='utf-8') as f:
            json.dump(checkpoint_data, f, ensure_ascii=False, indent=2)
        
        self.logger.debug(f"Checkpoint saved: {self.checkpoint_path}")
    
    def merge_with_original(self, output_path: str):
        """
        Merge scraped detail dengan original CSV
        """
        # Load original
        konflik_file = Path("data/raw/kpa_ylbhi_tanahkita/tanahkita_konflik.csv")
        df_original = pd.read_csv(konflik_file)
        
        # Convert details to dataframe
        df_details = pd.DataFrame(self.details)
        
        # Merge on 'nomor'
        df_merged = df_original.merge(df_details, on='nomor', how='left')
        
        # Save
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        df_merged.to_csv(output_file, index=False, encoding='utf-8-sig')
        
        self.logger.info(f"📄 Merged data saved: {output_file}")
        self.logger.info(f"   Total rows: {len(df_merged)}")
        self.logger.info(f"   Columns: {len(df_merged.columns)}")
        
        return df_merged


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description="TanahKita Detail Scraper - Extract detail pages + kriminalisasi detection"
    )
    parser.add_argument(
        "--test",
        type=int,
        metavar="N",
        help="Test mode: scrape N kasus pertama (e.g., --test 2)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Scrape semua 178 kasus"
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=1.5,
        help="Delay between requests in seconds (default: 1.5)"
    )
    parser.add_argument(
        "--output",
        default="data/processed/tanahkita_konflik_detail.csv",
        help="Output file path (default: data/processed/tanahkita_konflik_detail.csv)"
    )
    parser.add_argument(
        "--checkpoint",
        default="output/checkpoint_tanahkita.json",
        help="Checkpoint file path"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    # Validate args
    if not args.test and not args.all:
        parser.error("Please specify --test N or --all")
    
    # Scraper setup
    scraper = TanahKitaDetailScraper(
        delay=args.delay,
        verbose=args.verbose,
        checkpoint_path=args.checkpoint if args.all else None
    )
    
    try:
        # Scrape
        if args.test:
            scraper.scrape_all(test_mode=True, test_limit=args.test)
        else:
            scraper.scrape_all(test_mode=False)
        
        # Merge and export
        df_final = scraper.merge_with_original(args.output)
        
        print("\n" + "="*60)
        print("✅ SCRAPING & MERGE COMPLETE!")
        print("="*60)
        print(f"Output file: {args.output}")
        print(f"Total rows: {len(df_final)}")
        print(f"Kriminalisasi cases: {sum(df_final['indikasi_kriminalisasi'] == True)}")
        print("="*60)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Scraping interrupted by user")
        if scraper.checkpoint_path:
            scraper.save_checkpoint()
            print(f"💾 Checkpoint saved: {scraper.checkpoint_path}")
        
        # Still try to export partial data
        if scraper.details:
            scraper.merge_with_original(args.output)
            print(f"📊 Partial data exported")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
