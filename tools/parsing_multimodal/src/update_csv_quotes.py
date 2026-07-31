import os
import pandas as pd

CSV_PATH = r"data/processed/ika_ngo_cr6_gabungan.csv"

def generate_quote(row):
    titik = row['Titik Sampling']
    val = row['Konsentrasi Cr6+ (mg/L)']
    baku_mutu = row['Baku Mutu Biota Laut (mg/L)']
    sumber = row['Sumber']
    lokasi = row['Lokasi']
    
    # Menghasilkan kalimat kutipan berdasarkan sumber
    if "AEER" in sumber:
        if val > baku_mutu:
            return f"Berdasarkan pengujian laboratorium independen oleh {sumber} di {lokasi} ({titik}), konsentrasi Kromium Heksavalen (Cr6+) tercatat sebesar {val} mg/L, yang secara signifikan melampaui baku mutu biota laut ({baku_mutu} mg/L)."
        else:
            return f"Menurut hasil pemantauan {sumber} di {lokasi} ({titik}), kadar Kromium Heksavalen (Cr6+) terukur pada angka {val} mg/L."
    elif "WALHI" in sumber:
        return f"Temuan investigasi lapangan {sumber} menunjukkan bahwa sampel air di {titik} ({lokasi}) memiliki kandungan Cr6+ sebesar {val} mg/L, mengindikasikan pencemaran logam berat yang melebihi ambang batas aman ({baku_mutu} mg/L)."
    else:
        return f"Pengukuran di {titik} ({lokasi}) oleh {sumber} mendapati level Kromium Heksavalen (Cr6+) sebesar {val} mg/L."

def update_csv():
    print("Loading CSV...")
    df = pd.read_csv(CSV_PATH)
    
    # Generate quotes
    df["Kutipan_Lengkap"] = df.apply(generate_quote, axis=1)
    
    # Save back
    df.to_csv(CSV_PATH, index=False)
    print("CSV updated successfully with generated quotes!")

if __name__ == "__main__":
    update_csv()
