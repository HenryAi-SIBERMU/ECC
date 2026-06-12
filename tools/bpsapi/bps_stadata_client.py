#!/usr/bin/env python3
"""
BPS Client using Official Stadata Package
CELIOS ECC Intelligence System

Wrapper around the official stadata package for easier data retrieval
"""

import logging
from typing import List, Dict, Optional
from pathlib import Path
from datetime import datetime

import stadata
import pandas as pd


class BPSStadataClient:
    """Client wrapper for BPS Stadata package"""
    
    def __init__(
        self,
        api_key: str,
        verbose: bool = False
    ):
        """
        Initialize BPS Stadata Client
        
        Args:
            api_key: BPS API key
            verbose: Enable verbose logging
        """
        self.api_key = api_key
        self.client = stadata.Client(api_key)
        self.logger = self._setup_logger(verbose)
        self.logger.info("BPS Stadata Client initialized")
    
    def _setup_logger(self, verbose: bool) -> logging.Logger:
        """Setup logging"""
        logger = logging.getLogger("BPSStadataClient")
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
    
    def list_domains(self) -> pd.DataFrame:
        """
        List all available domains (provinces and regencies)
        
        Returns:
            DataFrame of domains
        """
        try:
            domains = self.client.list_domain()
            self.logger.info(f"Found {len(domains)} domains")
            return domains
        except Exception as e:
            self.logger.error(f"Failed to list domains: {e}")
            return pd.DataFrame()
    
    def list_dynamic_tables(
        self,
        domains: List[str],
        keyword: Optional[str] = None
    ) -> pd.DataFrame:
        """
        List dynamic tables for specified domains
        
        Args:
            domains: List of domain codes (e.g., ['7100', '7200'])
            keyword: Optional keyword to filter tables
            
        Returns:
            DataFrame of dynamic tables
        """
        try:
            self.logger.info(f"Listing dynamic tables for {len(domains)} domains...")
            tables = self.client.list_dynamictable(all=False, domain=domains)
            
            df = pd.DataFrame(tables)
            
            # Filter by keyword if provided
            if keyword and not df.empty:
                df = df[df['title'].str.contains(keyword, case=False, na=False)]
                self.logger.info(f"Found {len(df)} tables matching '{keyword}'")
            else:
                self.logger.info(f"Found {len(df)} dynamic tables")
            
            return df
        except Exception as e:
            self.logger.error(f"Failed to list dynamic tables: {e}")
            return pd.DataFrame()
    
    def get_dynamic_table(
        self,
        domain: str,
        var_id: str,
        year: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Get data from a specific dynamic table
        
        Args:
            domain: Domain code (e.g., '7100')
            var_id: Variable ID from dynamic table list
            year: Optional year filter
            
        Returns:
            DataFrame of table data
        """
        try:
            self.logger.info(f"Fetching dynamic table: domain={domain}, var={var_id}, year={year}")
            
            data = self.client.view_dynamictable(
                domain=domain,
                var=var_id,
                th=year if year else ''
            )
            
            df = pd.DataFrame(data)
            self.logger.info(f"Retrieved {len(df)} rows")
            return df
        except Exception as e:
            self.logger.error(f"Failed to get dynamic table: {e}")
            return pd.DataFrame()
    
    def export_to_csv(self, df: pd.DataFrame, output_path: str):
        """Export DataFrame to CSV"""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        self.logger.info(f"Exported {len(df)} rows to {output_path}")
    
    def export_to_excel(self, df: pd.DataFrame, output_path: str):
        """Export DataFrame to Excel"""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        df.to_excel(output_path, index=False, engine='openpyxl')
        self.logger.info(f"Exported {len(df)} rows to {output_path}")
    
    def export_to_json(self, df: pd.DataFrame, output_path: str):
        """Export DataFrame to JSON"""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        df.to_json(output_path, orient='records', force_ascii=False, indent=2)
        self.logger.info(f"Exported {len(df)} rows to {output_path}")


if __name__ == "__main__":
    # Quick test
    import sys
    
    api_key = "06fd644648629502353deaed29fc6383"
    
    print("="*80)
    print("BPS Stadata Client - Test")
    print("="*80)
    
    try:
        client = BPSStadataClient(api_key=api_key, verbose=True)
        
        print("\n1. Testing domains...")
        domains = client.list_domains()
        if not domains.empty:
            print(f"   ✅ Found {len(domains)} domains")
            
            # Find Sulawesi provinces
            sulawesi = domains[
                (domains['domain_id'].str.startswith(('71', '72', '73', '74', '75', '76'))) & 
                (domains['domain_id'].str.len() == 4)
            ]
            print(f"\n   Sulawesi Provinces ({len(sulawesi)}):")
            for idx, prov in sulawesi.iterrows():
                print(f"   - {prov['domain_name']} (Code: {prov['domain_id']})")
        
        print("\n2. Testing dynamic tables (Sulawesi Selatan - 7300)...")
        tables = client.list_dynamic_tables(domains=['7300'])
        if not tables.empty:
            print(f"   ✅ Found {len(tables)} dynamic tables")
            print(f"\n   Sample tables (first 5):")
            for idx, row in tables.head().iterrows():
                print(f"   {idx+1}. {row['title']}")
                print(f"      Var ID: {row.get('var_id', 'N/A')}")
        
        print("\n" + "="*80)
        print("✅ All tests passed!")
        print("="*80)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
