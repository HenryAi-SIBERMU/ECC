import ast
try:
    ast.parse(open('pages/1_Ekspansi_Industri.py', encoding='utf-8').read())
    print("OK")
except SyntaxError as e:
    print(f"Error at line {e.lineno}: {e.msg}")
