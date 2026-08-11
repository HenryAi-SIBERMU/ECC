import urllib.request
import urllib.parse
import re
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def search_ddg(query):
    url = 'https://html.duckduckgo.com/html/?q=' + urllib.parse.quote(query)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            html = response.read().decode('utf-8')
            links = set(re.findall(r'href=[\"\'](https://peraturan.bpk.go.id/Details/\d+/[^\"\']+)[\"\']', html))
            for link in links:
                print('Found URL:', link)
    except Exception as e:
        print('Error:', e)

print('Searching PermenLHK 27...')
search_ddg('site:peraturan.bpk.go.id "Permen LHK" "Nomor 27 Tahun 2021"')
print('Searching Permenkes 6...')
search_ddg('site:peraturan.bpk.go.id "Permenkes" "Nomor 6 Tahun 2024"')
