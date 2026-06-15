"""Debug BPS Ekspor API response structure."""
import requests

API_KEY = "06fd644648629502353deaed29fc6383"
url = f"https://webapi.bps.go.id/v1/api/list/model/data/domain/0000/var/2346/th/124:125/key/{API_KEY}/"
r = requests.get(url, timeout=30)
d = r.json()

print("Status:", d.get("data-availability"))
print("Turvars:", d.get("turvar", [])[:3])
print("Tahuns:", d.get("tahun", []))
print("Turtahun:", d.get("turtahun", []))
print("\nVervars (first 5):")
for v in d.get("vervar", [])[:5]:
    print(f"  val={v['val']}, label={v['label']}")

dc = d.get("datacontent", {})
print(f"\nDatacontent: {len(dc)} entries")
print("Sample keys:", list(dc.keys())[:10])
print("Sample values:", list(dc.values())[:5])

# Try to construct a key manually
vervars = d.get("vervar", [])
turvars = d.get("turvar", [])
tahuns = d.get("tahun", [])
turtahun = d.get("turtahun", [])
tt_val = str(turtahun[0]["val"]) if turtahun else "0"

print(f"\nturtahun[0] val: {tt_val}")
if vervars and turvars and tahuns:
    v = vervars[0]
    t = turvars[0]
    th = tahuns[0]
    test_key = f"{v['val']}{2346}{t['val']}{th['val']}{tt_val}"
    print(f"Test key: {test_key}")
    print(f"In datacontent: {test_key in dc}")
    print(f"Value: {dc.get(test_key)}")
