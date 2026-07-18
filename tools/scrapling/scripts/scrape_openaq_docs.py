#!/usr/bin/env python3
"""
OpenAQ API Documentation Scraper
Scrapes https://docs.openaq.org and converts to markdown like BPS API docs
"""

import requests
from bs4 import BeautifulSoup
from pathlib import Path
import time
from urllib.parse import urljoin
import re

class OpenAQDocsScraper:
    """Scraper untuk dokumentasi OpenAQ API"""
    
    def __init__(self):
        self.base_url = "https://docs.openaq.org"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.content = []
        
        # Complete list of documentation URLs from sidebar
        self.doc_pages = [
            # About
            ('/about/about', 'About OpenAQ API'),
            ('/about/terms', 'Terms of Use'),
            
            # Using the API
            ('/using-the-api/quick-start', 'Quick Start'),
            ('/using-the-api/api-key', 'API Key'),
            ('/using-the-api/rate-limits', 'Rate Limits'),
            ('/using-the-api/pagination', 'Pagination'),
            ('/using-the-api/dates-datetimes-timezones', 'Dates, Datetimes and Timezones'),
            ('/using-the-api/geospatial-queries', 'Geospatial Queries'),
            ('/using-the-api/client-libraries', 'Client Libraries'),
            
            # Examples
            ('/examples', 'Examples Overview'),
            ('/examples/python', 'Python Examples'),
            ('/examples/r', 'R Examples'),
            ('/examples/javascript', 'JavaScript Examples'),
            
            # Resources
            ('/resources/countries', 'Countries Resource'),
            ('/resources/instruments', 'Instruments Resource'),
            ('/resources/latest', 'Latest Resource'),
            ('/resources/licenses', 'Licenses Resource'),
            ('/resources/locations', 'Locations Resource'),
            ('/resources/manufacturers', 'Manufacturers Resource'),
            ('/resources/measurements', 'Measurements Resource'),
            ('/resources/owners', 'Owners Resource'),
            ('/resources/parameters', 'Parameters Resource'),
            ('/resources/providers', 'Providers Resource'),
            ('/resources/sensors', 'Sensors Resource'),
            
            # Errors
            ('/errors/about', 'About Errors'),
            ('/errors/401', '401 - Unauthorized'),
            ('/errors/403', '403 - Forbidden'),
            ('/errors/404', '404 - Not Found'),
            ('/errors/405', '405 - Method Not Allowed'),
            ('/errors/408', '408 - Request Timeout'),
            ('/errors/410', '410 - Gone'),
            ('/errors/422', '422 - Unprocessable Content'),
            ('/errors/429', '429 - Too Many Requests'),
            
            # API Reference
            ('/reference/overview', 'API Reference Overview'),
            ('/reference/v3', 'API v3 Reference'),
            ('/reference/v3/locations', 'v3 Locations Endpoint'),
            ('/reference/v3/measurements', 'v3 Measurements Endpoint'),
            ('/reference/v3/parameters', 'v3 Parameters Endpoint'),
            ('/reference/v3/countries', 'v3 Countries Endpoint'),
            ('/reference/v3/providers', 'v3 Providers Endpoint'),
            ('/reference/v3/instruments', 'v3 Instruments Endpoint'),
            ('/reference/v3/manufacturers', 'v3 Manufacturers Endpoint'),
            ('/reference/v3/owners', 'v3 Owners Endpoint'),
            ('/reference/v3/licenses', 'v3 Licenses Endpoint'),
            ('/reference/v3/sensors', 'v3 Sensors Endpoint'),
            ('/reference/v3/latest', 'v3 Latest Endpoint'),
            
            # Open Data on AWS
            ('/open-data-on-aws/quick-start', 'AWS Quick Start'),
            ('/open-data-on-aws/about', 'About Open Data on AWS'),
            ('/open-data-on-aws/guide-downloading-year', 'Guide - Downloading a Year of Data'),
            ('/open-data-on-aws/guide-querying-athena', 'Guide - Querying with Athena'),
        ]
        
    def fetch_page(self, url: str):
        """Fetch page dengan retry"""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response
        except Exception as e:
            print(f"❌ Error fetching {url}: {e}")
            return None
    
    def extract_main_sections(self, soup: BeautifulSoup):
        """Extract main navigation sections"""
        sections = []
        
        # Try to find navigation menu
        nav = soup.find('nav') or soup.find('aside') or soup.find(class_=re.compile('sidebar|navigation|menu', re.I))
        
        if nav:
            links = nav.find_all('a', href=True)
            for link in links:
                href = link.get('href')
                text = link.get_text(strip=True)
                if href and text and not href.startswith('#'):
                    full_url = urljoin(self.base_url, href)
                    sections.append({
                        'title': text,
                        'url': full_url
                    })
        
        return sections
    
    def scrape_page_content(self, url: str, title: str):
        """Scrape content from a single documentation page"""
        print(f"📄 Scraping: {title}")
        
        response = self.fetch_page(url)
        if not response:
            return None
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find main content area
        main_content = (
            soup.find('main') or 
            soup.find('article') or 
            soup.find(class_=re.compile('content|documentation|main', re.I)) or
            soup.find('div', {'role': 'main'})
        )
        
        if not main_content:
            main_content = soup
        
        # Extract content
        content_md = f"\n\n## {title}\n\n---\n\n"
        
        # Process all elements
        for elem in main_content.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'ul', 'ol', 'pre', 'code', 'table']):
            if elem.name.startswith('h'):
                level = int(elem.name[1])
                heading = elem.get_text(strip=True)
                content_md += f"\n{'#' * (level + 1)} {heading}\n\n"
            
            elif elem.name == 'p':
                text = elem.get_text(strip=True)
                if text:
                    content_md += f"{text}\n\n"
            
            elif elem.name in ['ul', 'ol']:
                for li in elem.find_all('li', recursive=False):
                    text = li.get_text(strip=True)
                    content_md += f"- {text}\n"
                content_md += "\n"
            
            elif elem.name == 'pre':
                code = elem.get_text()
                content_md += f"```\n{code}\n```\n\n"
            
            elif elem.name == 'code' and elem.parent.name != 'pre':
                code = elem.get_text()
                content_md += f"`{code}` "
            
            elif elem.name == 'table':
                content_md += self.table_to_markdown(elem)
        
        return content_md
    
    def table_to_markdown(self, table):
        """Convert HTML table to markdown"""
        md = "\n"
        
        # Extract headers
        headers = []
        thead = table.find('thead')
        if thead:
            for th in thead.find_all(['th', 'td']):
                headers.append(th.get_text(strip=True))
        
        if not headers:
            # Try first row
            first_row = table.find('tr')
            if first_row:
                for th in first_row.find_all(['th', 'td']):
                    headers.append(th.get_text(strip=True))
        
        if headers:
            md += "| " + " | ".join(headers) + " |\n"
            md += "| " + " | ".join(['---' for _ in headers]) + " |\n"
        
        # Extract rows
        tbody = table.find('tbody') or table
        for tr in tbody.find_all('tr')[1 if not thead else 0:]:
            cells = []
            for td in tr.find_all(['td', 'th']):
                cells.append(td.get_text(strip=True))
            if cells:
                md += "| " + " | ".join(cells) + " |\n"
        
        md += "\n"
        return md
    
    def scrape_all(self):
        """Main scraping workflow"""
        print("🌐 Scraping OpenAQ Documentation...")
        
        # Header
        self.content.append("# OpenAQ API Documentation\n\n")
        self.content.append("Complete API documentation scraped from https://docs.openaq.org\n\n")
        self.content.append("---\n\n")
        
        # Scrape each page
        for path, title in self.doc_pages:
            url = self.base_url + path
            content = self.scrape_page_content(url, title)
            if content:
                self.content.append(content)
            time.sleep(2)  # Be nice to the server
        
        print("\n✅ Scraping complete!")
    
    def save_markdown(self, output_path: str):
        """Save to markdown file"""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(''.join(self.content))
        
        print(f"\n📝 Saved to: {output_file}")
        print(f"📊 Size: {output_file.stat().st_size / 1024:.1f} KB")


def main():
    scraper = OpenAQDocsScraper()
    scraper.scrape_all()
    
    output_path = "docs/openaq-api-documentation.md"
    scraper.save_markdown(output_path)
    
    print("\n" + "="*70)
    print("✅ DONE! OpenAQ API documentation saved")
    print("="*70)


if __name__ == "__main__":
    main()
