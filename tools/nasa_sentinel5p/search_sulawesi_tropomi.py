"""Search NASA CMR for Sentinel-5P/TROPOMI granules over Sulawesi.

This tool uses NASA Earthdata CMR metadata search. Collection/granule metadata
search is public; downloading science files usually requires Earthdata Login.

The first step is discovery: confirm which Sentinel-5P/TROPOMI collections and
granules overlap Sulawesi for NO2/SO2/CO/aerosol proxies.

Example:
    python tools/nasa_sentinel5p/search_sulawesi_tropomi.py --keyword NO2 --year 2024
    python tools/nasa_sentinel5p/search_sulawesi_tropomi.py --keyword SO2 --year 2024 --out data/raw/nasa_sentinel5p/sulawesi_so2_granules_2024.csv
"""

from __future__ import annotations

import argparse
import csv
import json
import urllib.parse
import urllib.request
from pathlib import Path


CMR_URL = "https://cmr.earthdata.nasa.gov/search"
SULAWESI_BBOX = "118.0,-6.5,126.0,2.5"  # west,south,east,north


def get_json(endpoint: str, params: dict[str, object]) -> dict:
    query = urllib.parse.urlencode(params, doseq=True)
    url = f"{CMR_URL}/{endpoint}.json?{query}"
    req = urllib.request.Request(url, headers={"Client-Id": "celios-d3tlh-sentinel5p-tool"})
    with urllib.request.urlopen(req, timeout=90) as response:
        return json.loads(response.read().decode("utf-8"))


def search_collections(keyword: str, page_size: int = 10) -> list[dict]:
    params = {
        "keyword": f"Sentinel-5P TROPOMI {keyword}",
        "page_size": page_size,
        "sort_key": "-usage_score",
    }
    data = get_json("collections", params)
    entries = (data.get("feed") or {}).get("entry") or []
    keyword_l = keyword.lower()
    filtered = []
    for entry in entries:
        haystack = f"{entry.get('short_name') or ''} {entry.get('title') or ''}".lower()
        if keyword_l in haystack:
            filtered.append(entry)
    return filtered or entries


def search_granules(collection_concept_id: str, bbox: str, temporal: str, page_size: int) -> list[dict]:
    params = {
        "collection_concept_id": collection_concept_id,
        "bounding_box": bbox,
        "temporal": temporal,
        "page_size": page_size,
        "sort_key": "-start_date",
    }
    data = get_json("granules", params)
    return (data.get("feed") or {}).get("entry") or []


def granule_links(entry: dict) -> tuple[str, str]:
    links = entry.get("links") or []
    data_links = []
    browse_links = []
    for link in links:
        href = link.get("href") or ""
        rel = link.get("rel") or ""
        inherited = link.get("inherited")
        if inherited:
            continue
        if "data#" in rel or "data" in rel:
            data_links.append(href)
        if "browse" in rel:
            browse_links.append(href)
    return ";".join(data_links[:5]), ";".join(browse_links[:5])


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "keyword",
        "collection_concept_id",
        "collection_short_name",
        "collection_title",
        "granule_id",
        "title",
        "time_start",
        "time_end",
        "size_mb",
        "producer_granule_id",
        "data_links",
        "browse_links",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Search NASA CMR Sentinel-5P/TROPOMI granules over Sulawesi.")
    parser.add_argument("--keyword", default="NO2", help="Pollutant keyword, e.g. NO2, SO2, CO, aerosol.")
    parser.add_argument("--year", type=int, default=2024, help="Year to query.")
    parser.add_argument("--bbox", default=SULAWESI_BBOX, help="west,south,east,north bbox.")
    parser.add_argument("--page-size", type=int, default=2000, help="Granules per collection.")
    parser.add_argument("--out", default=None, help="Output CSV path.")
    args = parser.parse_args()

    temporal = f"{args.year}-01-01T00:00:00Z,{args.year}-12-31T23:59:59Z"
    collections = search_collections(args.keyword, page_size=10)
    print(f"Collections found for Sentinel-5P TROPOMI {args.keyword}: {len(collections)}")

    rows: list[dict] = []
    for coll in collections:
        concept_id = coll.get("id")
        if not concept_id:
            continue
        short_name = coll.get("short_name") or ""
        title = coll.get("title") or ""
        granules = search_granules(concept_id, args.bbox, temporal, args.page_size)
        print(f"{concept_id} | {short_name} | granules over bbox/year: {len(granules)}")
        for granule in granules:
            data_links, browse_links = granule_links(granule)
            rows.append({
                "keyword": args.keyword,
                "collection_concept_id": concept_id,
                "collection_short_name": short_name,
                "collection_title": title,
                "granule_id": granule.get("id"),
                "title": granule.get("title"),
                "time_start": granule.get("time_start"),
                "time_end": granule.get("time_end"),
                "size_mb": granule.get("granule_size"),
                "producer_granule_id": granule.get("producer_granule_id"),
                "data_links": data_links,
                "browse_links": browse_links,
            })

    out = args.out or f"data/raw/nasa_sentinel5p/sulawesi_tropomi_{args.keyword.lower()}_{args.year}_granules.csv"
    write_csv(Path(out), rows)
    print(f"Rows written: {len(rows)} -> {out}")
    if not rows:
        print("No matching granules found. Try keyword: NO2, SO2, CO, AER_AI, aerosol, or OMI as fallback.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
