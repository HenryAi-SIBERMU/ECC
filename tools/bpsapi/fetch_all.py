#!/usr/bin/env python3
"""
Fetch All Data - Batch Script
CELIOS ECC Intelligence System

Fetch semua data yang diperlukan:
- Ekspor per sektor
- PAD per kabupaten/kota
"""

import argparse
from datetime import datetime

from bps_client import BPSClient
from fetch_ekspor import fetch_ekspor_sulawesi
from fetch_pad_sulawesi import fetch_pad_sulawesi


def main():
    """Batch fetch all data"""
    parser = argparse.ArgumentParser(
        description="Fetch ALL data dari BPS API untuk ECC analysis"
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
        "--output-dir",
        default="output",
        help="Output directory"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    print("="*80)
    print("BPS Data Fetcher - CELIOS ECC")
    print("="*80)
    print(f"Time range: {args.tahun_awal} - {args.tahun_akhir}")
    print(f"Output dir: {args.output_dir}")
    print("="*80)
    
    # Initialize client
    api_key = "06fd644648629502353deaed29fc6383"
    client = BPSClient(api_key=api_key, verbose=args.verbose)
    
    # Test connection
    print("\n1. Testing API connection...")
    if not client.test_connection():
        print("❌ Failed to connect to BPS API")
        return
    print("✅ Connected!")
    
    # Fetch ekspor data
    print("\n2. Fetching EKSPOR data...")
    print("-" * 80)
    ekspor_data = fetch_ekspor_sulawesi(
        client,
        tahun_awal=args.tahun_awal,
        tahun_akhir=args.tahun_akhir
    )
    
    if ekspor_data:
        output_path = f"{args.output_dir}/ekspor_sulawesi_{args.tahun_awal}_{args.tahun_akhir}.csv"
        client.export_to_csv(ekspor_data, output_path)
        client.export_to_json(ekspor_data, output_path.replace('.csv', '.json'))
        print(f"✅ Ekspor data saved: {len(ekspor_data)} entries")
    else:
        print("⚠️  No ekspor data retrieved")
    
    # Fetch PAD data
    print("\n3. Fetching PAD data...")
    print("-" * 80)
    pad_data = fetch_pad_sulawesi(
        client,
        tahun_awal=args.tahun_awal,
        tahun_akhir=args.tahun_akhir
    )
    
    if pad_data:
        output_path = f"{args.output_dir}/pad_sulawesi_{args.tahun_awal}_{args.tahun_akhir}.csv"
        client.export_to_csv(pad_data, output_path)
        client.export_to_json(pad_data, output_path.replace('.csv', '.json'))
        print(f"✅ PAD data saved: {len(pad_data)} entries")
    else:
        print("⚠️  No PAD data retrieved")
    
    # Summary
    print("\n" + "="*80)
    print("📊 SUMMARY")
    print("="*80)
    print(f"Ekspor data: {len(ekspor_data)} entries")
    print(f"PAD data:    {len(pad_data)} entries")
    print(f"Total:       {len(ekspor_data) + len(pad_data)} entries")
    print(f"\n📁 Output directory: {args.output_dir}/")
    print("="*80)
    print("✅ All data fetched successfully!")
    print("="*80)


if __name__ == "__main__":
    main()
