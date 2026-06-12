#!/usr/bin/env python3
"""
BPS API Client
CELIOS ECC Intelligence System

Python client untuk BPS (Badan Pusat Statistik) Web API
"""

import time
import logging
import os
from typing import List, Dict, Optional, Any
from datetime import datetime
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import yaml
from dotenv import load_dotenv


class BPSClient:
    """Client untuk mengakses BPS Web API"""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        config_path: str = "config.yaml",
        verbose: bool = False
    ):
        """
        Initialize BPS API Client
        
        Args:
            api_key: BPS API key (jika tidak ada, akan load dari env/config)
            config_path: Path ke config file
            verbose: Enable verbose logging
        """
        # Load environment variables
        load_dotenv()
        
        # Setup logging
        self.logger = self._setup_logger(verbose)
        
        # Load config
        self.config = self._load_config(config_path)
        
        # Set API key
        self.api_key = api_key or os.getenv("BPS_API_KEY") or self.config.get("bps", {}).get("api_key")
        
        if not self.api_key or self.api_key.startswith("${"):
            raise ValueError(
                "BPS API key not found! "
                "Set BPS_API_KEY environment variable or provide via api_key parameter"
            )
        
        # API settings
        self.base_url = self.config.get("bps", {}).get(
            "base_url",
            "https://webapi.bps.go.id/v1/api"
        )
        self.timeout = self.config.get("bps", {}).get("timeout", 30)
        self.rate_limit = self.config.get("bps", {}).get("rate_limit", 1.0)
        
        # Create session
        self.session = self._create_session()
        
        self.logger.info("BPS API Client initialized")
    
    def _setup_logger(self, verbose: bool) -> logging.Logger:
        """Setup logging"""
        logger = logging.getLogger("BPSClient")
        level = logging.DEBUG if verbose else logging.INFO
        logger.setLevel(level)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _load_config(self, config_path: str) -> Dict:
        """Load YAML configuration"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            self.logger.warning(f"Config {config_path} not found, using defaults")
            return {}
    
    def _create_session(self) -> requests.Session:
        """Create requests session with retry logic"""
        session = requests.Session()
        
        # Retry strategy
        max_retries = self.config.get("bps", {}).get("max_retries", 3)
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "POST"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    def _rate_limit(self):
        """Apply rate limiting"""
        time.sleep(self.rate_limit)
    
    def _make_request(
        self,
        endpoint: str,
        params: Optional[Dict] = None,
        method: str = "GET"
    ) -> Dict:
        """
        Make API request
        
        Args:
            endpoint: API endpoint (e.g., "list", "data")
            params: Query parameters
            method: HTTP method
            
        Returns:
            Response JSON
        """
        url = f"{self.base_url}/{endpoint}"
        
        # Add API key to params
        if params is None:
            params = {}
        params["key"] = self.api_key
        
        try:
            self.logger.debug(f"Request: {method} {url} | params: {params}")
            
            if method == "GET":
                response = self.session.get(url, params=params, timeout=self.timeout)
            elif method == "POST":
                response = self.session.post(url, json=params, timeout=self.timeout)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            self._rate_limit()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API request failed: {e}")
            raise
    
    def test_connection(self) -> bool:
        """
        Test API connection and key validity
        
        Returns:
            True if connection successful
        """
        try:
            response = self._make_request("list", params={"page": 1})
            self.logger.info("✅ API connection successful")
            return True
        except Exception as e:
            self.logger.error(f"❌ API connection failed: {e}")
            return False
    
    def list_domains(self, type_filter: str = "all") -> List[Dict]:
        """
        List available domains (provinces/regions)
        
        Args:
            type_filter: Type of domains to list (default: "all")
        
        Returns:
            List of domains with id, name, etc.
        """
        try:
            response = self._make_request("domain", params={"type": type_filter})
            
            if response.get("status") == "OK" and response.get("data-availability") == "available":
                domains = response["data"][1]  # [0] is pagination info, [1] is data
                self.logger.info(f"Found {len(domains)} domains")
                return domains
            else:
                self.logger.warning("No domain data available")
                return []
        except Exception as e:
            self.logger.error(f"Failed to list domains: {e}")
            return []
    
    def list_dynamic_tables(
        self,
        domain: str = "0000",
        page: int = 1
    ) -> List[Dict]:
        """
        List available dynamic tables for a domain
        
        Args:
            domain: Domain code (default: "0000" for national)
            page: Page number (default: 1)
            
        Returns:
            List of dynamic tables with var_id, title, etc.
        """
        try:
            response = self._make_request("list", params={
                "model": "dynamictable",
                "domain": domain,
                "page": page
            })
            
            if response.get("status") == "OK":
                tables = response.get("datacontent", [])
                self.logger.info(f"Found {len(tables)} dynamic tables for domain {domain}")
                return tables
            else:
                self.logger.warning(f"No dynamic tables for domain {domain}")
                return []
        except Exception as e:
            self.logger.error(f"Failed to list dynamic tables: {e}")
            return []
    
    def get_dynamic_table(
        self,
        var: str,
        domain: str = "0000",
        year: Optional[str] = None
    ) -> List[Dict]:
        """
        Get data from a specific dynamic table variable
        
        Args:
            var: Variable ID (e.g., "123" for a specific indicator)
            domain: Domain code (province/regency)
            year: Year filter (optional)
            
        Returns:
            List of data entries from the dynamic table
        """
        params = {
            "model": "data",
            "domain": domain,
            "var": var,
            "lang": "ind"
        }
        
        if year:
            params["th"] = year
        
        try:
            response = self._make_request("list", params=params)
            
            if response.get("status") == "OK":
                data = response.get("datacontent", [])
                self.logger.info(f"Retrieved {len(data)} entries for var={var}, domain={domain}")
                return data
            else:
                self.logger.warning(f"No data for var={var}, domain={domain}")
                return []
        except Exception as e:
            self.logger.error(f"Failed to get dynamic table data: {e}")
            return []
    
    def get_data(
        self,
        model: str,
        domain: str = "0000",
        tahun: Optional[int] = None,
        **kwargs
    ) -> List[Dict]:
        """
        Get data from BPS API
        
        Args:
            model: Model/indicator code
            domain: Domain code (province/regency). "0000" = National
            tahun: Year filter
            **kwargs: Additional parameters
            
        Returns:
            List of data entries
        """
        params = {
            "model": model,
            "domain": domain,
            **kwargs
        }
        
        if tahun:
            params["tahun"] = tahun
        
        try:
            response = self._make_request("data", params=params)
            data = response.get("data", [])
            self.logger.info(f"Retrieved {len(data)} data entries")
            return data
        except Exception as e:
            self.logger.error(f"Failed to get data: {e}")
            return []
    
    def get_sulawesi_provinces(self) -> List[Dict]:
        """
        Get Sulawesi province codes from config
        
        Returns:
            List of {code, name} dicts
        """
        return self.config.get("bps", {}).get("sulawesi_provinces", [])
    
    def export_to_csv(self, data: List[Dict], output_path: str):
        """Export data to CSV"""
        import pandas as pd
        
        df = pd.DataFrame(data)
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        df.to_csv(output_path, index=False, encoding='utf-8-sig', quoting=1)
        self.logger.info(f"Exported {len(data)} entries to {output_path}")
    
    def export_to_json(self, data: List[Dict], output_path: str):
        """Export data to JSON"""
        import json
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"Exported {len(data)} entries to {output_path}")
    
    def export_to_excel(self, data: List[Dict], output_path: str):
        """Export data to Excel"""
        import pandas as pd
        
        df = pd.DataFrame(data)
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        df.to_excel(output_path, index=False, engine='openpyxl')
        self.logger.info(f"Exported {len(data)} entries to {output_path}")


if __name__ == "__main__":
    # Quick test
    import sys
    
    # Check for API key
    api_key = "06fd644648629502353deaed29fc6383"  # Your key
    
    print("="*80)
    print("BPS API Client - Connection Test")
    print("="*80)
    
    try:
        client = BPSClient(api_key=api_key, verbose=True)
        
        print("\n1. Testing connection...")
        if client.test_connection():
            print("   ✅ Connection successful!")
        else:
            print("   ❌ Connection failed!")
            sys.exit(1)
        
        print("\n2. Listing domains...")
        domains = client.list_domains(type_filter="all")
        if domains:
            print(f"   Found {len(domains)} domains")
            # Show Sulawesi provinces (4-digit codes: 7100, 7200, etc.)
            sulawesi_domains = [d for d in domains if d.get("domain_id", "").startswith(("71", "72", "73", "74", "75", "76"))]
            print(f"   Sulawesi provinces ({len([d for d in sulawesi_domains if len(d.get('domain_id', '')) == 4])}):")
            for domain in sulawesi_domains[:6]:  # Show province level only
                if len(domain.get("domain_id", "")) == 4:
                    print(f"   - {domain.get('domain_name', 'N/A')} (Code: {domain.get('domain_id', 'N/A')})")
        
        print("\n3. Listing dynamic tables (sample from national level)...")
        tables = client.list_dynamic_tables(domain="0000", page=1)
        if tables:
            print(f"   Found {len(tables)} dynamic tables on page 1")
            print("   Sample tables:")
            for i, table in enumerate(tables[:3], 1):
                print(f"   {i}. {table.get('title', 'N/A')}")
                print(f"      Var ID: {table.get('var', 'N/A')}")
                print(f"      Subject: {table.get('subcat', 'N/A')}")
        
        print("\n" + "="*80)
        print("✅ All tests passed! Client is ready.")
        print("="*80)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
