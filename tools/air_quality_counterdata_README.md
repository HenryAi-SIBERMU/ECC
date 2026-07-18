# Air Quality Counter-Data Tools

Purpose: test data sources that can challenge or validate official IKU/IKA trends.

## OpenAQ

Tool: `tools/openaq/check_sulawesi_coverage.py`

Checks whether OpenAQ v3 has ground-monitor locations inside a Sulawesi bounding box.

Requires:

```powershell
$env:OPENAQ_API_KEY="your_key"
python "tools/openaq/check_sulawesi_coverage.py"
```

Default output:

`data/raw/openaq/sulawesi_locations.csv`

Interpretation:

- If zero rows: OpenAQ cannot be used as a Sulawesi ground-monitor counter-dataset.
- If rows exist: fetch sensor-level measurements next using the location/sensor IDs.

## NASA Sentinel-5P/TROPOMI

Tool: `tools/nasa_sentinel5p/search_sulawesi_tropomi.py`

Searches NASA CMR metadata for Sentinel-5P/TROPOMI collections and granules over Sulawesi.

Examples:

```powershell
python "tools/nasa_sentinel5p/search_sulawesi_tropomi.py" --keyword NO2 --year 2024
python "tools/nasa_sentinel5p/search_sulawesi_tropomi.py" --keyword SO2 --year 2024
python "tools/nasa_sentinel5p/search_sulawesi_tropomi.py" --keyword CO --year 2024
```

Default output:

`data/raw/nasa_sentinel5p/sulawesi_tropomi_<keyword>_<year>_granules.csv`

Notes:

- CMR metadata search is public.
- Downloading and processing NetCDF/HDF science files usually requires NASA Earthdata Login.
- If Sentinel-5P is sparse or hard to download, use OMI/OMSO2/OMNO2 or NASA FIRMS as fallback proxy.

### Download Earthdata Granules

Tool: `tools/nasa_sentinel5p/download_earthdata_granules.py`

Requires NASA Earthdata credentials:

```powershell
$env:EARTHDATA_USERNAME="your_username"
$env:EARTHDATA_PASSWORD="your_password"
python "tools/nasa_sentinel5p/download_earthdata_granules.py" --input "data/raw/nasa_sentinel5p/sulawesi_tropomi_no2_2024_granules.csv" --limit 1
```

Default output directory:

`data/raw/nasa_sentinel5p/granules/`

### Process Downloaded NetCDF to CSV

Tool: `tools/nasa_sentinel5p/process_tropomi_bbox.py`

Examples:

```powershell
python "tools/nasa_sentinel5p/process_tropomi_bbox.py" --product NO2
python "tools/nasa_sentinel5p/process_tropomi_bbox.py" --product SO2
python "tools/nasa_sentinel5p/process_tropomi_bbox.py" --product CO
```

Default output:

`data/processed/sulawesi_tropomi_<product>_bbox_aggregates.csv`
