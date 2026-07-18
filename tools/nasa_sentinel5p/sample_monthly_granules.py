"""Sample one granule per year from CMR search results for download."""

from __future__ import annotations

import csv
import sys
from datetime import datetime
from pathlib import Path


def sample_granules(years: list[int], base_dir: Path) -> list[dict]:
    """Pick one granule per year (mid-year preferred) from existing CSVs."""
    sampled = []
    for year in years:
        csv_path = base_dir / f"sulawesi_tropomi_no2_{year}_granules.csv"
        if not csv_path.exists():
            print(f"WARN: {csv_path} not found, skipping")
            continue
        
        rows = []
        with csv_path.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
        
        if not rows:
            print(f"WARN: no rows in {csv_path}")
            continue
        
        # Pick 4 granules per year (March, June, September, December)
        targets = [
            datetime(year, 3, 1),
            datetime(year, 6, 1),
            datetime(year, 9, 1),
            datetime(year, 12, 1)
        ]
        
        for target in targets:
            def time_diff(row):
                ts = (row.get("time_start") or "")[:10]
                try:
                    dt = datetime.strptime(ts, "%Y-%m-%d")
                    return abs((dt - target).days)
                except ValueError:
                    return 9999
            
            best = min(rows, key=time_diff)
            if best not in sampled:
                sampled.append(best)
                print(f"{year} (target {target.strftime('%b')}): selected {best.get('time_start', '?')[:10]} | {best.get('size_mb', '?')} MB")
    
    return sampled


def write_sample_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    base_dir = Path("data/raw/nasa_sentinel5p")
    years = list(range(2018, 2025))
    sampled = sample_granules(years, base_dir)
    
    out = base_dir / "sulawesi_tropomi_no2_sample_download.csv"
    write_sample_csv(out, sampled)
    print(f"\nSampled {len(sampled)} granules -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
