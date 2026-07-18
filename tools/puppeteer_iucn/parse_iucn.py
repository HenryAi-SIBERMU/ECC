import os, glob

def main():
    files = glob.glob('error_*.txt')
    results = []
    for f in files:
        species = f.replace('error_', '').replace('.txt', '').replace('_', ' ')
        try:
            txt = open(f, encoding='utf-8').read()
        except:
            continue
            
        lines = [l.strip() for l in txt.split('\n') if l.strip()]
        
        status_map = {
            'cr': 'Critically Endangered', 
            'en': 'Endangered', 
            'vu': 'Vulnerable', 
            'nt': 'Near Threatened', 
            'lc': 'Least Concern'
        }
        mining_threat = 'No'
        threats_start = False
        for line in lines:
            if line == 'Threats':
                threats_start = True
            elif threats_start and line.startswith('12.'):
                break
            elif threats_start and '3. Energy production & mining' in line:
                if '(1)' in line or '(2)' in line or '(3)' in line:
                    mining_threat = 'Yes'
                    
        # Cari occurrence terakhir (kemungkinan besar di bagian tabel hasil bawah)
        lines_reversed = list(reversed(lines))
        for i, line in enumerate(lines_reversed):
            if species.lower() in line.lower() and "search for" not in line.lower():
                common = lines_reversed[i+1] if i+1 < len(lines_reversed) else 'Unknown'
                trend = lines_reversed[i-1] if i > 0 else 'Unknown'
                status_raw = lines_reversed[i-2].lower() if i > 1 else 'Unknown'
                status = status_map.get(status_raw, status_raw.upper())
                results.append(f'"{species}","{common}","{status}","{trend}","{mining_threat}"')
                found = True
                break
                
        if not found:
            results.append(f'"{species}","Unknown","Unknown","Unknown","Unknown"')

    out = 'Scientific Name,Common Name,Status,Population Trend,Mining Threat\n' + '\n'.join(results)
    out_path = '../../data/raw/biodiversitas_iucn_sulawesi.csv'
    with open(out_path, 'w', encoding='utf-8') as out_f:
        out_f.write(out)
        
    print('CSV Biodiversitas diperbarui dengan data ancaman tambang!')
    print(out)

if __name__ == '__main__':
    main()
