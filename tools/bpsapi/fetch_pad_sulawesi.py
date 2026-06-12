#!/usr/bin/env python3
"""
Fetch PAD (Pendapatan Asli Daerah) Data from BPS API
CELIOS ECC Intelligence System

Fetch PAD per Kabupaten/Kota di Sulawesi
"""

import argparse
from datetime import datetime
from tqdm import tqdm

from bps_client import BPSClient
from utils.province_codes import SULAWESI_PROVINCES, get_province_name


def fetch_pad_sulawesi(
    client: BPSClient,
    tahun_awal: int = 2016,
    tahun_akhir: int = 2026
) -> list:
    """
    Fetch PAD data untuk semua kabupaten/kota di Sulawesi
    
    Args:
        client: BPSClient instance
        tahun_awal: Start year
        tahun_akhir: End year
        
    Returns:
        List of PAD data
    """
    all_data = []
    
    print(f"\n📊 Fetching PAD data ({tahun_awal}-{tahun_akhir})...")
    print(f"Target: Kabupaten/Kota di {len(SULAWESI_PROVINCES)} provinsi Sulawesi")
    
    for prov_code, prov_name in tqdm(SULAWESI_PROVINCES.items(), desc="Provinces"):
        for tahun in range(tahun_awal, tahun_akhir + 1):
            try:
                # BPS API: PAD data by province and year
                # Model code perlu disesuaikan dengan BPS API documentation
                data = client.get_data(
                    model="pad",  # Akan di-adjust sesuai BPS API
                    domain=prov_code,
                    tahun=tahun
                )
                
                # Process and enrich data
                for entry in data:
                    enriched = {
                        "tahun": tahun,
                        "kode_provinsi": prov_code,
                        "nama_provinsi": prov_name,
                        "scraped_at": datetime.now().isoformat(),
                        **entry  # Merge dengan data dari API
                    }
                    all_data.append(enriched)
                
            except Exception as e:
                client.logger.warning(f"Failed to fetch PAD {prov_name} {tahun}: {e}")
                continue
    
    print(f"\n✅ Total data fetched: {len(all_data)} entries")
    return all_data


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Fetch PAD data dari BPS API untuk Sulawesi"
    )
    parser.add_argument(
        "--tahun-awal",
        type=int,
        default=2016,
        help="Start year (default: 2016)"
    )
    parser.add_argument(
        "--tahun-akhir",
        type=int,
        default=2026,
        help="End year (default: 2026)"
    )
    parser.add_argument(
        "--output",
        default="output/pad_sulawesi.csv",
        help="Output file path"
    )
    parser.add_argument(
        "--format",
        choices=["csv", "json", "xlsx"],
        default="csv",
        help="Output format"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    # Initialize client
    api_key = "06fd644648629502353deaed29fc6383"
    client = BPSClient(api_key=api_key, verbose=args.verbose)
    
    # Test connection
    if not client.test_connection():
        print("❌ Failed to connect to BPS API")
        return
    
    # Fetch data
    data = fetch_pad_sulawesi(
        client,
        tahun_awal=args.tahun_awal,
        tahun_akhir=args.tahun_akhir
    )
    
    if not data:
        print("⚠️  No data retrieved")
        return
    
    # Export
    output_path = args.output
    if args.format == "csv":
        client.export_to_csv(data, output_path)
    elif args.format == "json":
        client.export_to_json(data, output_path)
    elif args.format == "xlsx":
        client.export_to_excel(data, output_path)
    
    print(f"\n✅ Success!")
    print(f"📁 Output: {output_path}")
    print(f"📊 Total entries: {len(data)}")


if __name__ == "__main__":
    main()
