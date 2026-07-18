import requests
import re
import urllib3
urllib3.disable_warnings()

js_url = 'https://tailing.grida.no/static/static_files/web_spesific/js/main.js'
print(f"Fetching {js_url}")
text = requests.get(js_url, verify=False).text

# Cari string yang dimulai dengan /api/ atau mengandung json
matches = re.findall(r"['\"](/api/[a-zA-Z0-9_/-]+)['\"]", text)
matches += re.findall(r"['\"](/[a-zA-Z0-9_/-]+\.json)['\"]", text)

print("Semua endpoint potensial di main.js:")
for m in set(matches):
    print(m)

# Coba cari url untuk search atau filter
search_urls = re.findall(r"url\s*:\s*['\"]([^'\"]+)['\"]", text)
for u in set(search_urls):
    print("AJAX URL:", u)
