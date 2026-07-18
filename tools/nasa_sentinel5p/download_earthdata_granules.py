"""Download NASA Earthdata/GES DISC granules listed by CMR search CSV.

Requires NASA Earthdata Login credentials. Set either:
    EARTHDATA_USERNAME and EARTHDATA_PASSWORD

or create a .netrc entry for urs.earthdata.nasa.gov.

Example:
    set EARTHDATA_USERNAME=your_username
    set EARTHDATA_PASSWORD=your_password
    python tools/nasa_sentinel5p/download_earthdata_granules.py --input data/raw/nasa_sentinel5p/sulawesi_tropomi_no2_2024_granules.csv --limit 2
"""

from __future__ import annotations

import argparse
import csv
import netrc
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


def get_credentials() -> tuple[str | None, str | None]:
    username = os.getenv("EARTHDATA_USERNAME")
    password = os.getenv("EARTHDATA_PASSWORD")
    if username and password:
        return username, password
    try:
        auth = netrc.netrc().authenticators("urs.earthdata.nasa.gov")
    except Exception:
        return None, None
    if auth:
        return auth[0], auth[2]
    return None, None


class EarthdataRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Keep Authorization header across Earthdata redirects."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        new_req = super().redirect_request(req, fp, code, msg, headers, newurl)
        if new_req is not None and req.has_header("Authorization"):
            new_req.add_unredirected_header("Authorization", req.get_header("Authorization"))
        return new_req


def build_opener(username: str | None, password: str | None) -> urllib.request.OpenerDirector:
    password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    if username and password:
        password_mgr.add_password(None, "https://urs.earthdata.nasa.gov", username, password)
        password_mgr.add_password(None, "https://data.gesdisc.earthdata.nasa.gov", username, password)
    auth_handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
    cookie_handler = urllib.request.HTTPCookieProcessor()
    return urllib.request.build_opener(EarthdataRedirectHandler, auth_handler, cookie_handler)


def first_nc_link(data_links: str) -> str | None:
    for link in str(data_links).split(";"):
        link = link.strip()
        if link.startswith("https://") and link.endswith(".nc"):
            return link
    return None


import time

def download(url: str, output_path: Path, opener: urllib.request.OpenerDirector) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url)
    with opener.open(req, timeout=180) as response, output_path.open("wb") as f:
        total = int(response.headers.get("content-length") or 0)
        done = 0
        start_time = time.time()
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            f.write(chunk)
            done += len(chunk)
            if total:
                pct = done / total * 100
                elapsed = time.time() - start_time
                speed_mb_s = (done / (1024*1024)) / elapsed if elapsed > 0 else 0
                eta_s = (total - done) / (1024*1024) / speed_mb_s if speed_mb_s > 0 else 0
                eta_str = f"{int(eta_s//60)}m {int(eta_s%60)}s"
                print(f"  {output_path.name[:20]}... : {pct:5.1f}% | {speed_mb_s:.1f} MB/s | ETA: {eta_str}      ", end="\r")
        print(f"  {output_path.name}: downloaded {done / (1024 * 1024):.1f} MB")


def main() -> int:
    parser = argparse.ArgumentParser(description="Download Sentinel-5P/TROPOMI NetCDF granules from Earthdata.")
    parser.add_argument("--input", required=True, help="Granule CSV from search_sulawesi_tropomi.py")
    parser.add_argument("--out-dir", default="data/raw/nasa_sentinel5p/granules", help="Download directory.")
    parser.add_argument("--limit", type=int, default=0, help="Max files to download, 0 = all.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing files.")
    args = parser.parse_args()

    username, password = get_credentials()
    if not username or not password:
        print("ERROR: Set EARTHDATA_USERNAME and EARTHDATA_PASSWORD, or configure .netrc.", file=sys.stderr)
        return 2

    opener = build_opener(username, password)
    out_dir = Path(args.out_dir)
    count = 0
    with open(args.input, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            url = first_nc_link(row.get("data_links", ""))
            if not url:
                continue
            filename = Path(urllib.parse.urlparse(url).path).name
            output_path = out_dir / filename
            if output_path.exists() and not args.overwrite:
                print(f"SKIP existing: {output_path}")
                continue
            print(f"Downloading: {url}")
            try:
                download(url, output_path, opener)
            except urllib.error.HTTPError as exc:
                print(f"ERROR HTTP {exc.code}: {url}", file=sys.stderr)
                return 1
            count += 1
            if args.limit and count >= args.limit:
                break
    print(f"Downloaded files: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
