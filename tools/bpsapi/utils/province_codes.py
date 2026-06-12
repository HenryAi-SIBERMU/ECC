"""
Province and Regency Codes for BPS API
CELIOS ECC Intelligence System

Kode wilayah BPS (Badan Pusat Statistik) Indonesia
"""

# Sulawesi Provinces (focus region for ECC analysis)
# BPS uses 4-digit codes: 7100, 7200, 7300, 7400, 7500, 7600
SULAWESI_PROVINCES = {
    "7100": "Sulawesi Utara",
    "7200": "Sulawesi Tengah",
    "7300": "Sulawesi Selatan",
    "7400": "Sulawesi Tenggara",
    "7500": "Gorontalo",
    "7600": "Sulawesi Barat"
}

# All Indonesia Provinces
INDONESIA_PROVINCES = {
    "11": "Aceh",
    "12": "Sumatera Utara",
    "13": "Sumatera Barat",
    "14": "Riau",
    "15": "Jambi",
    "16": "Sumatera Selatan",
    "17": "Bengkulu",
    "18": "Lampung",
    "19": "Kepulauan Bangka Belitung",
    "21": "Kepulauan Riau",
    "31": "DKI Jakarta",
    "32": "Jawa Barat",
    "33": "Jawa Tengah",
    "34": "DI Yogyakarta",
    "35": "Jawa Timur",
    "36": "Banten",
    "51": "Bali",
    "52": "Nusa Tenggara Barat",
    "53": "Nusa Tenggara Timur",
    "61": "Kalimantan Barat",
    "62": "Kalimantan Tengah",
    "63": "Kalimantan Selatan",
    "64": "Kalimantan Timur",
    "65": "Kalimantan Utara",
    "71": "Sulawesi Utara",
    "72": "Sulawesi Tengah",
    "73": "Sulawesi Selatan",
    "74": "Sulawesi Tenggara",
    "75": "Gorontalo",
    "76": "Sulawesi Barat",
    "81": "Maluku",
    "82": "Maluku Utara",
    "91": "Papua",
    "92": "Papua Barat",
    "93": "Papua Selatan",
    "94": "Papua Tengah",
    "95": "Papua Pegunungan",
    "96": "Papua Barat Daya"
}


def get_province_name(code: str) -> str:
    """
    Get province name from code
    
    Args:
        code: Province code (e.g., "73")
        
    Returns:
        Province name or "Unknown"
    """
    return INDONESIA_PROVINCES.get(code, f"Unknown (code: {code})")


def is_sulawesi(code: str) -> bool:
    """Check if province code is in Sulawesi"""
    return code in SULAWESI_PROVINCES
