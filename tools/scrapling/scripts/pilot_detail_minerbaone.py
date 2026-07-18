#!/usr/bin/env python3
"""
MinerbaOne Detail Page Pilot
Test scraping detail pages untuk beberapa companies

Usage:
    python pilot_detail_minerbaone.py --sample 5
"""

import argparse
import sys
import json
import requests
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import pandas as pd

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))
from scraper_base import BaseScraper


class MinerbaOneDetailPilot(BaseScraper):
    """Pilot scraper untuk test detail pages"""
    
    def __init__(self, delay: float = 1.0, verbose: bool = False):
        super().__init__(name="minerbaone_detail", delay=delay, verbose=verbose)
        self.base_url = "https://minerbaone.esdm.go.id"
    
    def test_detail_api(self, company_id: str) -> Dict:
        """
        Test apakah ada API endpoint untuk detail page
        
        Args:
            company_id: ID badan usaha
            
        Returns:
            Dict dengan test results
        """
        # Try common API patterns
        api_patterns = [
            f"/api/common/v2/publik/badan-usaha/{company_id}",
            f"/api/common/v2/publik/badan-usaha/{company_id}/detail",
            f"/api/publik/badan-usaha/{company_id}",
            f"/api/v1/publik/badan-usaha/{company_id}",
        ]
        
        results = {
            'company_id': company_id,
            'api_found': False,
            'working_endpoint': None,
            'response_sample': None,
            'needs_browser': False
        }
        
        for pattern in api_patterns:
            url = self.base_url + pattern
            
            try:
                self.logger.debug(f"Testing API: {url}")
                response = self.session.get(url, timeout=10)
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        
                        # Check if it has meaningful data (not just {"message": "Not Found"})
                        if data and len(str(data)) > 100:
                            self.logger.info(f"✅ Found working API: {pattern}")
                            results['api_found'] = True
                            results['working_endpoint'] = pattern
                            results['response_sample'] = data
                            
                            # Save sample response
                            output_dir = Path("output/pilot")
                            output_dir.mkdir(parents=True, exist_ok=True)
                            sample_path = output_dir / f"api_detail_{company_id}.json"
                            with open(sample_path, 'w', encoding='utf-8') as f:
                                json.dump(data, f, indent=2, ensure_ascii=False)
                            
                            self.logger.info(f"📄 Sample saved: {sample_path}")
                            return results
                        
                    except json.JSONDecodeError:
                        pass
                
            except Exception as e:
                self.logger.debug(f"Failed {pattern}: {e}")
                continue
        
        # No API found, will need browser automation
        self.logger.warning(f"❌ No API endpoint found for {company_id}")
        results['needs_browser'] = True
        
        return results
    
    def test_sample_companies(self, sample_size: int = 5) -> List[Dict]:
        """
        Test scraping detail untuk sample companies
        
        Args:
            sample_size: Number of companies to test
            
        Returns:
            List of test results
        """
        # Load companies from Opsi 1 result
        companies_file = Path("output/minerbaone_companies.csv")
        
        if not companies_file.exists():
            self.logger.error(f"❌ Companies file not found: {companies_file}")
            self.logger.info("   Please run Opsi 1 first!")
            return []
        
        # Read companies
        df = pd.read_csv(companies_file)
        self.logger.info(f"📊 Loaded {len(df)} companies from Opsi 1")
        
        # Get sample (first N + some random ones from middle)
        sample_df = pd.concat([
            df.head(3),  # First 3
            df.iloc[100:100+sample_size-3]  # Some from middle
        ])
        
        self.logger.info(f"🎯 Testing {len(sample_df)} sample companies...")
        
        results = []
        
        for idx, row in sample_df.iterrows():
            company_id = str(row['id_badan_usaha'])
            company_name = row['nama_badan_usaha']
            
            self.logger.info(f"\n{'='*60}")
            self.logger.info(f"Testing: {company_name} (ID: {company_id})")
            self.logger.info(f"{'='*60}")
            
            result = self.test_detail_api(company_id)
            result['company_name'] = company_name
            result['detail_url'] = row.get('detail_url', f"https://minerbaone.esdm.go.id/publik/badan-usaha/{company_id}")
            
            results.append(result)
            
            # Rate limit
            self._rate_limit()
        
        return results
    
    def analyze_results(self, results: List[Dict]) -> Dict:
        """Analyze test results"""
        
        total = len(results)
        api_found = sum(1 for r in results if r['api_found'])
        needs_browser = sum(1 for r in results if r['needs_browser'])
        
        analysis = {
            'total_tested': total,
            'api_available': api_found,
            'needs_browser': needs_browser,
            'success_rate': (api_found / total * 100) if total > 0 else 0
        }
        
        self.logger.info(f"\n{'='*60}")
        self.logger.info(f"PILOT TEST RESULTS")
        self.logger.info(f"{'='*60}")
        self.logger.info(f"Total tested: {total}")
        self.logger.info(f"✅ API available: {api_found} ({analysis['success_rate']:.1f}%)")
        self.logger.info(f"❌ Needs browser: {needs_browser}")
        
        if api_found > 0:
            # Find working endpoint
            working = next((r for r in results if r['api_found']), None)
            if working:
                self.logger.info(f"\n🎯 Working API pattern: {working['working_endpoint']}")
                self.logger.info(f"   Sample response keys: {list(working['response_sample'].keys())}")
        
        # Save analysis
        output_dir = Path("output/pilot")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        analysis_path = output_dir / "pilot_analysis.json"
        with open(analysis_path, 'w', encoding='utf-8') as f:
            json.dump({
                'analysis': analysis,
                'results': results
            }, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"\n📄 Full results saved: {analysis_path}")
        
        return analysis


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Pilot test for MinerbaOne detail page scraping"
    )
    parser.add_argument(
        "--sample",
        type=int,
        default=5,
        help="Number of companies to test (default: 5)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    print("="*60)
    print("MinerbaOne Detail Page Pilot Test")
    print("="*60)
    print(f"Sample size: {args.sample} companies")
    print("="*60)
    
    pilot = MinerbaOneDetailPilot(delay=1.0, verbose=args.verbose)
    
    try:
        # Test sample companies
        results = pilot.test_sample_companies(sample_size=args.sample)
        
        if not results:
            print("\n❌ No results. Please check if Opsi 1 data exists.")
            return
        
        # Analyze results
        analysis = pilot.analyze_results(results)
        
        # Recommendation
        print(f"\n{'='*60}")
        print("RECOMMENDATION")
        print(f"{'='*60}")
        
        if analysis['success_rate'] >= 80:
            print("✅ API approach recommended!")
            print("   → Fast scraping with requests (similar to Opsi 1)")
            print(f"   → Estimated time: ~2-3 hours for 7,527 companies")
        elif analysis['success_rate'] > 0:
            print("⚠️  Mixed results - API partially available")
            print("   → May need hybrid approach")
        else:
            print("❌ Browser automation required")
            print("   → Slow scraping with Scrapling/Playwright")
            print(f"   → Estimated time: ~5-8 hours for 7,527 companies")
        
        print(f"{'='*60}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
