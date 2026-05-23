import os
import pandas as pd
import streamlit as st

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "processed")


@st.cache_data
def load_nasional() -> pd.DataFrame:
    path = os.path.join(DATA_DIR, "nasional_summary.csv")
    return pd.read_csv(path)


@st.cache_data
def load_provinsi() -> pd.DataFrame:
    path = os.path.join(DATA_DIR, "provinsi_ecc.csv")
    return pd.read_csv(path)


def fmt_number(val, decimals=2) -> str:
    """Format angka dengan pemisah ribuan dan desimal."""
    try:
        return f"{val:,.{decimals}f}"
    except (TypeError, ValueError):
        return str(val)


def get_val(df: pd.DataFrame, col: str, default=0):
    """Ambil nilai pertama dari kolom DataFrame dengan fallback."""
    try:
        return df[col].iloc[0]
    except (KeyError, IndexError):
        return default


def get_growth_color(growth_val) -> str:
    """
    Warna pertumbuhan untuk ECC:
    - Defisit makin besar (positif) → merah (buruk)
    - Defisit makin kecil / reserve makin besar (negatif) → hijau (baik)
    """
    try:
        val = float(growth_val)
        if val > 0:
            return "#EF4444"
        elif val < 0:
            return "#22C55E"
        else:
            return "#94A3B8"
    except (TypeError, ValueError):
        return "#94A3B8"


def get_ecc_status_color(defisit_val) -> str:
    """Warna berdasarkan status ECC per provinsi."""
    try:
        val = float(defisit_val)
        if val > 0.5:
            return "#EF4444"
        elif val > 0:
            return "#F97316"
        elif val == 0:
            return "#EAB308"
        else:
            return "#22C55E"
    except (TypeError, ValueError):
        return "#94A3B8"
