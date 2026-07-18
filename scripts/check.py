lines = open('pages/1_Ekspansi_Industri.py', encoding='utf-8').readlines()
quotes = []
for i, l in enumerate(lines):
    count = l.count('\"\"\"')
    if count > 0:
        quotes.append((i+1, count, l.strip()))
for q in quotes:
    print(q)
