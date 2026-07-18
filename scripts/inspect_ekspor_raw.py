"""Inspect header structure of raw ekspor Excel."""
import pandas as pd

xlsx_path = r"data\raw\eksporimpor\exim_sulsel.bps.go.id_Selasa, 09 Juni 2026 pukul 12.24.09.xlsx"
xl = pd.ExcelFile(xlsx_path)
df = pd.read_excel(xl, "Sheet1", header=None)

print(f"Shape: {df.shape}")
print(f"\n=== ROW 0 (first 20 cols) ===")
for i in range(min(20, df.shape[1])):
    val = df.iloc[0, i]
    if pd.notna(val):
        print(f"  Col {i}: {val}")

print(f"\n=== ROW 1 (first 20 cols) ===")
for i in range(min(20, df.shape[1])):
    val = df.iloc[1, i]
    if pd.notna(val):
        print(f"  Col {i}: {val}")

print(f"\n=== ROW 2 (first 20 cols) ===")
for i in range(min(20, df.shape[1])):
    val = df.iloc[2, i]
    if pd.notna(val):
        print(f"  Col {i}: {val}")

# Find non-NaN columns in row 0
print(f"\n=== ALL non-NaN in row 0 ===")
for i in range(df.shape[1]):
    val = df.iloc[0, i]
    if pd.notna(val):
        print(f"  Col {i}: {val}")

# Find non-NaN columns in row 1
print(f"\n=== ALL non-NaN in row 1 ===")
for i in range(df.shape[1]):
    val = df.iloc[1, i]
    if pd.notna(val):
        print(f"  Col {i}: {val}")

# Check first 10 data rows (col 0 and 1)
print(f"\n=== First 30 data rows (col 0, 1, last col) ===")
last_col = df.shape[1] - 1
for i in range(min(30, df.shape[0])):
    c0 = df.iloc[i, 0]
    c1 = df.iloc[i, 1]
    cl = df.iloc[i, last_col]
    if pd.notna(c0) or pd.notna(c1):
        print(f"  Row {i}: col0={c0}, col1={c1}, last={cl}")
