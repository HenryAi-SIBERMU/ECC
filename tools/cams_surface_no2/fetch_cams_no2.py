import ee
import argparse

# Initialize Earth Engine
try:
    ee.Initialize()
except Exception as e:
    print("Please authenticate to Earth Engine first using 'earthengine authenticate'")
    exit(1)

def get_tropomi_surface_no2_estimate(lat, lon, date_start, date_end, pblh_m):
    """
    Fetches TROPOMI Column NO2 and estimates surface concentration in ug/m3.
    """
    # Sentinel-5P TROPOMI NO2 Column Density (mol/m2)
    tropomi = ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_NO2") \
        .filterDate(date_start, date_end) \
        .select('tropospheric_NO2_column_number_density')
    
    mean_tropomi = tropomi.mean()
    
    # Get value at point (mol/m2)
    point = ee.Geometry.Point([lon, lat])
    
    try:
        value_mol = mean_tropomi.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=point,
            scale=1113.2 # TROPOMI resolution
        ).getInfo()
        
        if not value_mol or 'tropospheric_NO2_column_number_density' not in value_mol or value_mol['tropospheric_NO2_column_number_density'] is None:
            return None
            
        col_density = value_mol['tropospheric_NO2_column_number_density']
        
        # --- EMPIRICAL CONVERSION ---
        # ug/m3 = (Column Density / PBLH) * Molar Mass of NO2 in ug/mol
        # Molar Mass of NO2 = 46.0055 g/mol = 46,005,500 ug/mol
        molar_mass_ug = 46005500
        ugm3_estimate = (col_density / pblh_m) * molar_mass_ug
        
        return {
            'col_density_mol_m2': col_density,
            'surface_ugm3_estimate': ugm3_estimate
        }
        
    except Exception as e:
        print(f"Error extracting data: {e}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Estimate Surface NO2 in ug/m3 from TROPOMI")
    parser.add_argument('--lat', type=float, default=-2.82, help="Latitude (default: Morowali -2.82)")
    parser.add_argument('--lon', type=float, default=122.15, help="Longitude (default: Morowali 122.15)")
    parser.add_argument('--start', type=str, default="2023-01-01", help="Start date YYYY-MM-DD")
    parser.add_argument('--end', type=str, default="2023-12-31", help="End date YYYY-MM-DD")
    parser.add_argument('--pblh', type=float, default=1000.0, help="Assumed Planetary Boundary Layer Height in meters (default: 1000)")
    
    args = parser.parse_args()
    
    print(f"Fetching TROPOMI NO2 for coordinates: {args.lat}, {args.lon}...")
    result = get_tropomi_surface_no2_estimate(args.lat, args.lon, args.start, args.end, args.pblh)
    
    print("-" * 50)
    if result:
        print(f"1. Raw Column Density (TROPOMI) : {result['col_density_mol_m2']:.8f} mol/m2")
        print(f"2. Assumed PBL Height           : {args.pblh} meters")
        print(f"3. Estimated Surface NO2        : {result['surface_ugm3_estimate']:.2f} ug/m3")
        print("-" * 50)
        print("WARNING: This is a rough empirical physics estimation.")
        print("Baku Mutu Nasional PP 22/2021 untuk NO2 adalah 65 ug/m3 (24 Jam) / 50 ug/m3 (1 Tahun).")
        
        # Save to CSV
        import csv
        import os
        
        # Ensure directory exists
        save_dir = 'data/raw/tropomi_ugm3_estimasi'
        os.makedirs(save_dir, exist_ok=True)
        csv_path = os.path.join(save_dir, 'tropomi_ugm3_estimasi.csv')
        
        file_exists = os.path.isfile(csv_path)
        with open(csv_path, mode='a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['Latitude', 'Longitude', 'Start_Date', 'End_Date', 'PBLH_m', 'Col_Density_mol_m2', 'Estimated_ug_m3'])
            writer.writerow([args.lat, args.lon, args.start, args.end, args.pblh, result['col_density_mol_m2'], round(result['surface_ugm3_estimate'], 4)])
            
        print(f"Dataset berhasil disimpan ke: {csv_path}")
        
    else:
        print("No data found for this location/period.")
    print("-" * 50)
