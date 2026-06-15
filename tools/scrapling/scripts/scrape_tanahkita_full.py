#!/usr/bin/env python3
"""
TanahKita Full Scraper - List + Detail
Scrape konflik list AND detail pages dalam 1 run

Usage:
    python scrape_tanahkita_full.py --test 2      # Test 2 kasus
    python scrape_tanahkita_full.py --all         # Semua kasus
    python scrape_tanahkita_full.py --max 50      # Limit 50 kasus
"""

import argparse
import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from tqdm import tqdm
import sys

sys.path.insert(0, str(Path(__file__).parent))
from scraper_base import BaseScraper


class TanahKitaFullScraper(BaseScraper):
    """Scraper untuk list + detail TanahKita.id"""
    
    def __init__(self, delay: float = 1.5, max_cases: Optional[int] = None, verbose: bool = False):
        super().__init__(name="tanahkita_full", delay=delay, verbose=verbose)
        
        self.base_url = "https://tanahkita.id/data/konflik"
        self.max_cases = max_cases
        
        # Kriminalisasi patterns
        self.kriminalisasi_patterns = {
            'kriminalisasi': r'kriminalisas[i]',
            'ditangkap': r'ditangkap|penangkapan|penahanan|ditahan|tangkap',
            'aparat': r'polisi|polda|polres|polsek|polhut|TNI|tentara|satpol\s*pp|aparat',
            'kekerasan': r'kekerasan|intimidasi|ancaman|teror|diusir|dipukul|penganiayaan',
            'korban_fisik': r'luka|terluka|tewas|meninggal|cedera|dipukul|disiksa'
        }
        
        self.number_patterns = {
            'ditangkap': r'(\d+)\s*(?:orang)?\s*(?:warga|petani|masyarakat|aktivis)?\s*(?:di)?(?:tangkap|ditahan|ditangkap)',
            'luka': r'(\d+)\s*(?:orang)?\s*(?:luka|terluka|cedera)',
            'tewas': r'(\d+)\s*(?:orang)?\s*(?:tewas|meninggal|terbunuh)'
        }
    
    def fix_detail_url(self, url: str) -> str:
        """Fix bug URL: /data/data/konflik/ → /data/konflik/"""
        if '/data/data/konflik/' in url:
            return url.replace('/data/data/konflik/', '/data/konflik/')
        return url
    
    def scrape_list_page(self, page_num: int) -> List[Dict]:
        """Scrape list page untuk dapatkan basic info + detail URLs"""
        if page_num == 1:
            url = self.base_url
        else:
            offset = (page_num - 1) * 10
            url = f"{self.base_url}/index/{offset}"
        
        try:
            response = self.fetch_page(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            table = soup.find('table')
            if not table:
                return []
            
            rows = table.find('tbody').find_all('tr') if table.find('tbody') else []
            cases = []
            
            for row in rows:
                cols = row.find_all('td', recursive=False)
                if len(cols) not in [7, 8]:
                    continue
                
                nomor_text = cols[0].get_text(strip=True)
                if not nomor_text.isdigit():
                    continue
                
                tahun_text = cols[1].get_text(strip=True)
                if not tahun_text.isdigit():
                    continue
                
                # Determine column indices
                if len(cols) == 8:
                    lokasi_idx, status_idx, detail_idx = 5, 6, 7
                else:
                    lokasi_idx, status_idx, detail_idx = 4, 5, 6
                
                # Extract detail URL
                detail_url = None
                link = cols[detail_idx].find('a', href=True)
                if link:
                    detail_url = urljoin(self.base_url, link['href'])
                    detail_url = self.fix_detail_url(detail_url)
                
                if not detail_url:
                    continue
                
                case = {
                    "nomor": int(nomor_text),
                    "tahun": int(tahun_text),
                    "judul": cols[2].get_text(strip=True),
                    "deskripsi": cols[3].get_text(strip=True),
                    "lokasi": cols[lokasi_idx].get_text(strip=True),
                    "status": cols[status_idx].get_text(strip=True),
                    "detail_url": detail_url,
                    "list_scraped_at": datetime.now().isoformat()
                }
                cases.append(case)
            
            return cases
            
        except Exception as e:
            self.logger.error(f"Error scraping list page {page_num}: {e}")
            return []
    
    def get_all_cases(self) -> List[Dict]:
        """Scrape semua list pages untuk dapatkan semua kasus"""
        self.logger.info("Fetching case list...")
        
        # Get first page to determine total
        response = self.fetch_page(self.base_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Count total entries
        pagination_text = soup.find(string=re.compile(r'of \d+ entries'))
        total_entries = 178  # default
        
        if pagination_text:
            match = re.search(r'of (\d+) entries', pagination_text)
            if match:
                total_entries = int(match.group(1))
        
        total_pages = (total_entries + 9) // 10  # 10 per page
        
        self.logger.info(f"Found {total_entries} total cases, {total_pages} pages")
        
        # Scrape all list pages
        all_cases = self.scrape_list_page(1)  # First page
        
        for page_num in tqdm(range(2, total_pages + 1), desc="Fetching list"):
            cases = self.scrape_list_page(page_num)
            all_cases.extend(cases)
        
        self.logger.info(f"Collected {len(all_cases)} cases from list")
        
        # Apply limit if set
        if self.max_cases and len(all_cases) > self.max_cases:
            all_cases = all_cases[:self.max_cases]
            self.logger.info(f"Limited to {self.max_cases} cases")
        
        return all_cases
    
    def extract_from_table(self, soup: BeautifulSoup, label: str) -> Optional[str]:
        """Extract value from table row with format: <td>Label</td><td>:</td><td>Value</td>"""
        try:
            rows = soup.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 3:
                    cell_text = cells[0].get_text(strip=True)
                    if label.lower() in cell_text.lower():
                        value = cells[2].get_text(strip=True)
                        return value if value else None
            return None
        except Exception as e:
            return None
    
    def extract_keterlibatan(self, soup: BeautifulSoup) -> Dict[str, List[str]]:
        """Extract actors from KETERLIBATAN section"""
        keterlibatan = {
            'pemerintah': [],
            'perusahaan': [],
            'masyarakat': []
        }
        
        try:
            # Find KETERLIBATAN heading
            h4 = soup.find('h4', string=lambda s: s and 'KETERLIBATAN' in s.upper())
            if not h4:
                return keterlibatan
            
            # Get next sibling div with class="row keterlibatan"
            next_div = h4.find_next_sibling('div', class_='row')
            if not next_div:
                next_div = h4.find_next_sibling('div')
            
            if not next_div:
                return keterlibatan
            
            # Find 3 columns (col-md-4)
            columns = next_div.find_all('div', class_=lambda x: x and 'col-md-4' in str(x))
            
            for col in columns:
                # Get label to determine which category
                label = col.find('label')
                if not label:
                    continue
                
                label_text = label.get_text(strip=True).lower()
                
                # Extract list items
                items = []
                for li in col.find_all('li'):
                    text = li.get_text(strip=True)
                    if text:  # Not empty
                        items.append(text)
                
                # Map to correct category
                if 'pemerintah' in label_text:
                    keterlibatan['pemerintah'] = items
                elif 'perusahaan' in label_text:
                    keterlibatan['perusahaan'] = items
                elif 'masyarakat' in label_text:
                    keterlibatan['masyarakat'] = items
        
        except Exception as e:
            self.logger.error(f"Error extracting keterlibatan: {e}")
        
        return keterlibatan
    
    def extract_sumber(self, soup: BeautifulSoup) -> str:
        """Extract source/sumber"""
        try:
            # Find label with text "Sumber"
            for label in soup.find_all('label'):
                if 'sumber' in label.get_text(strip=True).lower():
                    # Get next sibling (should be <p>)
                    next_elem = label.find_next_sibling()
                    if next_elem:
                        return next_elem.get_text(strip=True)
            
            # Fallback: find heading "Sumber"
            for heading in soup.find_all(['h4', 'h5', 'strong', 'b']):
                if 'sumber' in heading.get_text(strip=True).lower():
                    next_elem = heading.find_next_sibling()
                    if next_elem:
                        return next_elem.get_text(strip=True)
            return ""
        except:
            return ""
    
    def extract_lampiran(self, soup: BeautifulSoup) -> str:
        """Extract lampiran/attachments"""
        try:
            lampiran_list = []
            for heading in soup.find_all(['h4', 'h5', 'strong', 'b']):
                if 'lampiran' in heading.get_text(strip=True).lower():
                    # Find all links or file references after this heading
                    for sibling in heading.find_next_siblings():
                        if sibling.name in ['h1', 'h2', 'h3', 'h4', 'h5']:
                            break
                        # Look for links
                        links = sibling.find_all('a', href=True)
                        for link in links:
                            link_text = link.get_text(strip=True)
                            link_url = link.get('href')
                            if link_text and link_url:
                                lampiran_list.append(f"{link_text} ({link_url})")
                        
                        # If no links, get text (might say "Tidak Ada Lampiran")
                        if not links:
                            text = sibling.get_text(strip=True)
                            if text and len(text) < 100:
                                lampiran_list.append(text)
                    break
            
            return ' | '.join(lampiran_list) if lampiran_list else "Tidak Ada Lampiran"
        except:
            return ""
        """Extract value from table row with format: <td>Label</td><td>:</td><td>Value</td>"""
        try:
            rows = soup.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 3:
                    cell_text = cells[0].get_text(strip=True)
                    if label.lower() in cell_text.lower():
                        value = cells[2].get_text(strip=True)
                        return value if value else None
            return None
        except Exception as e:
            return None
    
    def parse_luas_ha(self, text: str) -> Optional[float]:
        """Parse luas dari text seperti '1250 Ha' atau '0,00 Ha'"""
        if not text:
            return None
        try:
            clean_text = text.replace('Ha', '').replace('ha', '').strip()
            clean_text = clean_text.replace('.', '').replace(',', '.')
            match = re.search(r'[\d.]+', clean_text)
            if match:
                return float(match.group())
        except:
            pass
        return None
    
    def parse_dampak_jiwa(self, text: str) -> Optional[int]:
        """Parse dampak dari text seperti '1.330 Jiwa' atau '150 Jiwa'"""
        if not text:
            return None
        try:
            # Remove 'Jiwa', 'jiwa', 'Ha', 'ha', whitespace
            clean_text = re.sub(r'\s*(jiwa|ha)\s*', '', text, flags=re.I).strip()
            # Remove thousand separators (titik) but keep comma as decimal
            clean_text = clean_text.replace('.', '')
            # Find all digits (now contiguous)
            match = re.search(r'(\d+)', clean_text)
            if match:
                return int(match.group(1))
        except:
            pass
        return None
    
    def extract_narasi(self, soup: BeautifulSoup) -> str:
        """Extract narrative text from KONTEN section"""
        try:
            # Strategy 1: Find heading with "Narasi"
            for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'strong', 'b']):
                heading_text = heading.get_text(strip=True).lower()
                if heading_text == 'narasi' or heading_text == 'konten':
                    # Get all following paragraphs until next major section
                    narasi_parts = []
                    for sibling in heading.find_next_siblings():
                        sibling_text = sibling.get_text(strip=True)
                        # Stop at next major heading (Sumber, Lampiran, etc)
                        if sibling.name in ['h1', 'h2', 'h3', 'h4', 'h5']:
                            if any(keyword in sibling_text.lower() for keyword in ['sumber', 'lampiran', 'dokumen']):
                                break
                        
                        # Only include paragraphs with substantial text
                        if sibling.name in ['p', 'div']:
                            text = sibling.get_text(separator=' ', strip=True)
                            # Filter out section labels and short texts
                            if len(text) > 100 and not any(label in text.lower() for label in ['keterlibatan', 'pemerintah', 'perusahaan', 'masyarakat', 'narasi', 'konten', 'sumber', 'lampiran']):
                                narasi_parts.append(text)
                    
                    if narasi_parts:
                        return '\n\n'.join(narasi_parts)
            
            # Strategy 2: Find all long paragraphs (likely narrative content)
            all_paragraphs = []
            for p in soup.find_all('p'):
                text = p.get_text(separator=' ', strip=True)
                # Only paragraphs longer than 200 chars, not section labels
                if len(text) > 200 and not any(label in text[:50].lower() for label in ['keterlibatan', 'data detil', 'konten', 'lampiran']):
                    all_paragraphs.append(text)
            
            if all_paragraphs:
                return '\n\n'.join(all_paragraphs)
            
            return ""
        except Exception as e:
            self.logger.error(f"Error extracting narasi: {e}")
            return ""
    
    def detect_kriminalisasi(self, narasi: str) -> Tuple[bool, List[str], Dict[str, int]]:
        """Detect kriminalisasi from narrative - NO aktor (already in keterlibatan columns)"""
        if not narasi:
            return False, [], {'ditangkap': 0, 'luka': 0, 'tewas': 0}
        
        narasi_lower = narasi.lower()
        bukti_sentences = []
        jumlah = {'ditangkap': 0, 'luka': 0, 'tewas': 0}
        
        sentences = re.split(r'[.!?\n]+', narasi)
        
        # Check patterns for kriminalisasi evidence
        found_kriminalisasi = False
        for pattern_name, pattern in self.kriminalisasi_patterns.items():
            if re.search(pattern, narasi_lower):
                found_kriminalisasi = True
                for sentence in sentences:
                    if re.search(pattern, sentence.lower()):
                        bukti_sentences.append(sentence.strip())
        
        # Extract numbers from narasi (ditangkap, luka, tewas)
        for key, pattern in self.number_patterns.items():
            matches = re.findall(pattern, narasi_lower)
            if matches:
                numbers = [int(m) for m in matches if m.isdigit()]
                if numbers:
                    jumlah[key] = max(numbers)
        
        bukti_sentences = list(set(bukti_sentences))[:5]
        
        return found_kriminalisasi, bukti_sentences, jumlah
    
    def scrape_detail(self, case: Dict) -> Dict:
        """Scrape detail page - follow exact structure from TanahKita website"""
        detail_url = case['detail_url']
        
        try:
            response = self.fetch_page(detail_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # === DATA DETAIL (from table) ===
            case['nomor_kejadian'] = self.extract_from_table(soup, 'Nomor Kejadian')
            case['waktu_kejadian'] = self.extract_from_table(soup, 'Waktu Kejadian')
            case['konflik'] = self.extract_from_table(soup, 'Konflik')
            case['status_konflik'] = self.extract_from_table(soup, 'Status Konflik')
            case['sektor'] = self.extract_from_table(soup, 'Sektor')
            case['sektor_lain'] = self.extract_from_table(soup, 'Sektor Lain')
            
            luas_text = self.extract_from_table(soup, 'Luas')
            dampak_text = self.extract_from_table(soup, 'Dampak Masyarakat')
            
            case['luas_ha'] = self.parse_luas_ha(luas_text)
            case['dampak_masyarakat_jiwa'] = self.parse_dampak_jiwa(dampak_text)
            case['confidentiality'] = self.extract_from_table(soup, 'Confidentiality')
            
            # === KETERLIBATAN (3 columns) ===
            keterlibatan = self.extract_keterlibatan(soup)
            case['keterlibatan_pemerintah'] = ' | '.join(keterlibatan['pemerintah']) if keterlibatan['pemerintah'] else None
            case['keterlibatan_perusahaan'] = ' | '.join(keterlibatan['perusahaan']) if keterlibatan['perusahaan'] else None
            case['keterlibatan_masyarakat'] = ' | '.join(keterlibatan['masyarakat']) if keterlibatan['masyarakat'] else None
            
            # === KONTEN ===
            case['narasi'] = self.extract_narasi(soup)
            case['sumber'] = self.extract_sumber(soup)
            
            # === LAMPIRAN ===
            case['lampiran'] = self.extract_lampiran(soup)
            
            # === ANALYSIS (computed from narasi only) ===
            # Aktor already captured in keterlibatan_pemerintah column
            found, bukti, jumlah = self.detect_kriminalisasi(case['narasi'])
            case['indikasi_kriminalisasi'] = found
            case['bukti_kriminalisasi'] = ' | '.join(bukti) if bukti else None
            case['jumlah_ditangkap'] = jumlah['ditangkap']
            case['jumlah_luka'] = jumlah['luka']
            case['jumlah_tewas'] = jumlah['tewas']
            
            # === METADATA ===
            case['scraped_at'] = datetime.now().isoformat()
            case['scraping_success'] = True
            
        except Exception as e:
            self.logger.error(f"Error scraping detail {case.get('nomor', '?')}: {e}")
            case['scraping_success'] = False
            case['error_message'] = str(e)
        
        return case
    
    def scrape_all(self):
        """Main scraping workflow"""
        # Step 1: Get all case list
        cases = self.get_all_cases()
        
        if not cases:
            self.logger.error("No cases found!")
            return
        
        # Step 2: Scrape details
        self.logger.info(f"\nScraping details for {len(cases)} cases...")
        
        for i, case in enumerate(tqdm(cases, desc="Scraping details")):
            try:
                case_with_detail = self.scrape_detail(case)
                self.data.append(case_with_detail)
                
            except KeyboardInterrupt:
                self.logger.warning("\n⚠️  Interrupted by user!")
                raise
            except Exception as e:
                self.logger.error(f"Error processing case {case.get('nomor')}: {e}")
                continue
        
        success_count = sum(1 for d in self.data if d.get('scraping_success'))
        krim_count = sum(1 for d in self.data if d.get('indikasi_kriminalisasi'))
        
        self.logger.info(f"\n✅ COMPLETE!")
        self.logger.info(f"Total: {len(self.data)} | Success: {success_count} | Kriminalisasi: {krim_count}")


def main():
    parser = argparse.ArgumentParser(description="TanahKita Full Scraper - List + Detail")
    parser.add_argument("--test", type=int, metavar="N", help="Test mode: scrape N kasus")
    parser.add_argument("--all", action="store_true", help="Scrape semua kasus")
    parser.add_argument("--max", type=int, metavar="N", help="Limit maksimal N kasus")
    parser.add_argument("--delay", type=float, default=1.5, help="Delay between requests (default: 1.5s)")
    parser.add_argument("--output", default="data/processed/tanahkita_konflik_full.csv", help="Output CSV file")
    parser.add_argument("--verbose", action="store_true", help="Verbose logging")
    
    args = parser.parse_args()
    
    if not args.test and not args.all and not args.max:
        parser.error("Specify --test N, --max N, or --all")
    
    max_cases = args.test or args.max
    
    scraper = TanahKitaFullScraper(delay=args.delay, max_cases=max_cases, verbose=args.verbose)
    
    try:
        scraper.scrape_all()
        scraper.export_csv(args.output)
        
        print(f"\n{'='*60}")
        print(f"✅ DONE! Saved to: {args.output}")
        print(f"{'='*60}")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted")
        if scraper.data:
            scraper.export_csv(args.output)
            print(f"💾 Partial data saved: {len(scraper.data)} cases")


if __name__ == "__main__":
    main()
