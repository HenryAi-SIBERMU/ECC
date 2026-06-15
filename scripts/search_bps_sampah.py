import requests

def search_sampah():
    url = 'https://webapi.bps.go.id/v1/api/list/model/statictable/lang/ind/domain/0000/keyword/sampah/key/82a7a4212555c82ff19fc1b47659a848/'
    resp = requests.get(url, verify=False)
    data = resp.json()
    if 'data' in data:
        for p in data['data'][1]:
            print(f"ID={p['table_id']} | {p['title']}")

if __name__ == "__main__":
    search_sampah()
