"""Geçici: ScrapeCreators ile anahtar kelimeyle Instagram profil + Reels arar (salt okuma)."""
import json, os, sys, urllib.parse, urllib.request
KEY = os.environ["SC_KEY"]
def get(path, **q):
    url = f"https://api.scrapecreators.com{path}?" + urllib.parse.urlencode(q)
    try:
        return json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"x-api-key": KEY}), timeout=90))
    except Exception as e:  # noqa: BLE001
        return {"hata": str(e)}
def walk(o, out):
    if isinstance(o, dict):
        u = o.get("username") or (o.get("owner") or {}).get("username") if isinstance(o.get("owner"), dict) else o.get("username")
        if u:
            out.append({k: o.get(k) for k in ("username", "full_name", "follower_count", "followers", "is_verified",
                                              "video_view_count", "video_play_count", "play_count", "like_count") if o.get(k) is not None}
                       | ({"owner": o["owner"].get("username")} if isinstance(o.get("owner"), dict) else {}))
        for v in o.values():
            walk(v, out)
    elif isinstance(o, list):
        for v in o:
            walk(v, out)
print("=====ARA_BASLA=====")
for q in [x.strip() for x in sys.argv[1].split("|") if x.strip()]:
    for path in ("/v1/instagram/search/profiles", "/v2/instagram/reels/search"):
        r = get(path, query=q)
        out = []
        walk(r, out)
        print(json.dumps({"q": q, "path": path, "hata": r.get("hata") if isinstance(r, dict) else None,
                          "anahtarlar": list(r.keys())[:8] if isinstance(r, dict) else None, "sonuc": out[:40]}, ensure_ascii=False))
print("=====ARA_BITTI=====")
