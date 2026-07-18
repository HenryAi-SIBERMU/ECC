import sys
try:
    with open('pages/1_Ekspansi_Industri.py', 'r', encoding='utf-8') as f:
        code = f.read()
    exec(code, {})
    print("RUNTIME OK")
except Exception as e:
    print("RUNTIME ERROR:", e)
