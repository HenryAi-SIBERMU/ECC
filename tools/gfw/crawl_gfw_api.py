#!/usr/bin/env python3
"""
GFW Data API Crawler
=====================

Crawls and documents the Global Forest Watch Data API endpoints.
Similar approach to BPS API documentation generation.

API Base: https://data-api.globalforestwatch.org
OpenAPI Spec: https://data-api.globalforestwatch.org/openapi.json
Production API (v1): https://production-api.globalforestwatch.org

Author: CELIOS Research Division
Date: 14 Juni 2026
"""

import requests
import json
import time
import logging
from datetime import datetime
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ── Configuration ──────────────────────────────────────────────
DATA_API = "https://data-api.globalforestwatch.org"
PROD_API = "https://production-api.globalforestwatch.org"
OUTPUT_DIR = Path(__file__).parent / "crawl_results"
OUTPUT_DIR.mkdir(exist_ok=True)

SULAWESI_PROVINCES = {
    'Sulawesi Utara': {'admin1': '31', 'bps': '71'},
    'Sulawesi Tengah': {'admin1': '29', 'bps': '72'},
    'Sulawesi Selatan': {'admin1': '30', 'bps': '73'},
    'Sulawesi Tenggara': {'admin1': '32', 'bps': '74'},
    'Gorontalo': {'admin1': '11', 'bps': '75'},
    'Sulawesi Barat': {'admin1': '33', 'bps': '76'},
}


def safe_request(url, params=None, method="GET", timeout=15):
    """Make a safe request with error handling."""
    try:
        if method == "GET":
            resp = requests.get(url, params=params, timeout=timeout)
        elif method == "POST":
            resp = requests.post(url, json=params, timeout=timeout)
        else:
            resp = requests.request(method, url, params=params, timeout=timeout)
        
        return {
            'url': resp.url,
            'status_code': resp.status_code,
            'headers': dict(resp.headers),
            'content_type': resp.headers.get('content-type', ''),
            'body_preview': resp.text[:2000] if resp.text else '',
            'json': resp.json() if 'json' in resp.headers.get('content-type', '') else None,
            'elapsed_ms': resp.elapsed.total_seconds() * 1000,
        }
    except Exception as e:
        return {
            'url': url,
            'status_code': None,
            'error': str(e),
            'elapsed_ms': None,
        }


def crawl_openapi_spec():
    """Fetch the OpenAPI specification."""
    logger.info("Fetching OpenAPI spec...")
    result = safe_request(f"{DATA_API}/openapi.json")
    
    if result['json']:
        spec = result['json']
        info = spec.get('info', {})
        paths = spec.get('paths', {})
        
        summary = {
            'title': info.get('title'),
            'version': info.get('version'),
            'description': info.get('description', '')[:500],
            'total_paths': len(paths),
            'base_url': spec.get('servers', [{}])[0].get('url', ''),
            'tags': [t.get('name') for t in spec.get('tags', [])],
            'paths_list': sorted(paths.keys()),
        }
        
        # Save full spec
        with open(OUTPUT_DIR / "openapi_spec.json", 'w', encoding='utf-8') as f:
            json.dump(spec, f, indent=2, ensure_ascii=False)
        
        # Save summary
        with open(OUTPUT_DIR / "openapi_summary.json", 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        logger.info(f"OpenAPI spec: {summary['title']} v{summary['version']}, {summary['total_paths']} paths")
        return spec
    
    return None


def crawl_datasets(page_size=50):
    """List all available datasets."""
    logger.info("Fetching datasets list...")
    all_datasets = []
    page = 1
    
    while True:
        result = safe_request(f"{DATA_API}/datasets", params={
            'page[number]': page,
            'page[size]': page_size,
        })
        
        if result['json'] and 'data' in result['json']:
            data = result['json']['data']
            if not data:
                break
            all_datasets.extend(data)
            logger.info(f"  Page {page}: {len(data)} datasets (total: {len(all_datasets)})")
            
            # Check for next page
            links = result['json'].get('links', {})
            if not links.get('next'):
                break
            page += 1
            time.sleep(0.5)
        else:
            break
    
    with open(OUTPUT_DIR / "datasets_list.json", 'w', encoding='utf-8') as f:
        json.dump(all_datasets, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Total datasets: {len(all_datasets)}")
    return all_datasets


def crawl_dataset_detail(dataset_id):
    """Get detail for a specific dataset."""
    logger.info(f"  Fetching dataset: {dataset_id}")
    result = safe_request(f"{DATA_API}/dataset/{dataset_id}")
    
    if result['json']:
        return result['json']
    return None


def crawl_dataset_versions(dataset_id):
    """Get versions for a dataset."""
    detail = crawl_dataset_detail(dataset_id)
    if detail and 'data' in detail:
        versions = detail['data'].get('versions', [])
        return versions
    return []


def crawl_dataset_version_detail(dataset_id, version):
    """Get version detail including assets and fields."""
    logger.info(f"  Fetching version detail: {dataset_id}/{version}")
    
    results = {}
    
    # Version metadata
    result = safe_request(f"{DATA_API}/dataset/{dataset_id}/{version}")
    if result['json']:
        results['version'] = result['json']
    
    # Fields
    result = safe_request(f"{DATA_API}/dataset/{dataset_id}/{version}/fields")
    if result['json']:
        results['fields'] = result['json']
    
    # Metadata
    result = safe_request(f"{DATA_API}/dataset/{dataset_id}/{version}/metadata")
    if result['json']:
        results['metadata'] = result['json']
    
    # Extent
    result = safe_request(f"{DATA_API}/dataset/{dataset_id}/{version}/extent")
    if result['json']:
        results['extent'] = result['json']
    
    return results


def crawl_query_endpoints():
    """Test query endpoints with sample data."""
    logger.info("Testing query endpoints...")
    
    results = {}
    
    # Key datasets for Sulawesi deforestation
    key_datasets = [
        'umd_tree_cover_loss',
        'umd_tree_cover_gain',
        'umd_tree_cover_density_2000',
        'umd_tree_cover_density_2010',
        'tsc_tree_cover_loss_drivers',
        'gfw_forest_carbon_gross_removals',
        'gfw_forest_carbon_gross_emissions',
        'nasa_viirs_fire_alerts',
        'wdpa_protected_areas',
        'idn_forest_area',
        'gfw_land_rights',
        'gfw_mining',
        'gfw_oil_palm',
        'gfw_wood_fiber',
    ]
    
    for ds in key_datasets:
        logger.info(f"  Testing dataset: {ds}")
        
        # Get dataset detail
        detail = safe_request(f"{DATA_API}/dataset/{ds}")
        if detail['json']:
            results[ds] = {
                'status': detail['status_code'],
                'data': detail['json'],
            }
            
            # Try to get latest version fields
            if 'data' in detail['json']:
                latest = detail['json']['data'].get('latest', {})
                version = latest.get('version', 'latest')
                
                fields_result = safe_request(f"{DATA_API}/dataset/{ds}/{version}/fields")
                if fields_result['json']:
                    results[ds]['fields'] = fields_result['json']
                
                metadata_result = safe_request(f"{DATA_API}/dataset/{ds}/{version}/metadata")
                if metadata_result['json']:
                    results[ds]['metadata'] = metadata_result['json']
        else:
            results[ds] = {'status': detail['status_code'], 'error': detail.get('error')}
        
        time.sleep(0.5)
    
    with open(OUTPUT_DIR / "key_datasets.json", 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    return results


def crawl_production_api():
    """Test production API (v1) endpoints."""
    logger.info("Testing production API (v1) endpoints...")
    
    results = {}
    
    # UMD Loss/Gain for Sulawesi Selatan
    endpoint = f"{PROD_API}/v1/umd-loss-gain"
    params = {'iso': 'IDN', 'admin1': '30', 'thresh': '30', 'period': '2020-01-01,2023-12-31'}
    result = safe_request(endpoint, params=params)
    results['umd-loss-gain'] = result
    logger.info(f"  umd-loss-gain: {result['status_code']}")
    
    time.sleep(1)
    
    # GLAD Alerts
    endpoint = f"{PROD_API}/v1/glad-alerts"
    params = {'iso': 'IDN', 'admin1': '30', 'dateRange': '2023-01-01,2024-12-31'}
    result = safe_request(endpoint, params=params)
    results['glad-alerts'] = result
    logger.info(f"  glad-alerts: {result['status_code']}")
    
    time.sleep(1)
    
    # Forest change by admin
    endpoint = f"{PROD_API}/v1/forest-change/umd-loss-gain/admin"
    params = {'iso': 'IDN', 'admin1': '30', 'thresh': '30', 'period': '2020-01-01,2023-12-31'}
    result = safe_request(endpoint, params=params)
    results['forest-change-admin'] = result
    logger.info(f"  forest-change-admin: {result['status_code']}")
    
    time.sleep(1)
    
    # Active fires (VIIRS)
    endpoint = f"{PROD_API}/v1/viirs-active-fires"
    params = {'iso': 'IDN', 'admin1': '30'}
    result = safe_request(endpoint, params=params)
    results['viirs-active-fires'] = result
    logger.info(f"  viirs-active-fires: {result['status_code']}")
    
    time.sleep(1)
    
    # Tree cover loss by driver (beta)
    endpoint = f"{DATA_API}/v0/land/tree_cover_loss_by_driver"
    params = {
        'canopy_cover': 30,
        'aoi': json.dumps({"type": "admin", "country": "IDN"})
    }
    result = safe_request(endpoint, params=params)
    results['tcl-by-driver'] = result
    logger.info(f"  tree-cover-loss-by-driver: {result['status_code']}")
    
    with open(OUTPUT_DIR / "production_api_results.json", 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False, default=str)
    
    return results


def crawl_geostore():
    """Test geostore endpoints."""
    logger.info("Testing geostore endpoints...")
    
    # Test get geostore for Indonesia (admin boundary)
    # Using GADM admin code for Indonesia
    result = safe_request(f"{DATA_API}/geostore/42e337ec66a2449e893a6b9be3371c59")
    
    if result['json']:
        with open(OUTPUT_DIR / "geostore_sample.json", 'w', encoding='utf-8') as f:
            json.dump(result['json'], f, indent=2, ensure_ascii=False)
    
    return result


def crawl_all_sulawesi_provinces():
    """Test data fetch for all Sulawesi provinces."""
    logger.info("Testing data for all Sulawesi provinces...")
    
    results = {}
    
    for prov_name, prov_info in SULAWESI_PROVINCES.items():
        admin1 = prov_info['admin1']
        logger.info(f"  Testing {prov_name} (admin1={admin1})...")
        
        # Test production API
        endpoint = f"{PROD_API}/v1/umd-loss-gain"
        params = {
            'iso': 'IDN',
            'admin1': admin1,
            'thresh': '30',
            'period': '2016-01-01,2023-12-31'
        }
        result = safe_request(endpoint, params=params)
        results[prov_name] = {
            'admin1': admin1,
            'status_code': result['status_code'],
            'response_preview': result.get('body_preview', '')[:1000],
        }
        
        time.sleep(1.5)
    
    with open(OUTPUT_DIR / "sulawesi_provinces_test.json", 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    return results


def generate_report():
    """Generate a summary report of all crawled endpoints."""
    logger.info("Generating crawl report...")
    
    report = []
    report.append(f"# GFW API Crawl Report")
    report.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"**Data API:** {DATA_API}")
    report.append(f"**Production API:** {PROD_API}")
    report.append("")
    
    # List files generated
    report.append("## Files Generated")
    for f in sorted(OUTPUT_DIR.iterdir()):
        if f.is_file() and f.name != "crawl_report.md":
            size = f.stat().st_size
            report.append(f"- `{f.name}` ({size:,} bytes)")
    
    report.append("")
    report.append("## Crawl Status")
    report.append("See individual JSON files for detailed results.")
    
    with open(OUTPUT_DIR / "crawl_report.md", 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))
    
    logger.info("Crawl report saved.")


def main():
    """Run all crawls."""
    logger.info("=" * 60)
    logger.info("GFW Data API Crawler — Starting")
    logger.info("=" * 60)
    
    # 1. Fetch OpenAPI spec
    spec = crawl_openapi_spec()
    
    # 2. List datasets
    datasets = crawl_datasets()
    
    # 3. Test key datasets
    crawl_query_endpoints()
    
    # 4. Test production API (v1)
    crawl_production_api()
    
    # 5. Test geostore
    crawl_geostore()
    
    # 6. Test all Sulawesi provinces
    crawl_all_sulawesi_provinces()
    
    # 7. Generate report
    generate_report()
    
    logger.info("=" * 60)
    logger.info("GFW Data API Crawler — Complete!")
    logger.info(f"Results saved to: {OUTPUT_DIR}")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
