import ee
import pandas as pd
import os

# Koordinat Bounding Box Sulawesi
MIN_LON, MIN_LAT, MAX_LON, MAX_LAT = 118.0, -6.5, 126.0, 2.5

def init_gee():
    print("Mencoba inisialisasi Google Earth Engine...")
    try:
        ee.Initialize()
        print("Inisialisasi berhasil!")
    except Exception as e:
        print("Belum terautentikasi. Membuka URL untuk login...")
        # Menggunakan mode notebook agar Google tidak memblokir aplikasi lokal
        ee.Authenticate(auth_mode='notebook')
        ee.Initialize()
        print("Autentikasi dan Inisialisasi berhasil!")

def get_annual_no2():
    init_gee()
    
    region = ee.Geometry.BBox(MIN_LON, MIN_LAT, MAX_LON, MAX_LAT)
    
    # Dataset Sentinel-5P NO2 dari satelit TROPOMI (Offline/High Quality)
    collection = ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_NO2") \
                   .select('tropospheric_NO2_column_number_density')
                   
    years = list(range(2018, 2025))
    results = []
    
    print("\nMeminta komputasi rata-rata bulanan dari server Google (untuk keperluan audit raw data)...")
    import calendar
    for year in years:
        for month in range(1, 13):
            # Skip bulan sebelum Juli 2018 (karena TROPOMI baru mulai beroperasi pertengahan 2018)
            if year == 2018 and month < 7:
                continue
                
            _, last_day = calendar.monthrange(year, month)
            start_date = f'{year}-{month:02d}-01'
            end_date = f'{year}-{month:02d}-{last_day}'
            
            # Filter koleksi berdasarkan bulan
            monthly_col = collection.filterDate(start_date, end_date)
            
            # Cek apakah ada data di bulan tersebut
            count = monthly_col.size().getInfo()
            if count == 0:
                print(f"{year}-{month:02d}: Tidak ada data satelit")
                continue
                
            monthly_mean_img = monthly_col.mean()
            
            # Kurangi citra menjadi 1 angka rata-rata untuk kotak wilayah Sulawesi
            stats = monthly_mean_img.reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=region,
                scale=5000, 
                maxPixels=1e9
            )
            
            try:
                val = stats.get('tropospheric_NO2_column_number_density').getInfo()
                if val is not None:
                    results.append({'Tahun': year, 'Bulan': month, 'Tanggal': f'{year}-{month:02d}-01', 'Rata_Rata_NO2': val})
                    print(f"{year}-{month:02d}: {val} mol/m^2")
                else:
                    print(f"{year}-{month:02d}: Data null")
            except Exception as e:
                print(f"Error pada {year}-{month:02d}: {e}")
            
    df = pd.DataFrame(results)
    
    # Simpan CSV
    out_dir = "data/processed"
    os.makedirs(out_dir, exist_ok=True)
    output_path = os.path.join(out_dir, "gee_nasa_no2_sulawesi_monthly_raw.csv")
    df.to_csv(output_path, index=False)
    
    print(f"\nSelesai! Data agregat rata-rata tahunan tersimpan di: {output_path}")

if __name__ == "__main__":
    get_annual_no2()
