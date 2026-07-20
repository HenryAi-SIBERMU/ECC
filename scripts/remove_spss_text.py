import os

replacements = {
    "pages/11_Demografi_Sosial.py": [
        ("tool SPSS crosstab", "tool crosstab"),
        ("Uji SPSS-Style Crosstab", "Uji Crosstab"),
        ("SPSS-style crosstab", "uji crosstab")
    ],
    "pages/4_Konflik_Sosial.py": [
        ("& SPSS-Style Crosstabulation", "& Crosstabulation"),
        ("gaya SPSS ", ""),
        ("gaya SPSS", ""),
        ("(Chi-Square SPSS Style)", "(Chi-Square)")
    ],
    "pages/3_Beban_Kesehatan.py": [
        ("standar SPSS", "statistik formal")
    ],
    "pages/1_Ekspansi_Industri.py": [
        ("standar SPSS", "statistik formal")
    ],
    "pages/2_Kualitas_Lingkungan.py": [
        (" ala SPSS", ""),
        ("ala SPSS", ""),
        ("Crosstabulation SPSS", "Crosstabulation"),
        ("SPSS Crosstab Section", "Crosstab Section")
    ],
    "pages/5_Pola_Penerbitan_Izin.py": [
        ("standar SPSS", "statistik formal")
    ]
}

for filepath, reps in replacements.items():
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        for old, new in reps:
            content = content.replace(old, new)
            
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Processed {filepath}")
