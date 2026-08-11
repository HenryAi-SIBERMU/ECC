import urllib.request
import re
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def download_bpk(bpk_id, filename):
    url = f'https://peraturan.bpk.go.id/Details/{bpk_id}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            html = response.read().decode('utf-8')
            match = re.search(r'href=[\"\'](/Home/Download/' + str(bpk_id) + r'/[^\"\']+)[\"\']', html)
            if match:
                download_url = 'https://peraturan.bpk.go.id' + match.group(1).replace(' ', '%20')
                print('Found download URL:', download_url)
                
                req2 = urllib.request.Request(download_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
                with urllib.request.urlopen(req2, context=ctx) as res2, open(filename, 'wb') as f:
                    f.write(res2.read())
                print(f'Successfully downloaded {filename}!')
            else:
                print(f'Could not find download link in HTML for {bpk_id}')
    except Exception as e:
        print(f'Error for {bpk_id}: {e}')

download_bpk('211000', 'PermenLHK_No_6_Tahun_2021.pdf')
