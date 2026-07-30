import glob, re
for f in sorted(glob.glob('pages/*.py')):
    print(f"\n--- {f} ---")
    for l in open(f, encoding='utf-8'):
        m = re.search(r'(?:st\.subheader|st\.markdown)\s*\(\s*[\'\"](?:###\s*)?(.*?)(?:[\'\"])', l)
        if m:
            print(m.group(1))
