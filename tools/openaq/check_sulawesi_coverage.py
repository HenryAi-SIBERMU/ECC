"""Check OpenAQ v3 coverage for Sulawesi.

This tool verifies whether OpenAQ has ground-monitor stations inside a Sulawesi
bounding box. It does not assume coverage exists. OpenAQ v3 requires an API key:
set OPENAQ_API_KEY before running.

Example:
    set OPENAQ_API_KEY=your_key
    python tools/openaq/check_sulawesi_coverage.py --out data/raw/openaq/sulawesi_locations.csv
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path


BASE_URL = "https://api.openaq.org/v3"

# Approximate Sulawesi bounding box: west,south,east,north
SULAWESI_BBOX = "118.0,-6.5,126.0,2.5"


def request_json(path: str, params: dict[str, object], api_key: str) -> dict:
    query = urllib.parse.urlencode(params, doseq=True)
    url = f"{BASE_URL}{path}?{query}"
    req = urllib.request.Request(url, headers={"X-API-Key": api_key})
    with urllib.request.urlopen(req, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def flatten_location(row: dict) -> dict:
    country = row.get("country") or {}
    provider = row.get("provider") or {}
    owner = row.get("owner") or {}
    coords = row.get("coordinates") or {}
    sensors = row.get("sensors") or []
    parameters = []
    for sensor in sensors:
        parameter = sensor.get("parameter") or {}
        name = parameter.get("name")
        if name:
            parameters.append(name)
    return {
        "id": row.get("id"),
        "name": row.get("name"),
        "locality": row.get("locality"),
        "country_code": country.get("code"),
        "country_name": country.get("name"),
        "provider": provider.get("name"),
        "owner": owner.get("name"),
        "latitude": coords.get("latitude"),
        "longitude": coords.get("longitude"),
        "datetime_first": (row.get("datetimeFirst") or {}).get("utc") if isinstance(row.get("datetimeFirst"), dict) else row.get("datetimeFirst"),
        "datetime_last": (row.get("datetimeLast") or {}).get("utc") if isinstance(row.get("datetimeLast"), dict) else row.get("datetimeLast"),
        "parameters": ";".join(sorted(set(parameters))),
    }


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "id",
        "name",
        "locality",
        "country_code",
        "country_name",
        "provider",
        "owner",
        "latitude",
        "longitude",
        "datetime_first",
        "datetime_last",
        "parameters",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check OpenAQ station coverage for Sulawesi.")
    parser.add_argument("--bbox", default=SULAWESI_BBOX, help="west,south,east,north bbox. Default: Sulawesi.")
    parser.add_argument("--limit", type=int, default=1000, help="OpenAQ page size.")
    parser.add_argument("--out", default="data/raw/openaq/sulawesi_locations.csv", help="Output CSV path.")
    args = parser.parse_args()

    api_key = os.getenv("OPENAQ_API_KEY")
    if not api_key:
        print("ERROR: OPENAQ_API_KEY is not set. Register at https://explore.openaq.org.", file=sys.stderr)
        return 2

    params = {
        "bbox": args.bbox,
        "limit": args.limit,
        "page": 1,
    }
    try:
        data = request_json("/locations", params, api_key)
    except Exception as exc:  # noqa: BLE001 - CLI tool should report any API/network error.
        print(f"ERROR: OpenAQ request failed: {exc}", file=sys.stderr)
        return 1

    results = data.get("results") or []
    rows = [flatten_location(row) for row in results]
    write_csv(Path(args.out), rows)

    found = (data.get("meta") or {}).get("found", len(rows))
    print(f"OpenAQ locations found in bbox {args.bbox}: {found}")
    print(f"Rows written: {len(rows)} -> {args.out}")
    if not rows:
        print("No OpenAQ ground-monitor locations found for this bbox.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
