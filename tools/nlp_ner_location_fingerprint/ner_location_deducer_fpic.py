import pandas as pd
import argparse
import sys

def deduce_sulawesi_province(text: str, default_val: str = "Sulawesi (unspecified)") -> str:
    """
    Perform simple Named Entity Recognition (NER) / Keyword matching 
    to deduce the province in Sulawesi based on geographical footprints in the text.
    """
    text = str(text).lower()
    
    if 'konawe' in text or 'wawoni' in text or 'tinanggea' in text or 'baubau' in text or 'sulawesi tenggara' in text or 'sultra' in text or 'kolaka' in text or 'bombana' in text:
        return 'Sulawesi Tenggara'
    
    if 'minahasa' in text or 'sulawesi utara' in text or 'sulut' in text or 'manado' in text or 'bitung' in text or 'sangihe' in text or 'talaud' in text or 'kotamobagu' in text or 'bolaang' in text or 'sitaro' in text or 'bangka' in text:
        return 'Sulawesi Utara'
        
    if 'luwu timur' in text or 'luwu utara' in text or 'sulawesi selatan' in text or 'sulsel' in text or 'sorowako' in text or 'makassar' in text or 'gowa' in text or 'bone' in text:
        return 'Sulawesi Selatan'
        
    if 'morowali' in text or 'sulawesi tengah' in text or 'sulteng' in text or 'palu' in text or 'donggala' in text or 'poso' in text or 'banggai' in text:
        return 'Sulawesi Tengah'
        
    if 'gorontalo' in text or 'pohuwato' in text or 'bone bolango' in text:
        return 'Gorontalo'
        
    if 'sulawesi barat' in text or 'sulbar' in text or 'mamuju' in text or 'majene' in text or 'polewali' in text:
        return 'Sulawesi Barat'
        
    return default_val

# Mapping kabupaten/kota keyword -> nama resmi per provinsi
KABUPATEN_MAP = {
    # Sulawesi Tengah
    'morowali utara': 'Kab. Morowali Utara',
    'morowali': 'Kab. Morowali',
    'poso': 'Kab. Poso',
    'donggala': 'Kab. Donggala',
    'sigi': 'Kab. Sigi',
    'banggai kepulauan': 'Kab. Banggai Kepulauan',
    'banggai laut': 'Kab. Banggai Laut',
    'banggai': 'Kab. Banggai',
    'tojo una': 'Kab. Tojo Una-Una',
    'palu': 'Kota Palu',
    'parigi': 'Kab. Parigi Moutong',
    'buol': 'Kab. Buol',
    'tolitoli': 'Kab. Toli-Toli',
    'lore lindu': 'Kab. Sigi (TNLL)',
    # Sulawesi Tenggara
    'konawe selatan': 'Kab. Konawe Selatan',
    'konawe utara': 'Kab. Konawe Utara',
    'konawe': 'Kab. Konawe',
    'kolaka utara': 'Kab. Kolaka Utara',
    'kolaka timur': 'Kab. Kolaka Timur',
    'kolaka': 'Kab. Kolaka',
    'bombana': 'Kab. Bombana',
    'muna barat': 'Kab. Muna Barat',
    'muna': 'Kab. Muna',
    'buton utara': 'Kab. Buton Utara',
    'buton tengah': 'Kab. Buton Tengah',
    'buton selatan': 'Kab. Buton Selatan',
    'buton': 'Kab. Buton',
    'baubau': 'Kota Baubau',
    'kendari': 'Kota Kendari',
    'wawoni': 'Kab. Konawe Kepulauan (Wawoni)',
    'wakatobi': 'Kab. Wakatobi',
    'tinanggea': 'Kab. Konawe Selatan',
    # Sulawesi Selatan
    'luwu timur': 'Kab. Luwu Timur',
    'luwu utara': 'Kab. Luwu Utara',
    'luwu': 'Kab. Luwu',
    'sorowako': 'Kab. Luwu Timur (Sorowako)',
    'makassar': 'Kota Makassar',
    'gowa': 'Kab. Gowa',
    'bone': 'Kab. Bone',
    'sinjai': 'Kab. Sinjai',
    'bulukumba': 'Kab. Bulukumba',
    'bantaeng': 'Kab. Bantaeng',
    'selayar': 'Kab. Kepulauan Selayar',
    'jeneponto': 'Kab. Jeneponto',
    'takalar': 'Kab. Takalar',
    'maros': 'Kab. Maros',
    'pangkep': 'Kab. Pangkajene dan Kepulauan',
    'barru': 'Kab. Barru',
    'pare-pare': 'Kota Parepare',
    'parepare': 'Kota Parepare',
    'pinrang': 'Kab. Pinrang',
    'enrekang': 'Kab. Enrekang',
    'tana toraja': 'Kab. Tana Toraja',
    'toraja utara': 'Kab. Toraja Utara',
    'sidrap': 'Kab. Sidenreng Rappang',
    'wajo': 'Kab. Wajo',
    'soppeng': 'Kab. Soppeng',
    # Sulawesi Utara
    'minahasa utara': 'Kab. Minahasa Utara',
    'minahasa selatan': 'Kab. Minahasa Selatan',
    'minahasa tenggara': 'Kab. Minahasa Tenggara',
    'minahasa': 'Kab. Minahasa',
    'manado': 'Kota Manado',
    'bitung': 'Kota Bitung',
    'tomohon': 'Kota Tomohon',
    'kotamobagu': 'Kota Kotamobagu',
    'bolaang mongondow utara': 'Kab. Bolaang Mongondow Utara',
    'bolaang mongondow timur': 'Kab. Bolaang Mongondow Timur',
    'bolaang mongondow selatan': 'Kab. Bolaang Mongondow Selatan',
    'bolaang': 'Kab. Bolaang Mongondow',
    'sitaro': 'Kab. Kepulauan Sitaro',
    'sangihe': 'Kab. Kepulauan Sangihe',
    'talaud': 'Kab. Kepulauan Talaud',
    # Sulawesi Barat
    'mamuju utara': 'Kab. Pasangkayu',
    'mamuju tengah': 'Kab. Mamuju Tengah',
    'mamuju': 'Kab. Mamuju',
    'majene': 'Kab. Majene',
    'polewali': 'Kab. Polewali Mandar',
    'mamasa': 'Kab. Mamasa',
    'pasangkayu': 'Kab. Pasangkayu',
    # Gorontalo
    'pohuwato': 'Kab. Pohuwato',
    'bone bolango': 'Kab. Bone Bolango',
    'boalemo': 'Kab. Boalemo',
    'gorontalo utara': 'Kab. Gorontalo Utara',
    'gorontalo': 'Kab. Gorontalo / Kota Gorontalo',
}

def deduce_kabupaten(text: str, default_val: str = '') -> str:
    """
    Perform keyword-based NER to extract the most specific kabupaten/kota
    from a free text string. Uses longest-match priority.
    """
    text = str(text).lower()
    # Sort by length descending for longest-match first
    for keyword in sorted(KABUPATEN_MAP.keys(), key=len, reverse=True):
        if keyword in text:
            return KABUPATEN_MAP[keyword]
    return default_val

def apply_ner_to_dataframe(df: pd.DataFrame, source_columns: list, target_column: str = 'provinsi', missing_indicator: str = 'Sulawesi (unspecified)'):
    """
    Iterates through a dataframe and updates the target_column using NER footprints 
    found in the source_columns if the target_column matches the missing_indicator.
    """
    def _deduce_row(row):
        # If the province is already specified (not missing indicator), keep it
        if row[target_column] != missing_indicator and pd.notna(row[target_column]):
            return row[target_column]
            
        # Combine text from all source columns
        combined_text = " ".join([str(row[col]) for col in source_columns if pd.notna(row[col])])
        
        return deduce_sulawesi_province(combined_text, default_val=row[target_column])

    df[target_column] = df.apply(_deduce_row, axis=1)
    return df

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NER Location Deducer for Sulawesi Datasets")
    parser.add_argument("--input", required=True, help="Path to input CSV file")
    parser.add_argument("--output", required=True, help="Path to save cleaned CSV file")
    parser.add_argument("--source-cols", nargs='+', required=True, help="Columns to scan for location keywords (e.g. judul deskripsi)")
    parser.add_argument("--target-col", default="provinsi", help="Column to update (default: provinsi)")
    parser.add_argument("--missing-val", default="Sulawesi (unspecified)", help="Value that indicates missing province data")
    
    args = parser.parse_args()
    
    try:
        print(f"Loading data from {args.input}...")
        df = pd.read_csv(args.input)
        
        initial_missing = len(df[df[args.target_col] == args.missing_val])
        print(f"Initial missing/unspecified locations: {initial_missing}")
        
        df = apply_ner_to_dataframe(df, args.source_cols, args.target_col, args.missing_val)
        
        final_missing = len(df[df[args.target_col] == args.missing_val])
        recovered = initial_missing - final_missing
        
        print(f"Recovered {recovered} locations via NER fingerprinting.")
        print("Updated province distribution:")
        print(df[args.target_col].value_counts())
        
        df.to_csv(args.output, index=False)
        print(f"Cleaned dataset saved to {args.output}")
        
    except Exception as e:
        print(f"Error processing dataset: {e}")
        sys.exit(1)
