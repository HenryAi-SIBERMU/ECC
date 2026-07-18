"""Aggregate downloaded Sentinel-5P/TROPOMI NetCDF files over a bbox.

Uses h5py to avoid requiring netCDF4/xarray. This script targets common S5P L2
products from GES DISC. It tries known variable paths for NO2/SO2/CO/AER_AI and
computes simple mean/median/min/max over pixels inside the bbox.

Example:
    python tools/nasa_sentinel5p/process_tropomi_bbox.py --input-dir data/raw/nasa_sentinel5p/granules --product NO2
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

import h5py
import numpy as np


SULAWESI_BBOX = (118.0, -6.5, 126.0, 2.5)  # west,south,east,north

PRODUCT_PATHS = {
    "NO2": [
        "/PRODUCT/nitrogendioxide_tropospheric_column",
        "/PRODUCT/SUPPORT_DATA/DETAILED_RESULTS/nitrogendioxide_tropospheric_column",
        "/SCIENCE_DATA/ColumnAmountNO2Trop",
    ],
    "SO2": [
        "/PRODUCT/sulfurdioxide_total_vertical_column",
        "/PRODUCT/sulfurdioxide_total_vertical_column_1km",
    ],
    "CO": [
        "/PRODUCT/carbonmonoxide_total_column",
    ],
    "AER_AI": [
        "/PRODUCT/aerosol_index_354_388",
    ],
}

QUALITY_PATHS = {
    "NO2": ["/PRODUCT/qa_value", "/SCIENCE_DATA/qa_value"],
    "SO2": ["/PRODUCT/qa_value", "/SCIENCE_DATA/qa_value"],
    "CO": ["/PRODUCT/qa_value", "/SCIENCE_DATA/qa_value"],
    "AER_AI": ["/PRODUCT/qa_value", "/SCIENCE_DATA/qa_value"],
}


def find_dataset(h5: h5py.File, paths: list[str]) -> str | None:
    for path in paths:
        if path in h5:
            return path
    return None


def read_array(h5: h5py.File, path: str) -> np.ndarray:
    arr = h5[path][()]
    arr = np.asarray(arr)
    return np.squeeze(arr)


def parse_date(filename: str) -> str:
    match = re.search(r"__(\d{8})T", filename)
    if match:
        raw = match.group(1)
        return f"{raw[:4]}-{raw[4:6]}-{raw[6:]}"
    
    match2 = re.search(r"_(\d{4})m(\d{4})t", filename)
    if match2:
        y = match2.group(1)
        md = match2.group(2)
        return f"{y}-{md[:2]}-{md[2:]}"
        
    return ""


LAT_PATHS = ["/PRODUCT/latitude", "/GEOLOCATION_DATA/Latitude"]
LON_PATHS = ["/PRODUCT/longitude", "/GEOLOCATION_DATA/Longitude"]


def aggregate_file(path: Path, product: str, bbox: tuple[float, float, float, float], qa_min: float) -> dict:
    west, south, east, north = bbox
    with h5py.File(path, "r") as h5:
        lat = read_array(h5, find_dataset(h5, LAT_PATHS) or "/PRODUCT/latitude")
        lon = read_array(h5, find_dataset(h5, LON_PATHS) or "/PRODUCT/longitude")
        var_path = find_dataset(h5, PRODUCT_PATHS[product])
        if not var_path:
            raise KeyError(f"No known {product} variable path found in {path.name}")
        ds = h5[var_path]
        values = read_array(h5, var_path).astype(float)

        # Filter fill values
        fill_value = ds.attrs.get("_FillValue")
        if fill_value is not None:
            fill_value = float(np.asarray(fill_value).flat[0])
            values = np.where(np.abs(values - fill_value) > np.abs(fill_value) * 0.01, values, np.nan)
        
        # Filter valid range
        valid_min = ds.attrs.get("valid_min")
        valid_max = ds.attrs.get("valid_max")
        if valid_min is not None and valid_max is not None:
            vmin, vmax = float(valid_min), float(valid_max)
            values = np.where((values >= vmin) & (values <= vmax), values, np.nan)

        mask = (lon >= west) & (lon <= east) & (lat >= south) & (lat <= north)
        qa_paths = QUALITY_PATHS.get(product, [])
        if isinstance(qa_paths, str):
            qa_paths = [qa_paths]
        for qa_path in qa_paths:
            if qa_path and qa_path in h5:
                qa = read_array(h5, qa_path).astype(float)
                mask = mask & (qa >= qa_min)
                break

        values = np.where(np.isfinite(values), values, np.nan)
        selected = values[mask]
        selected = selected[np.isfinite(selected)]
        
        # Convert molec/cm² to mol/m² if needed
        units = ds.attrs.get("units", b"").decode() if isinstance(ds.attrs.get("units"), bytes) else str(ds.attrs.get("units", ""))
        if "molec/cm2" in units.lower():
            selected = selected / 6.02214076e23 * 1e4  # molec/cm² → mol/m²
        if selected.size == 0:
            return {
                "file": path.name,
                "date": parse_date(path.name),
                "product": product,
                "variable_path": var_path,
                "pixel_count": 0,
                "mean": "",
                "median": "",
                "min": "",
                "max": "",
            }
        return {
            "file": path.name,
            "date": parse_date(path.name),
            "product": product,
            "variable_path": var_path,
            "pixel_count": int(selected.size),
            "mean": float(np.nanmean(selected)),
            "median": float(np.nanmedian(selected)),
            "min": float(np.nanmin(selected)),
            "max": float(np.nanmax(selected)),
        }


def main() -> int:
    parser = argparse.ArgumentParser(description="Aggregate TROPOMI NetCDF files over Sulawesi bbox.")
    parser.add_argument("--input-dir", default="data/raw/nasa_sentinel5p/granules", help="Directory with .nc files.")
    parser.add_argument("--product", choices=sorted(PRODUCT_PATHS), required=True, help="NO2, SO2, CO, or AER_AI.")
    parser.add_argument("--bbox", default=",".join(map(str, SULAWESI_BBOX)), help="west,south,east,north")
    parser.add_argument("--qa-min", type=float, default=0.5, help="Minimum qa_value if present.")
    parser.add_argument("--out", default=None, help="Output CSV path.")
    args = parser.parse_args()

    bbox = tuple(float(x) for x in args.bbox.split(","))
    if len(bbox) != 4:
        raise ValueError("--bbox must be west,south,east,north")

    input_dir = Path(args.input_dir)
    files = sorted(input_dir.glob("*.nc"))
    rows = []
    for path in files:
        if f"__{args.product}" not in path.name and args.product not in path.name:
            # Keep permissive for AER_AI/CO naming, but skip obvious other product files.
            if args.product in {"NO2", "SO2"}:
                continue
        try:
            rows.append(aggregate_file(path, args.product, bbox, args.qa_min))
            print(f"Processed: {path.name}")
        except Exception as exc:  # noqa: BLE001 - report per-file failure and continue.
            print(f"WARN: failed {path.name}: {exc}")

    out = args.out or f"data/processed/sulawesi_tropomi_{args.product.lower()}_bbox_aggregates.csv"
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["file", "date", "product", "variable_path", "pixel_count", "mean", "median", "min", "max"]
    with open(out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Rows written: {len(rows)} -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
