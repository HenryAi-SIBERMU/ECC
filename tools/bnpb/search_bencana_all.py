import requests

API_KEY = "0b9fbc7bdccf0bb7bf0ff8502dbd6ec0"

def search_all_subjects():
    url = f"https://webapi.bps.go.id/v1/api/list/model/subject/domain/0000/lang/ind/key/{API_KEY}/"
    resp = requests.get(url)
    data = resp.json()
    if data.get("data") and len(data["data"]) > 1:
        return data["data"][1]
    return []

def search_vars_in_subject(sub_id):
    url = f"https://webapi.bps.go.id/v1/api/list/model/var/domain/0000/subject/{sub_id}/lang/ind/key/{API_KEY}/"
    resp = requests.get(url)
    try:
        data = resp.json()
        if data.get("data") and len(data["data"]) > 1:
            for v in data["data"][1]:
                title = v.get("title", "").lower()
                if "bencana" in title or "banjir" in title or "longsor" in title:
                    print(f"✅ KETEMU! Subjek {sub_id} -> ID: {v['var_id']} | Judul: {v['title']}")
    except:
        pass

if __name__ == "__main__":
    print("Mengambil daftar subjek...")
    subjects = search_all_subjects()
    print(f"Mencari kata kunci 'bencana/banjir/longsor' di {len(subjects)} subjek BPS...")
    for s in subjects:
        sub_id = s.get("sub_id")
        search_vars_in_subject(sub_id)
    print("Selesai pencarian di seluruh subjek BPS.")
