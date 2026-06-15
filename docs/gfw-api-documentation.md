# Global Forest Watch (GFW) Data API Documentation

**CELIOS ECC Intelligence System**
**Generated:** 14 Juni 2026 (via `tools/gfw/crawl_gfw_api.py`)
**Source:** https://data-api.globalforestwatch.org/openapi.json
**Spec Version:** OpenAPI 3.0.2

---

## Overview

The Global Forest Watch Data API provides programmatic access to the world's most comprehensive forest monitoring datasets. The API is built by the World Resources Institute (WRI) and includes data from Hansen et al. (2013, Science) — tree cover loss/gain at 30m resolution, deforestation alerts (GLAD/RADD), forest carbon emissions, fire hotspots, and 376+ total datasets.

### API Endpoints

| Environment | Base URL | Status |
|---|---|---|
| **Data API (v2)** | `https://data-api.globalforestwatch.org` | ✅ Active (51 paths, 376 datasets) |
| **Production API (v1)** | `https://production-api.globalforestwatch.org` | ✅ Active (requires geostore) |
| **Data Portal** | `https://data.globalforestwatch.org` | ✅ Active (landing page only) |
| **ReDoc UI** | `https://data-api.globalforestwatch.org/` | ✅ Active (interactive docs) |

### Tags (12 categories)

`Authentication`, `Dataset`, `Version`, `Assets`, `Query`, `Download`, `Geostore`, `Tasks`, `Analysis`, `Job`, `Health`, `Land`

---

## Authentication

The GFW Data API supports three authentication methods:

### 1. OAuth2 (Password Flow)

```http
POST /auth/token
Content-Type: application/x-www-form-urlencoded

grant_type=password&username=EMAIL&password=PASSWORD
```

**Token URL:** `/auth/token`
**Returns:** Access token for authenticated requests.

### 2. API Key (Header)

```http
GET /dataset/{dataset}/{version}/query/json
x-api-key: YOUR_API_KEY
```

### 3. API Key (Query Parameter)

```http
GET /dataset/{dataset}/{version}/query/json?x-api-key=YOUR_API_KEY
```

### API Key Management

| Method | Path | Description | Auth |
|---|---|---|---|
| **POST** | `/auth/sign-up` | Register new user (name, email) | None |
| **POST** | `/auth/token` | Get access token | None |
| **POST** | `/auth/apikey` | Create API key (valid 1 year) | OAuth2 |
| **GET** | `/auth/apikey/{api_key}` | Get API key details | OAuth2 |
| **DELETE** | `/auth/apikey/{api_key}` | Delete API key | OAuth2 |
| **GET** | `/auth/apikeys` | List all user's API keys | OAuth2 |
| **GET** | `/auth/apikey/{api_key}/validate` | Validate API key | OAuth2 |

**Creating an API Key:**
```http
POST /auth/apikey
Authorization: Bearer ACCESS_TOKEN
Content-Type: application/json

{
  "alias": "celios-research",
  "organization": "CELIOS ECC",
  "email": "research@celios.org",
  "domains": ["celios.org"]
}
```

**Note:** Most read-only endpoints (datasets, fields, metadata) do NOT require authentication. Authentication is required for:
- SQL queries (`/query/json`, `/query/csv`)
- Batch queries (`/query/batch`)
- Zonal analysis (`/analysis/zonal`)
- Creating/updating datasets and assets

---

## Datasets

### List All Datasets

```http
GET /datasets
```

**Parameters:**

| Field | Type | Description |
|---|---|---|
| `page[number]` | Integer | Page number (≥1) |
| `page[size]` | Integer | Page size (≥1, default 10) |

**Success 200:** Returns paginated list of datasets.
**Current total:** 376 datasets across 8 pages (at 50/page).

```json
{
  "data": [
    {
      "id": "umd_tree_cover_loss",
      "attributes": {
        "name": "UMD Tree Cover Loss",
        "description": "...",
        "latest": {"version": "v1.11"},
        "versions_count": 11
      }
    }
  ],
  "links": {"self": "...", "next": "...", "last": "..."},
  "meta": {"total_items": 376}
}
```

### Get Dataset Detail

```http
GET /dataset/{dataset}
```

**Path Parameters:**

| Field | Type | Description |
|---|---|---|
| `dataset` | String | Dataset ID (pattern: `^[a-z][a-z0-9_-]{2,}$`) |

**Success 200:** Returns dataset metadata, version list, and assets.

```json
{
  "data": {
    "id": "umd_tree_cover_loss",
    "attributes": {
      "name": "UMD Tree Cover Loss",
      "versions": [{"version": "v1.11", "is_latest": true}],
      "latest": {"version": "v1.11"}
    }
  }
}
```

### Create/Update/Delete Dataset (Admin)

| Method | Path | Description | Auth |
|---|---|---|---|
| **PUT** | `/dataset/{dataset}` | Create dataset | OAuth2 (MANAGER/ADMIN) |
| **PATCH** | `/dataset/{dataset}` | Update metadata/accessibility | OAuth2 |
| **DELETE** | `/dataset/{dataset}` | Delete dataset (owner/ADMIN) | OAuth2 |

---

## Version

### Get Version Metadata

```http
GET /dataset/{dataset}/{version}
```

**Path Parameters:**

| Field | Type | Description |
|---|---|---|
| `dataset` | String | Dataset ID |
| `version` | String | Version (e.g., `v1.11`, `latest`) |

**Success 200:** Returns version metadata and assets list.

### Version Detail Endpoints

| Method | Path | Description |
|---|---|---|
| **GET** | `/dataset/{dataset}/{version}/change_log` | Version change log |
| **GET** | `/dataset/{dataset}/{version}/creation_options` | Creation options |
| **GET** | `/dataset/{dataset}/{version}/extent` | Spatial extent (bounding box) |
| **GET** | `/dataset/{dataset}/{version}/stats` | Asset statistics |
| **GET** | `/dataset/{dataset}/{version}/fields` | **Fields/attributes** (vector) or tile sets (raster) |
| **GET** | `/dataset/{dataset}/{version}/metadata` | Metadata record |

### Get Fields (Most Important for CELIOS)

```http
GET /dataset/{dataset}/{version}/fields
```

Returns all available columns/attributes for a dataset.

**Example response for `umd_tree_cover_loss`:**
```json
{
  "data": [
    {"name": "umd_tree_cover_loss__year", "type": "integer", "description": "Year of tree cover loss"},
    {"name": "area__ha", "type": "number", "description": "Area in hectares"},
    {"name": "whrc_aboveground_co2_emissions__Mg", "type": "number"},
    {"name": "tsc_tree_cover_loss_drivers__type", "type": "string"},
    ...
  ]
}
```

**Field counts per key dataset (crawled 2026-06-14):**

| Dataset | Status | Fields |
|---|---|---|
| `umd_tree_cover_loss` | ✅ 200 | 223 |
| `umd_tree_cover_gain` | ✅ 200 | 223 |
| `umd_tree_cover_density_2000` | ✅ 200 | 223 |
| `umd_tree_cover_density_2010` | ✅ 200 | 223 |
| `tsc_tree_cover_loss_drivers` | ✅ 200 | 223 |
| `gfw_forest_carbon_gross_removals` | ✅ 200 | 223 |
| `gfw_forest_carbon_gross_emissions` | ✅ 200 | 223 |
| `nasa_viirs_fire_alerts` | ✅ 200 | 49 |
| `wdpa_protected_areas` | ✅ 200 | 42 |
| `idn_forest_area` | ✅ 200 | 22 |
| `gfw_land_rights` | ✅ 200 | 19 |
| `gfw_oil_palm` | ✅ 200 | 24 |
| `gfw_wood_fiber` | ✅ 200 | 24 |

### Version Management (Admin)

| Method | Path | Description | Auth |
|---|---|---|---|
| **PUT** | `/dataset/{dataset}/{version}` | Add new version | OAuth2 |
| **PATCH** | `/dataset/{dataset}/{version}` | Update version metadata | OAuth2 |
| **DELETE** | `/dataset/{dataset}/{version}` | Delete version | OAuth2 |
| **POST** | `/dataset/{dataset}/{version}/append` | Append data to table | OAuth2 |

### Metadata Management

| Method | Path | Description | Auth |
|---|---|---|---|
| **POST** | `/dataset/{dataset}/{version}/metadata` | Create metadata | OAuth2 |
| **PATCH** | `/dataset/{dataset}/{version}/metadata` | Update metadata | OAuth2 |
| **DELETE** | `/dataset/{dataset}/{version}/metadata` | Delete metadata | OAuth2 |

### Spatial Features

```http
GET /dataset/{dataset}/{version}/features?lat=-5.1477&lng=119.4327&z=10
```

Returns features at a specific lat/lng/zoom location.

**Special endpoint for fire alerts:**
```http
GET /dataset/nasa_viirs_fire_alerts/{version}/features?lat=-5.1477&lng=119.4327&z=10&start_date=2024-01-01&end_date=2024-12-31
```

---

## Query (SQL) ⭐ MOST IMPORTANT FOR CELIOS

The Query endpoints allow you to run SQL-like queries against datasets and get results in JSON or CSV format.

### Query JSON

```http
GET /dataset/{dataset}/{version}/query/json
```

**Parameters:**

| Field | Type | Required | Description |
|---|---|---|---|
| `sql` | String | ✅ | SQL query string |
| `geostore_id` | UUID | ❌ | Geostore ID to filter by boundary |
| `geostore_origin` | Enum | ❌ | `gfw` (default) or `rw` |

**Example — Tree cover loss in Sulawesi Selatan 2016-2023:**
```
GET /dataset/umd_tree_cover_loss/latest/query/json?sql=SELECT umd_tree_cover_loss__year, SUM(area__ha) as total_loss_ha FROM data WHERE umd_tree_cover_loss__year >= 2016 GROUP BY umd_tree_cover_loss__year ORDER BY umd_tree_cover_loss__year
```

**Response:**
```json
{
  "data": [
    {"umd_tree_cover_loss__year": 2016, "total_loss_ha": 12345.67},
    {"umd_tree_cover_loss__year": 2017, "total_loss_ha": 15432.10},
    ...
  ],
  "status": "success"
}
```

### Query CSV

```http
GET /dataset/{dataset}/{version}/query/csv
```

Same parameters as JSON, plus:

| Field | Type | Description |
|---|---|---|
| `delimiter` | Enum | `,` (default), `\t`, `\|`, `;` |

**Response:** CSV file download.

### POST Variants (for complex queries)

```http
POST /dataset/{dataset}/{version}/query/json
Content-Type: application/json

{
  "sql": "SELECT * FROM data WHERE umd_tree_cover_loss__year = 2020",
  "geostore_id": "UUID"
}
```

### Batch Query (for large feature lists)

```http
POST /dataset/{dataset}/{version}/query/batch
x-api-key: YOUR_API_KEY
Content-Type: application/json

{
  "features": [
    {"geostore_id": "UUID1"},
    {"geostore_id": "UUID2"}
  ]
}
```

**Returns:** Job ID for async processing. Check status via `/job/{job_id}`.

**Auth:** API Key required.

---

## Download

Download query results or raw data in various formats.

### Download Query Results

| Method | Path | Format |
|---|---|---|
| **GET/POST** | `/dataset/{dataset}/{version}/download/json` | JSON |
| **GET/POST** | `/dataset/{dataset}/{version}/download/csv` | CSV |

**Parameters (same as Query):**
- `sql` (required): SQL query string
- `geostore_id` (optional): UUID boundary filter
- `filename` (optional): Custom filename (default: `export.json` or `export.csv`)
- `delimiter` (optional for CSV): `,`, `\t`, `|`, `;`

**Example:**
```
GET /dataset/umd_tree_cover_loss/latest/download/csv?sql=SELECT * FROM data WHERE umd_tree_cover_loss__year = 2023&filename=sulawesi_2023.csv
```

### Download by AOI (Area of Interest)

```http
GET /dataset/{dataset}/{version}/download_by_aoi/json
GET /dataset/{dataset}/{version}/download_by_aoi/csv
```

**Additional parameter:**

| Field | Type | Description |
|---|---|---|
| `aoi` | Object (required) | Area definition (see AOI Types below) |

**AOI Types:**

```json
// Admin boundary
{"type": "admin", "country": "IDN", "region": "30"}

// Geostore UUID
{"type": "geostore", "id": "UUID"}

// Global extent
{"type": "global"}

// Protected area (WDPA ID)
{"type": "protected_area", "id": "12345"}
```

**Example — Download Sulawesi Selatan tree cover loss:**
```
GET /dataset/umd_tree_cover_loss/latest/download_by_aoi/csv?sql=SELECT umd_tree_cover_loss__year, SUM(area__ha) FROM data GROUP BY umd_tree_cover_loss__year&aoi={"type":"admin","country":"IDN","region":"30"}
```

### Download Raster/Spatial Data

| Method | Path | Format |
|---|---|---|
| **GET** | `/dataset/{dataset}/{version}/download/geotiff` | GeoTIFF (raster tile) |
| **GET** | `/dataset/{dataset}/{version}/download/shp` | ESRI Shapefile (307 redirect) |
| **GET** | `/dataset/{dataset}/{version}/download/gpkg` | GeoPackage (307 redirect) |

**GeoTIFF Parameters:**

| Field | Type | Description |
|---|---|---|
| `grid` | Enum (required) | Grid size: `1/4000`, `3/33600`, `10/40000`, `zoom_0`–`zoom_22`, etc. |
| `tile_id` | String (required) | Tile identifier |
| `pixel_meaning` | String (required) | Which raster layer to download |

---

## Geostore

Geostores define geographic boundaries used to filter analysis. Required for most production API calls.

### Create Geostore

```http
POST /geostore/
Content-Type: application/json

{
  "type": "Feature",
  "geometry": {
    "type": "Polygon",
    "coordinates": [[[119.4, -5.1], [120.0, -5.1], [120.0, -4.5], [119.4, -4.5], [119.4, -5.1]]]
  }
}
```

**Success 200:** Returns geostore with UUID.

### Get Geostore

```http
GET /geostore/{geostore_id}
```

**Returns:** GeoJSON geometry of the boundary.

**Note:** If UUID exists in GFW's database, returns directly. Otherwise, delegates to RW API.

### Get Geostore by Dataset Version

```http
GET /dataset/{dataset}/{version}/geostore/{geostore_id}
```

Returns GeoJSON for a specific dataset's geostore boundary.

---

## Assets

Assets represent the actual data files (GeoJSON, CSV, GeoTIFF, Shapefile, etc.) attached to dataset versions.

### List Assets

```http
GET /dataset/{dataset}/{version}/assets
GET /assets  (global, with filters)
```

**Parameters:**

| Field | Type | Description |
|---|---|---|
| `asset_type` | String | Filter by type (see Asset Types below) |
| `asset_uri` | String | Filter by URI |
| `is_latest` | Boolean | Filter by latest |
| `is_default` | Boolean | Filter by default |
| `page[number]` | Integer | Page number |
| `page[size]` | Integer | Page size |

### Asset Types

| Type | Description |
|---|---|
| `Dynamic vector tile cache` | Dynamic vector tiles |
| `Static vector tile cache` | Pre-generated vector tiles |
| `Raster tile cache` | Raster tiles for visualization |
| `Raster tile set` | Full raster dataset |
| `Database table` | Tabular data in database |
| `Geo database table` | Geospatial table |
| `ESRI Shapefile` | Shapefile export |
| `Geopackage` | GeoPackage export |
| `ndjson` | Newline-delimited JSON |
| `csv` | CSV export |
| `tsv` | TSV export |
| `1x1 grid` | 1x1 degree grid |
| `COG` | Cloud Optimized GeoTIFF |

### Asset Detail Endpoints

| Method | Path | Description |
|---|---|---|
| **GET** | `/asset/{asset_id}` | Get asset |
| **GET** | `/asset/{asset_id}/tasks` | List tasks |
| **GET** | `/asset/{asset_id}/change_log` | Change log |
| **GET** | `/asset/{asset_id}/extent` | Spatial extent |
| **GET** | `/asset/{asset_id}/tiles_info` | Tile info (redirect) |
| **GET** | `/asset/{asset_id}/stats` | Statistics |
| **GET** | `/asset/{asset_id}/fields` | Field definitions |
| **GET** | `/asset/{asset_id}/fields/{field_name}` | Field metadata |
| **GET** | `/asset/{asset_id}/metadata` | Asset metadata |

### Asset Management (Admin)

| Method | Path | Auth |
|---|---|---|
| **POST** | `/dataset/{dataset}/{version}/assets` | OAuth2 |
| **PATCH** | `/asset/{asset_id}` | OAuth2 |
| **DELETE** | `/asset/{asset_id}` | OAuth2 |
| **PATCH** | `/asset/{asset_id}/fields/{field_name}` | OAuth2 |
| **POST** | `/asset/{asset_id}/metadata` | None |
| **PATCH** | `/asset/{asset_id}/metadata` | OAuth2 |
| **DELETE** | `/asset/{asset_id}/metadata` | OAuth2 |

---

## Analysis

### Zonal Statistics ⭐

Calculate statistics on raster layers within geographic boundaries.

```http
GET /analysis/zonal/{geostore_id}
```

**Parameters:**

| Field | Type | Required | Description |
|---|---|---|---|
| `geostore_id` | UUID | ✅ | Boundary to analyze |
| `geostore_origin` | Enum | ❌ | `gfw` (default) or `rw` |
| `sum` | Array | ✅ | Raster layers to sum (see below) |
| `group_by` | Array | ❌ | Group results by layer |
| `filters` | Array | ❌ | Filter by layer values |
| `start_date` | String | ❌ | Start date filter |
| `end_date` | String | ❌ | End date filter |

**Available Raster Layers for `sum` / `group_by` / `filters`:**

| Layer ID | Description |
|---|---|
| `area__ha` | Area in hectares |
| `alert__count` | Deforestation alert count |
| `whrc_aboveground_co2_emissions__Mg` | CO2 emissions (megagrams) |
| `umd_tree_cover_loss__year` | Year of tree cover loss |
| `is__umd_regional_primary_forest_2001` | Primary forest (2001) |
| `is__umd_tree_cover_gain` | Tree cover gain |
| `whrc_aboveground_biomass_stock_2000__Mg_ha-1` | Biomass stock (2000) |
| `tsc_tree_cover_loss_drivers__type` | Loss driver type |
| `gfw_plantations__type` | Plantation type |
| `wdpa_protected_areas__iucn_cat` | IUCN protected area category |
| `esa_land_cover_2015__class` | ESA land cover class |
| `umd_glad_alerts__isoweek` | GLAD alert ISO week |
| `umd_glad_alerts__date` | GLAD alert date |
| `umd_tree_cover_density_2000__10/15/20/25/30/50/75` | Tree cover density thresholds |
| `umd_tree_cover_density_2010__10/15/20/25/30/50/75` | Tree cover density (2010) |
| `ifl_intact_forest_landscapes__year` | Intact forest year |
| `is__gmw_mangroves_1996` / `is__gmw_mangroves_2016` | Mangrove extent |
| `is__birdlife_alliance_for_zero_extinction_sites` | AZE sites |
| `is__birdlife_key_biodiversity_areas` | KBAs |
| `is__gfw_tiger_landscapes` | Tiger landscapes |
| `is__gfw_mining` | Mining concessions |
| `is__gfw_peatlands` | Peatlands |
| `is__gfw_oil_palm` | Oil palm |
| `is__gfw_wood_fiber` | Wood fiber |
| `is__gfw_managed_forests` | Managed forests |
| `is__gfw_land_rights` | Land rights |
| `is__gfw_resource_rights` | Resource rights |
| `rspo_oil_palm__certification_status` | RSPO certification |
| `idn_forest_area__type` | Indonesia forest area type |
| `per_forest_concessions__type` | Peru forest concessions |
| `bra_biomes__name` | Brazil biomes |

**Example — Annual tree cover loss in Sulawesi Selatan:**
```
GET /analysis/zonal/GEO_STORE_ID?sum=area__ha&group_by=umd_tree_cover_loss__year&geostore_origin=gfw
```

**Response:**
```json
{
  "data": [
    {"umd_tree_cover_loss__year": 2016, "area__ha": 12345.67},
    {"umd_tree_cover_loss__year": 2017, "area__ha": 15432.10},
    ...
  ]
}
```

**Auth:** API Key required.

### POST Variant

```http
POST /analysis/zonal
Content-Type: application/json
x-api-key: YOUR_API_KEY

{
  "geostore_id": "UUID",
  "sum": ["area__ha"],
  "group_by": ["umd_tree_cover_loss__year"],
  "filters": [{"layer": "tsc_tree_cover_loss_drivers__type", "value": "Commodity driven deforestation"}]
}
```

---

## Tasks

Tasks track asynchronous operations (e.g., data processing, batch queries).

| Method | Path | Description | Auth |
|---|---|---|---|
| **GET** | `/task/{task_id}` | Get task status | None |
| **PUT** | `/task/{task_id}` | Create task (service accounts) | OAuth2 |
| **PATCH** | `/task/{task_id}` | Update task status | OAuth2 |

---

## Job

Jobs track long-running async operations (expire after 90 days).

| Method | Path | Description |
|---|---|---|
| **GET** | `/job/{job_id}` | Get job status |

---

## Health

| Method | Path | Description |
|---|---|---|
| **GET** | `/ping` | Simple uptime check (no auth) |

---

## Land (Beta) — Tree Cover Loss by Driver

Specialized endpoints for tree cover loss analysis by driver category.

### Search/Create Analysis

```http
GET /v0/land/tree_cover_loss_by_driver
```

**Parameters:**

| Field | Type | Required | Description |
|---|---|---|---|
| `canopy_cover` | Integer | ❌ | Canopy cover threshold (default 30) |
| `aoi` | Object | ✅ | Area of interest (see AOI Types) |
| `dataset_version` | Object | ❌ | Override dataset versions |

**AOI Object (one of):**

```json
// By geostore UUID
{"type": "geostore", "geostore_id": "UUID"}

// By admin boundary
{"type": "admin", "country": "IDN", "region": "30", "subregion": "123"}

// Global
{"type": "global"}

// Protected area
{"type": "protected_area", "wdpa_id": "12345"}
```

**Example — Tree cover loss by driver for Indonesia:**
```
GET /v0/land/tree_cover_loss_by_driver?canopy_cover=30&aoi={"type":"admin","country":"IDN"}
```

### Get/Delete Result

| Method | Path | Description |
|---|---|---|
| **GET** | `/v0/land/tree_cover_loss_by_driver/{resource_id}` | Get analysis result |
| **DELETE** | `/v0/land/tree_cover_loss_by_driver/{resource_id}` | Delete failed analysis |

### Create New Analysis

```http
POST /v0/land/tree_cover_loss_by_driver
Content-Type: application/json
x-api-key: YOUR_API_KEY

{
  "canopy_cover": 30,
  "aoi": {"type": "admin", "country": "IDN", "region": "30"}
}
```

---

## Production API (v1) — Legacy Endpoints

**Base URL:** `https://production-api.globalforestwatch.org`

⚠️ **Important:** The production API (v1) requires a **geostore ID** for most endpoints. The workflow is:

1. Create or get a geostore: `POST /geostore/` or find existing UUID
2. Use geostore ID in API calls

### Endpoints

| Endpoint | Path | Status |
|---|---|---|
| UMD Loss/Gain | `/v1/umd-loss-gain` | ✅ Active (requires geostore) |
| GLAD Alerts | `/v1/glad-alerts` | ✅ Active (requires geostore) |
| Forest Change by Admin | `/v1/forest-change/umd-loss-gain/admin` | ⚠️ 403 (may need API key) |
| VIIRS Active Fires | `/v1/viirs-active-fires` | ✅ Active (requires geostore) |

### UMD Loss/Gain

```http
GET /v1/umd-loss-gain
```

**Parameters:**

| Field | Type | Required | Description |
|---|---|---|---|
| `geostore` | UUID | ✅ | Geostore ID |
| `thresh` | Integer | ❌ | Tree cover threshold (default 30) |
| `period` | String | ❌ | Date range: `YYYY-MM-DD,YYYY-MM-DD` |

**Example:**
```
GET /v1/umd-loss-gain?geostore=UUID&thresh=30&period=2016-01-01,2023-12-31
```

### GLAD Alerts

```http
GET /v1/glad-alerts
```

**Parameters:**

| Field | Type | Required | Description |
|---|---|---|---|
| `geostore` | UUID | ✅ | Geostore ID (or `geojson` body) |
| `dateRange` | String | ❌ | `YYYY-MM-DD,YYYY-MM-DD` |
| `period` | String | ❌ | Alert period |

### VIIRS Active Fires

```http
GET /v1/viirs-active-fires
```

**Parameters:**

| Field | Type | Required | Description |
|---|---|---|---|
| `geostore` | UUID | ✅ | Geostore ID |
| `dateRange` | String | ❌ | `YYYY-MM-DD,YYYY-MM-DD` |
| `alert_type` | String | ❌ | `alerts` or `active_fires` |

---

## Key Datasets for CELIOS D3TLH Research

### Priority Datasets (Sulawesi Deforestation 2016-2024)

| Dataset ID | Description | Resolution | Coverage |
|---|---|---|---|
| `umd_tree_cover_loss` | Annual tree cover loss (Hansen) | 30m | 2001-2023 |
| `umd_tree_cover_gain` | Tree cover gain (2000-2020) | 30m | 2000-2020 |
| `umd_tree_cover_density_2000` | Baseline tree cover density | 30m | 2000 |
| `umd_tree_cover_density_2010` | Tree cover density | 30m | 2010 |
| `tsc_tree_cover_loss_drivers` | Deforestation drivers (commodity, forestry, etc.) | 30m | 2001-2023 |
| `gfw_forest_carbon_gross_emissions` | Forest carbon emissions | 30m | 2001-2023 |
| `gfw_forest_carbon_gross_removals` | Forest carbon removals | 30m | 2001-2020 |
| `nasa_viirs_fire_alerts` | NASA VIIRS fire hotspots | Point data | 2012-present |
| `wdpa_protected_areas` | World Database of Protected Areas | Vector | Global |
| `idn_forest_area` | Indonesia forest area classification | 30m | Indonesia |
| `gfw_mining` | Mining concessions | Vector | Selected countries |
| `gfw_oil_palm` | Oil palm plantations | Vector | Selected countries |
| `gfw_wood_fiber` | Wood fiber plantations | Vector | Selected countries |
| `gfw_land_rights` | Land rights / community lands | Vector | Selected countries |

### Sulawesi Admin Codes (for API filtering)

| Province | ISO 3166-2 | Admin1 Code | BPS Code |
|---|---|---|---|
| Sulawesi Utara | ID-ND | `IDN.31` / `31` | 71 |
| Sulawesi Tengah | ID-CT | `IDN.29` / `29` | 72 |
| Sulawesi Selatan | ID-SN | `IDN.30` / `30` | 73 |
| Sulawesi Tenggara | ID-SG | `IDN.32` / `32` | 74 |
| Gorontalo | ID-GT | `IDN.11` / `11` | 75 |
| Sulawesi Barat | ID-SR | `IDN.33` / `33` | 76 |

---

## Usage Examples

### 1. Get Annual Tree Cover Loss for Sulawesi Selatan

```python
import requests

BASE = "https://data-api.globalforestwatch.org"
API_KEY = "your-api-key"

# Query tree cover loss by year
sql = """
SELECT umd_tree_cover_loss__year, SUM(area__ha) as total_loss_ha
FROM data
WHERE umd_tree_cover_loss__year >= 2016
GROUP BY umd_tree_cover_loss__year
ORDER BY umd_tree_cover_loss__year
"""

resp = requests.get(
    f"{BASE}/dataset/umd_tree_cover_loss/latest/query/json",
    params={"sql": sql},
    headers={"x-api-key": API_KEY}
)
data = resp.json()
print(data["data"])
```

### 2. Download Tree Cover Loss by Driver (CSV)

```python
resp = requests.get(
    f"{BASE}/dataset/tsc_tree_cover_loss_drivers/latest/download_by_aoi/csv",
    params={
        "sql": "SELECT tsc_tree_cover_loss_drivers__type, SUM(area__ha) FROM data GROUP BY tsc_tree_cover_loss_drivers__type",
        "aoi": '{"type":"admin","country":"IDN","region":"30"}',
        "filename": "sulsel_loss_drivers.csv"
    },
    headers={"x-api-key": API_KEY}
)

with open("sulsel_loss_drivers.csv", "wb") as f:
    f.write(resp.content)
```

### 3. Zonal Analysis for Custom Boundary

```python
# Step 1: Create geostore for Sulawesi mining concession
geostore = requests.post(
    f"{BASE}/geostore/",
    json={
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": [[[122.0, -2.5], [123.0, -2.5], [123.0, -2.0], [122.0, -2.0], [122.0, -2.5]]]
        }
    }
)
geostore_id = geostore.json()["data"]["id"]

# Step 2: Run zonal analysis
resp = requests.get(
    f"{BASE}/analysis/zonal/{geostore_id}",
    params={
        "sum": ["area__ha", "whrc_aboveground_co2_emissions__Mg"],
        "group_by": ["umd_tree_cover_loss__year"]
    },
    headers={"x-api-key": API_KEY}
)
print(resp.json())
```

### 4. Get Fire Hotspots Near Mining Concessions

```python
resp = requests.get(
    f"{BASE}/dataset/nasa_viirs_fire_alerts/latest/features",
    params={
        "lat": -2.6,  # Morowali area
        "lng": 121.9,
        "z": 10,
        "start_date": "2024-01-01",
        "end_date": "2024-12-31"
    }
)
fires = resp.json()
print(f"Found {len(fires['data'])} fire alerts")
```

### 5. Python SDK (gfwpy)

```python
pip install gfwpy

from gfwpy.api import GFWAPI

api = GFWAPI()
result = api.analysis.zonal(
    geostore_id="UUID",
    sum=["area__ha"],
    group_by=["umd_tree_cover_loss__year"]
)
```

---

## Rate Limits & Best Practices

| Recommendation | Detail |
|---|---|
| **Rate limit** | ~1 request/second for public endpoints |
| **API key** | Register at data-api.globalforestwatch.org for higher limits |
| **Pagination** | Use `page[number]` and `page[size]` for large dataset lists |
| **Batch queries** | Use `/query/batch` for >100 features (returns job_id) |
| **Geostore reuse** | Create geostore once, reuse UUID for multiple analyses |
| **SQL queries** | Use `GROUP BY` and aggregation for efficient results |
| **Download format** | CSV for tabular data, JSON for structured, GeoTIFF for raster |

---

## Complete Endpoint Reference (51 paths)

| # | Method | Path | Tag | Auth |
|---|---|---|---|---|
| 1 | POST | `/auth/sign-up` | Authentication | None |
| 2 | POST | `/auth/token` | Authentication | None |
| 3 | POST | `/auth/apikey` | Authentication | OAuth2 |
| 4 | GET | `/auth/apikey/{api_key}` | Authentication | OAuth2 |
| 5 | DELETE | `/auth/apikey/{api_key}` | Authentication | OAuth2 |
| 6 | GET | `/auth/apikeys` | Authentication | OAuth2 |
| 7 | GET | `/auth/apikey/{api_key}/validate` | Authentication | OAuth2 |
| 8 | GET | `/datasets` | Dataset | None |
| 9 | GET | `/dataset/{dataset}` | Dataset | None |
| 10 | PUT | `/dataset/{dataset}` | Dataset | OAuth2 |
| 11 | DELETE | `/dataset/{dataset}` | Dataset | OAuth2 |
| 12 | PATCH | `/dataset/{dataset}` | Dataset | OAuth2 |
| 13 | GET | `/dataset/{dataset}/{version}` | Version | None |
| 14 | PUT | `/dataset/{dataset}/{version}` | Version | OAuth2 |
| 15 | DELETE | `/dataset/{dataset}/{version}` | Version | OAuth2 |
| 16 | PATCH | `/dataset/{dataset}/{version}` | Version | OAuth2 |
| 17 | POST | `/dataset/{dataset}/{version}/append` | Version | OAuth2 |
| 18 | GET | `/dataset/{dataset}/{version}/change_log` | Version | None |
| 19 | GET | `/dataset/{dataset}/{version}/creation_options` | Version | None |
| 20 | GET | `/dataset/{dataset}/{version}/extent` | Version | None |
| 21 | GET | `/dataset/{dataset}/{version}/stats` | Version | None |
| 22 | GET | `/dataset/{dataset}/{version}/fields` | Version | None |
| 23 | GET | `/dataset/{dataset}/{version}/metadata` | Version | None |
| 24 | POST | `/dataset/{dataset}/{version}/metadata` | Version | OAuth2 |
| 25 | DELETE | `/dataset/{dataset}/{version}/metadata` | Version | OAuth2 |
| 26 | PATCH | `/dataset/{dataset}/{version}/metadata` | Version | OAuth2 |
| 27 | GET | `/dataset/nasa_viirs_fire_alerts/{version}/features` | Version | None |
| 28 | GET | `/dataset/{dataset}/{version}/features` | Version | None |
| 29 | GET | `/dataset/{dataset}/{version}/geostore/{geostore_id}` | Geostore | None |
| 30 | POST | `/geostore/` | Geostore | None |
| 31 | GET | `/geostore/{geostore_id}` | Geostore | None |
| 32 | GET | `/dataset/{dataset}/{version}/assets` | Assets | None |
| 33 | POST | `/dataset/{dataset}/{version}/assets` | Assets | OAuth2 |
| 34 | GET | `/assets` | Assets | None |
| 35 | GET | `/asset/{asset_id}` | Assets | None |
| 36 | DELETE | `/asset/{asset_id}` | Assets | OAuth2 |
| 37 | PATCH | `/asset/{asset_id}` | Assets | OAuth2 |
| 38 | GET | `/asset/{asset_id}/tasks` | Assets | None |
| 39 | GET | `/asset/{asset_id}/change_log` | Assets | None |
| 40 | GET | `/asset/{asset_id}/creation_options` | Assets | None |
| 41 | GET | `/asset/{asset_id}/extent` | Assets | None |
| 42 | GET | `/asset/{asset_id}/tiles_info` | Assets | None |
| 43 | GET | `/asset/{asset_id}/stats` | Assets | None |
| 44 | GET | `/asset/{asset_id}/fields` | Assets | None |
| 45 | GET | `/asset/{asset_id}/fields/{field_name}` | Assets | None |
| 46 | PATCH | `/asset/{asset_id}/fields/{field_name}` | Assets | OAuth2 |
| 47 | GET | `/asset/{asset_id}/metadata` | Assets | None |
| 48 | POST | `/asset/{asset_id}/metadata` | Assets | None |
| 49 | DELETE | `/asset/{asset_id}/metadata` | Assets | OAuth2 |
| 50 | PATCH | `/asset/{asset_id}/metadata` | Assets | OAuth2 |
| 51 | GET | `/dataset/{dataset}/{version}/query` | Query | None (deprecated) |
| 52 | POST | `/dataset/{dataset}/{version}/query` | Query | None (deprecated) |
| 53 | GET | `/dataset/{dataset}/{version}/query/json` | Query | API Key |
| 54 | POST | `/dataset/{dataset}/{version}/query/json` | Query | API Key |
| 55 | GET | `/dataset/{dataset}/{version}/query/csv` | Query | API Key |
| 56 | POST | `/dataset/{dataset}/{version}/query/csv` | Query | API Key |
| 57 | POST | `/dataset/{dataset}/{version}/query/batch` | Query | API Key |
| 58 | GET | `/dataset/{dataset}/{version}/download/json` | Download | None |
| 59 | POST | `/dataset/{dataset}/{version}/download/json` | Download | None |
| 60 | GET | `/dataset/{dataset}/{version}/download/csv` | Download | None |
| 61 | POST | `/dataset/{dataset}/{version}/download/csv` | Download | None |
| 62 | GET | `/dataset/{dataset}/{version}/download_by_aoi/csv` | Download | None |
| 63 | GET | `/dataset/{dataset}/{version}/download_by_aoi/json` | Download | None |
| 64 | GET | `/dataset/{dataset}/{version}/download/geotiff` | Download | None |
| 65 | GET | `/dataset/{dataset}/{version}/download/shp` | Download | None |
| 66 | GET | `/dataset/{dataset}/{version}/download/gpkg` | Download | None |
| 67 | GET | `/task/{task_id}` | Tasks | None |
| 68 | PUT | `/task/{task_id}` | Tasks | OAuth2 |
| 69 | PATCH | `/task/{task_id}` | Tasks | OAuth2 |
| 70 | GET | `/analysis/zonal/{geostore_id}` | Analysis | API Key |
| 71 | POST | `/analysis/zonal` | Analysis | API Key |
| 72 | GET | `/job/{job_id}` | Job | None |
| 73 | GET | `/ping` | Health | None |
| 74 | GET | `/v0/land/tree_cover_loss_by_driver` | Land (Beta) | API Key |
| 75 | POST | `/v0/land/tree_cover_loss_by_driver` | Land (Beta) | API Key |
| 76 | GET | `/v0/land/tree_cover_loss_by_driver/{resource_id}` | Land (Beta) | API Key |
| 77 | DELETE | `/v0/land/tree_cover_loss_by_driver/{resource_id}` | Land (Beta) | API Key |

---

## Crawl Results

All raw API responses are saved in `tools/gfw/crawl_results/`:

| File | Content |
|---|---|
| `openapi_spec.json` | Full OpenAPI 3.0.2 specification |
| `openapi_summary.json` | Paths, tags, and metadata summary |
| `datasets_list.json` | All 376 datasets with metadata |
| `key_datasets.json` | Detailed responses for 14 priority datasets |
| `production_api_results.json` | Production API (v1) test results |
| `sulawesi_provinces_test.json` | Sulawesi province data tests |
| `geostore_sample.json` | Sample geostore response |
| `crawl_report.md` | Crawl execution report |

---

*Documentation generated: 14 Juni 2026*
*Crawler script: `tools/gfw/crawl_gfw_api.py`*
*CELIOS ECC Intelligence System*
