"""Instagram'a YAYINLAMADAN yükleme testi: kapsayıcı oluşturur, videoyu yükler, Meta'nın işlemesini bekler.
media_publish ÇAĞRILMAZ; yayınlanmayan kapsayıcı 24 saatte kendiliğinden silinir.
Kullanım: python tools/yukleme_testi.py <video_yolu> [video_url]"""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import publisher as P

path = sys.argv[1]
url = sys.argv[2] if len(sys.argv) > 2 else None
token = os.environ["IG_ACCESS_TOKEN"]
mode = P.detect_mode(token)
uid = P.resolve_user_id(token, mode)
host = P._host(mode)
base = f"https://{host}/{P.API_VERSION}"
c = P._request("POST", f"{base}/{uid}/media", {"media_type": "REELS", "upload_type": "resumable",
                                               "caption": "test", "access_token": token})
cid = c["id"]
uri = c.get("uri") or f"https://rupload.facebook.com/ig-api-upload/{P.API_VERSION}/{cid}"
try:
    if url:
        P._request("POST", uri, headers={"Authorization": f"OAuth {token}", "file_url": url}, timeout=600)
    else:
        data = open(path, "rb").read()
        P._request("POST", uri, headers={"Authorization": f"OAuth {token}", "offset": "0",
                                         "file_size": str(len(data)), "Content-Type": "application/octet-stream"},
                   data=data, timeout=600)
    print("yükleme: tamam")
except P.PublishError as e:
    print("yükleme hatası:", e)
t0 = time.time()
while time.time() - t0 < 300:
    info = P._request("GET", f"{base}/{cid}", {"fields": "status_code,status", "access_token": token})
    if info.get("status_code") in ("FINISHED", "ERROR", "EXPIRED"):
        break
    time.sleep(10)
print("SONUÇ:", os.path.basename(path), info, "(yayınlanmadı)")
