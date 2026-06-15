import requests, urllib3, json
urllib3.disable_warnings()
api_key = '06fd644648629502353deaed29fc6383'

queries = ['indeks kualitas air', 'IKLH', 'IKA', 'kualitas lingkungan']
for q in queries:
    encoded = q.replace(' ', '%20')
    url = f'https://webapi.bps.go.id/v1/api/list/model/statictable/domain/0000/lang/ind/keyword/{encoded}/key/{api_key}'
    r = requests.get(url, timeout=10)
    try:
        data = r.json()
        raw = data.get('data', [])
        # data is [meta_dict, list_of_tables]
        if isinstance(raw, list) and len(raw) == 2:
            tables = raw[1]
        elif isinstance(raw, list):
            tables = raw
        else:
            tables = []
        print(f'Query: [{q}] -> {len(tables)} hasil')
        for t in tables:
            print(f'  ID={t.get("table_id")} | {t.get("title")}')
    except Exception as e:
        print(f'Query [{q}] ERROR: {e} | Response: {r.text[:200]}')
    print()
