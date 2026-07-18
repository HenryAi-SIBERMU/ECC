import requests

API_KEY = "06fd644648629502353deaed29fc6383"
url_domain = f"https://webapi.bps.go.id/v1/api/list/model/domain/type/all/key/{API_KEY}/"
resp = requests.get(url_domain).json()
print("Domain status:", resp.get("status", "NO STATUS"))
print("Domain message:", resp.get("message", "NO MSG"))
