import ee
import json
import glob
import os
import csv
import argparse

# Initialize Earth Engine
try:
    ee.Initialize()
except Exception as e:
    print("Please authenticate to Earth Engine first using 'earthengine authenticate'")
    exit(1)

def process_geojson_grid(geojson_path, date_start, date_end, pblh_m, scale_m=10000):
    """
    Reads a GeoJSON, samples TROPOMI NO2 at a given grid scale (meters), 
    and returns a list of dictionaries with lat, lon, and values.
    """
    with open(geojson_path, 'r', encoding='utf-8') as f:
        geo_data = json.load(f)
    
    # Extract the first feature's geometry
    if 'features' in geo_data and len(geo_data['features']) > 0:
        geom_dict = geo_data['features'][0]['geometry']
    elif 'geometry' in geo_data:
        geom_dict = geo_data['geometry']
    else:
        geom_dict = geo_data # assume it's just a geometry
        
    region = ee.Geometry(geom_dict)
    
    # 1. Get TROPOMI Data
    tropomi = ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_NO2") \
        .filterDate(date_start, date_end) \
        .select('tropospheric_NO2_column_number_density')
    
    mean_tropomi = tropomi.mean().rename('Col_Density_mol_m2')
    
    # 2. Empirical Conversion to ug/m3
    molar_mass_ug = 46005500
    ugm3_image = mean_tropomi.divide(pblh_m).multiply(molar_mass_ug).rename('Estimated_ug_m3')
    
    # Combine bands
    combined_image = mean_tropomi.addBands(ugm3_image)
    
    # 3. Sample as a grid of points
    print(f"  Sampling points at {scale_m/1000} KM scale. This might take a minute...")
    samples = combined_image.sample(
        region=region,
        scale=scale_m,
        projection='EPSG:4326',
        geometries=True,
        dropNulls=True
    )
    
    # Fetch data to local Python environment
    features = samples.getInfo()['features']
    
    results = []
    for feat in features:
        lon, lat = feat['geometry']['coordinates']
        props = feat['properties']
        results.append({
            'Latitude': lat,
            'Longitude': lon,
            'Col_Density_mol_m2': props.get('Col_Density_mol_m2'),
            'Estimated_ug_m3': props.get('Estimated_ug_m3')
        })
        
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Grid Sampling of TROPOMI NO2")
    parser.add_argument('--start', type=str, default="2023-01-01", help="Start date YYYY-MM-DD")
    parser.add_argument('--end', type=str, default="2023-12-31", help="End date YYYY-MM-DD")
    parser.add_argument('--pblh', type=float, default=1000.0, help="Assumed PBL Height (m)")
    parser.add_argument('--scale', type=int, default=10000, help="Grid scale in meters (default 10km)")
    
    args = parser.parse_args()
    
    geojson_folder = r"data/raw/tropomi_ugm3_estimasi"
    os.makedirs(geojson_folder, exist_ok=True)
    out_csv = os.path.join(geojson_folder, "tropomi_grid_sulawesi.csv")
    
    search_path = "tools/gfw/geostore_validation_sulawesi/*_v3.geojson"
    geojson_files = glob.glob(search_path)
    
    if not geojson_files:
        print(f"No V3 GeoJSON files found in {search_path}")
        exit(1)
        
    all_data = []
    
    print(f"Found {len(geojson_files)} province GeoJSON files.")
    for gf in geojson_files:
        prov_name = os.path.basename(gf).replace('_v3.geojson', '').replace('GFW_', '')
        print(f"\nProcessing {prov_name}...")
        
        try:
            points = process_geojson_grid(gf, args.start, args.end, args.pblh, args.scale)
            print(f"  Extracted {len(points)} grid points for {prov_name}.")
            
            # Tag with province name and metadata
            for p in points:
                p['Province'] = prov_name
                p['Start_Date'] = args.start
                p['End_Date'] = args.end
                p['PBLH_m'] = args.pblh
                all_data.append(p)
                
        except Exception as e:
            print(f"  [ERROR] Failed processing {prov_name}: {e}")
            
    # Save to CSV
    if all_data:
        keys = ['Province', 'Latitude', 'Longitude', 'Start_Date', 'End_Date', 'PBLH_m', 'Col_Density_mol_m2', 'Estimated_ug_m3']
        with open(out_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(all_data)
        print(f"\nSUCCESS! Total {len(all_data)} points saved to {out_csv}")
    else:
        print("\nNo data extracted.")
