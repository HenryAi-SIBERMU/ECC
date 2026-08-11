import ee
import pandas as pd
import os

def init_gee():
    print("Mencoba inisialisasi Google Earth Engine...")
    try:
        ee.Initialize()
        print("Inisialisasi berhasil!")
    except Exception as e:
        print("Belum terautentikasi. Membuka URL untuk login...")
        ee.Authenticate(auth_mode='notebook')
        ee.Initialize()
        print("Autentikasi dan Inisialisasi berhasil!")

def get_annual_no2_per_provinsi():
    init_gee()
    
    # Load GAUL Level 1 (Provinces) boundaries dari UN FAO
    provinces = ee.FeatureCollection("FAO/GAUL/2015/level1")
    sulawesi_provs = ["Sulawesi Tengah", "Sulawesi Tenggara", "Sulawesi Selatan", "Sulawesi Barat", "Gorontalo", "Sulawesi Utara"]
    
    # Filter FeatureCollection agar hanya berisi poligon 6 Provinsi di Sulawesi
    region = provinces.filter(ee.Filter.inList('ADM1_NAME', sulawesi_provs))
    
    # Dataset Sentinel-5P NO2
    collection = ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_NO2").select('tropospheric_NO2_column_number_density')
                   
    years = list(range(2018, 2025))
    results = []
    
    print("\nMeminta komputasi rata-rata spasial per-provinsi dari server superkomputer Google...")
    
    for year in years:
        start_date = f'{year}-01-01'
        if year == 2018:
            start_date = '2018-07-01'
            
        end_date = f'{year}-12-31'
        
        yearly_col = collection.filterDate(start_date, end_date)
        
        try:
            count = yearly_col.size().getInfo()
            if count == 0:
                print(f"{year}: Tidak ada data satelit")
                continue
                
            yearly_mean_img = yearly_col.mean()
            
            # Reduce Regions: hitung rata-rata pixel TROPOMI di DALAM batas tiap poligon provinsi
            stats = yearly_mean_img.reduceRegions(
                collection=region,
                reducer=ee.Reducer.mean(),
                scale=5000
            )
            
            # Ambil data dari server GEE ke lokal
            features = stats.getInfo()['features']
            for feat in features:
                props = feat['properties']
                prov_name = props.get('ADM1_NAME')
                val = props.get('mean')
                
                if val is not None:
                    results.append({'Provinsi': prov_name, 'Tahun': year, 'Rata_Rata_NO2': val})
                    print(f"✅ {prov_name} ({year}): {val:.7f} mol/m^2")
                else:
                    results.append({'Provinsi': prov_name, 'Tahun': year, 'Rata_Rata_NO2': 0})
                    print(f"⚠️ {prov_name} ({year}): Data null")
                    
        except Exception as e:
            print(f"Error pada {year}: {e}")
            
    # Konversi ke dataframe dan simpan
    df = pd.DataFrame(results)
    
    out_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed")
    os.makedirs(out_dir, exist_ok=True)
    output_path = os.path.abspath(os.path.join(out_dir, "gee_nasa_no2_sulawesi_provinsi.csv"))
    df.to_csv(output_path, index=False)
    
    print(f"\nSelesai! Data agregat rata-rata tahunan NO2 spesifik per-provinsi tersimpan di: {output_path}")

if __name__ == "__main__":
    get_annual_no2_per_provinsi()
