"""
HTML Parsing Utilities
CELIOS ECC Intelligence System

Helper functions untuk parsing HTML tables dan elements
"""

import re
from typing import List, Dict, Optional
from bs4 import BeautifulSoup, Tag


class HTMLTableParser:
    """Helper class untuk parse HTML tables"""
    
    @staticmethod
    def extract_table_headers(table: Tag) -> List[str]:
        """
        Ekstrak header dari table
        
        Args:
            table: BeautifulSoup table element
            
        Returns:
            List of header names
        """
        headers = []
        thead = table.find('thead')
        
        if thead:
            header_row = thead.find('tr')
            if header_row:
                headers = [th.get_text(strip=True) for th in header_row.find_all(['th', 'td'])]
        
        return headers
    
    @staticmethod
    def table_to_dicts(table: Tag, headers: Optional[List[str]] = None) -> List[Dict]:
        """
        Convert HTML table ke list of dicts
        
        Args:
            table: BeautifulSoup table element
            headers: Optional custom headers. If None, akan extract dari table.
            
        Returns:
            List of dicts, satu dict per row
        """
        if headers is None:
            headers = HTMLTableParser.extract_table_headers(table)
        
        data = []
        tbody = table.find('tbody')
        rows = tbody.find_all('tr') if tbody else table.find_all('tr')[1:]  # Skip header row
        
        for row in rows:
            cols = row.find_all('td')
            if len(cols) == 0:
                continue
            
            row_data = {}
            for i, col in enumerate(cols):
                header = headers[i] if i < len(headers) else f"col_{i}"
                row_data[header] = col.get_text(strip=True)
            
            data.append(row_data)
        
        return data
    
    @staticmethod
    def extract_pagination_info(soup: BeautifulSoup) -> Dict[str, int]:
        """
        Ekstrak informasi pagination dari halaman
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            Dict dengan keys: current_page, total_pages, total_entries, per_page
        """
        info = {
            "current_page": 1,
            "total_pages": 1,
            "total_entries": 0,
            "per_page": 10
        }
        
        # Cari text seperti "Displaying: 1 - 10 of 580 entries"
        pagination_text = soup.find(string=re.compile(r'of \d+ entries'))
        
        if pagination_text:
            # Parse "1 - 10 of 580 entries"
            match = re.search(r'(\d+)\s*-\s*(\d+)\s+of\s+(\d+)\s+entries', pagination_text)
            if match:
                start = int(match.group(1))
                end = int(match.group(2))
                total = int(match.group(3))
                
                info["total_entries"] = total
                info["per_page"] = end - start + 1
                info["current_page"] = (start - 1) // info["per_page"] + 1
                info["total_pages"] = (total + info["per_page"] - 1) // info["per_page"]
        
        return info
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean text dari whitespace berlebih dan karakter special
        
        Args:
            text: Raw text
            
        Returns:
            Cleaned text
        """
        # Remove multiple whitespaces
        text = re.sub(r'\s+', ' ', text)
        
        # Remove leading/trailing whitespace
        text = text.strip()
        
        # Remove zero-width spaces and other invisible chars
        text = re.sub(r'[\u200b-\u200f\u202a-\u202e]', '', text)
        
        return text
    
    @staticmethod
    def extract_all_links(element: Tag, base_url: str = "") -> List[str]:
        """
        Ekstrak semua links dari element
        
        Args:
            element: BeautifulSoup element
            base_url: Base URL untuk relative links
            
        Returns:
            List of absolute URLs
        """
        from urllib.parse import urljoin
        
        links = []
        for a in element.find_all('a', href=True):
            url = urljoin(base_url, a['href'])
            links.append(url)
        
        return links
