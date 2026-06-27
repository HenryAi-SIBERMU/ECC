import urllib.request
import json
import csv
import os
import time

def point_in_polygon(x, y, polygon):
    """
    Ray-casting algorithm to determine if a point is inside a polygon.
    Polygon is a list of [x, y] coordinates.
    """
    n = len(polygon)
    inside = False
    p1x, p1y = polygon[0]
    for i in range(1, n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xints = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

def get_province(lon, lat, geojson_data):
    """
    Mencari provinsi dari titik koordinat (lon, lat) menggunakan data GeoJSON.
    Mendukung tipe Polygon dan MultiPolygon.
    """
    for feature in geojson_data['features']:
        prop = feature['properties']
        geom = feature['geometry']
        if not geom:
            continue
            
        prov_name = prop.get('Propinsi', prop.get('state', prop.get('name', 'Unknown')))
        
        if isinstance(prov_name, str):
            prov_name = prov_name.title()
        
        if geom['type'] == 'Polygon':
            polygons = [geom['coordinates'][0]]
        elif geom['type'] == 'MultiPolygon':
            polygons = [poly[0] for poly in geom['coordinates']]
        else:
            continue
            
        for poly in polygons:
            if point_in_polygon(lon, lat, poly):
                return prov_name
    return "Unknown"

def main():
    print("Memuat data GeoJSON batas provinsi Indonesia...")
    geojson_path = '../../data/raw/indonesia-prov.geojson'
    
    with open(geojson_path, 'r', encoding='utf-8') as f:
        geojson_data = json.load(f)

    species_list = [
        "Babyrousa celebensis",
        "Babyrousa babyrussa",
        "Bubalus depressicornis",
        "Bubalus quarlesi",
        "Macaca nigra",
        "Macrocephalon maleo",
        "Tarsius tarsier"
    ]

    occurrences = []
    
    print("Memulai penarikan data dari GBIF API (Global Biodiversity Information Facility)...")
    for species in species_list:
        print(f"Menarik data koordinat (occurrence) untuk {species}...")
        
        # GBIF API search: country=ID (Indonesia), hasCoordinate=true
        encoded_species = urllib.parse.quote(species)
        url = f"https://api.gbif.org/v1/occurrence/search?scientificName={encoded_species}&country=ID&hasCoordinate=true&limit=100"
        
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                
                results = data.get('results', [])
                if not results:
                    print(f"  -> Tidak ada data spasial ditemukan untuk {species}.")
                    continue
                
                print(f"  -> Ditemukan {len(results)} titik observasi. Memetakan ke provinsi...")
                
                for res in results:
                    lat = res.get('decimalLatitude')
                    lon = res.get('decimalLongitude')
                    
                    if lat is not None and lon is not None:
                        prov = get_province(lon, lat, geojson_data)
                        
                        # Filter out if it maps to 'Unknown' or outside Sulawesi 
                        # (This ensures data integrity for Sulawesi analysis)
                        if "Sulawesi" in prov or prov == "Gorontalo":
                            occurrences.append({
                                'Scientific_Name': species,
                                'Latitude': lat,
                                'Longitude': lon,
                                'Province': prov,
                                'Year': res.get('year', 'Unknown'),
                                'Source': 'GBIF'
                            })
        except Exception as e:
            print(f"  -> Error mengambil data {species}: {e}")
            
        time.sleep(1) # Etika hit API
        
    print(f"\nSelesai! Total {len(occurrences)} titik observasi berhasil dipetakan ke wilayah Sulawesi.")
    
    # Save raw occurrences
    out_csv = '../../data/raw/gbif_sulawesi_occurrences.csv'
    with open(out_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['Scientific_Name', 'Latitude', 'Longitude', 'Province', 'Year', 'Source'])
        writer.writeheader()
        writer.writerows(occurrences)
        
    # Aggregate to update IUCN dataset ethically
    print("\nMengagregasi data untuk dataset akhir IUCN...")
    species_prov_map = {}
    for occ in occurrences:
        sp = occ['Scientific_Name']
        pr = occ['Province']
        if sp not in species_prov_map:
            species_prov_map[sp] = set()
        species_prov_map[sp].add(pr)
        
    # Load base IUCN (the initial one without location)
    # Wait, we can just regenerate the final CSV right here
    # Base data from IUCN scrape (previously established):
    iucn_base = {
        "Babyrousa celebensis": {"Common Name": "Sulawesi Babirusa", "Status": "Vulnerable", "Trend": "Decreasing", "Mining": "Yes"},
        "Babyrousa babyrussa": {"Common Name": "Hairy Babirusa", "Status": "Vulnerable", "Trend": "Decreasing", "Mining": "No"},
        "Bubalus depressicornis": {"Common Name": "Lowland Anoa", "Status": "Endangered", "Trend": "Decreasing", "Mining": "Yes"},
        "Bubalus quarlesi": {"Common Name": "Mountain Anoa", "Status": "Endangered", "Trend": "Decreasing", "Mining": "Yes"},
        "Macaca nigra": {"Common Name": "Celebes Crested Macaque", "Status": "Critically Endangered", "Trend": "Decreasing", "Mining": "Yes"},
        "Macrocephalon maleo": {"Common Name": "Maleo", "Status": "Critically Endangered", "Trend": "Decreasing", "Mining": "No"},
        "Tarsius tarsier": {"Common Name": "Spectral Tarsier", "Status": "Vulnerable", "Trend": "Decreasing", "Mining": "No"}
    }
    
    final_rows = []
    for sp, data in iucn_base.items():
        provs = species_prov_map.get(sp, set())
        if not provs:
            # Jika tidak ada di GBIF untuk Sulawesi, tandai Unverified
            final_rows.append([sp, data["Common Name"], data["Status"], data["Trend"], data["Mining"], "Unverified via GBIF"])
        else:
            for p in sorted(list(provs)):
                final_rows.append([sp, data["Common Name"], data["Status"], data["Trend"], data["Mining"], p])
                
    final_csv_path = '../../data/processed/sulawesi_biodiversitas_iucn_fase5_exploded.csv'
    with open(final_csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Scientific Name', 'Common Name', 'Status', 'Population Trend', 'Mining Threat', 'Province'])
        writer.writerows(final_rows)
        
    print(f"Dataset akhir berintegritas tinggi berhasil disimpan ke: {final_csv_path}")

if __name__ == '__main__':
    main()
