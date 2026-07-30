import os
import re

directory = r"C:\Users\yooma\OneDrive\Desktop\duniahub\client\4. Celios2\tools\streamlittopdf"

replacements = {
    "peningkatan signifikan": "peningkatan signifikan",
    "Peningkatan Signifikan": "Peningkatan Signifikan",
    "terdampak": "terdampak",
    "Terdampak": "Terdampak",
    "krisis ekologis": "krisis ekologis",
    "ekstraksi sumber daya": "ekstraksi sumber daya",
    "konflik fisik": "konflik fisik",
    "morbiditas": "morbiditas",
    "KESIMPULAN": "KESIMPULAN",
    "persetujuan administratif": "persetujuan administratif",
    "masif": "masif",
    "ekspansif terhadap lahan": "ekspansif terhadap lahan",
    "dialokasikan secara maksimal": "dialokasikan secara maksimal",
    "berdampak langsung pada": "berdampak langsung pada",
    "menurunkan indikator": "menurunkan indikator",
    "mengoreksi": "mengoreksi",
    "area dengan prevalensi penyakit tinggi": "area dengan prevalensi penyakit tinggi",
    "area ekstraksi": "area ekstraksi",
    "P-Value: < 0.001": "P-Value: < 0.001",
    "P-Value: < 0.001": "P-Value: < 0.001",
    "TIDAK SIGNIFIKAN": "TIDAK SIGNIFIKAN",
    "TIDAK SIGNIFIKAN": "TIDAK SIGNIFIKAN",
    "SIGNIFIKAN": "SIGNIFIKAN",
}

for filename in os.listdir(directory):
    if filename.endswith(".md") or filename.endswith(".py"):
        filepath = os.path.join(directory, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        new_content = content
        for old, new in replacements.items():
            # simple string replace
            new_content = new_content.replace(old, new)
            
        # also apply some regex if needed for p-values
        new_content = re.sub(r"P-Value\s*:\s*0\.0000?", "P-Value: < 0.001", new_content)
        
        if new_content != content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Updated {filename}")
