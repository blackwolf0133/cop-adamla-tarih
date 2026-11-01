"""8 günlük çalışmayı simüle eder: render + sahte paylaşım + kayıt."""
import json, os, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import daily, publisher
publisher.publish_reel = lambda **kw: {"media_id": "FAKE", "permalink": "https://instagram.com/reel/FAKE/", "container_id": "C"}
daily.save_state({"posted": []})
n = int(sys.argv[1]) if len(sys.argv) > 1 else 8
for day in range(n):
    q = daily.queue()
    if not q:
        print("Sıra bitti"); break
    daily.cmd_render(None)
    today = json.load(open(daily.TODAY))
    info = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type",
                           "-of", "json", today["path"]], capture_output=True, text=True)
    d = json.loads(info.stdout)
    dur = float(d["format"]["duration"]); kinds = sorted(s["codec_type"] for s in d["streams"])
    ok = 5 <= dur <= 90 and kinds == ["audio", "video"]
    tags = today["caption"].count("#")
    daily.cmd_publish(type("A", (), {"video_url": "https://x/y.mp4"}))
    print(f"GÜN {day+1}: {today['id']} {today['title'][:40]:40s} {dur:5.1f} sn  etiket={tags}  {'OK' if ok and tags <= 5 else 'SORUN'}", flush=True)
