"""Ses karşılaştırma: aynı iki cümle, farklı ücretsiz/ticari serbest modeller ve sesler.
Kullanım: python tools/ses_karsilastir.py <pocket|chatterbox> <çıktı>"""
import os, sys, subprocess
import numpy as np

T = ["Hayat, kimin gerçekten yanında olduğunu bazen en zor gününde gösterir. Ama biri kalır.",
     "Yıl bin dört yüz elli üç. Bir gecede, gemiler karadan yürüyerek Haliç'e indirildi!"]
which, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
ME = "/tmp/ref.wav" if os.path.exists("/tmp/ref.wav") else None


def finish(name, chunks, sr):
    import wave
    y = np.concatenate([np.concatenate([np.asarray(c, np.float32).reshape(-1), np.zeros(int(sr * 0.8), np.float32)]) for c in chunks])
    raw = f"/tmp/{name}.wav"
    with wave.open(raw, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes())
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af",
                    "highpass=f=70,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120,loudnorm=I=-16:TP=-1.5:LRA=7",
                    "-ar", "44100", "-b:a", "128k", os.path.join(out, name + ".mp3")], check=True)
    print("hazır:", name, flush=True)


if which in ("voxcpm", "trendyol"):
    subprocess.run([sys.executable, "tools/voxcpm_test.py", which, out], check=True)
    sys.exit(0)

if which == "adana":
    subprocess.run([sys.executable, "tools/adana_skec.py", "tools/skec/001_diyet.json", out], check=True)
    sys.exit(0)

if which == "pocket":
    from pocket_tts_turkish import TurkishTTS
    tts = TurkishTTS.from_pretrained(device="cpu")
    if ME:
        v = tts.voice_from_file(ME)
        finish("01_pocket_senin_sesin_simdiki", [tts.generate(t, voice=v, seed=7, emotion="sakin") for t in T], tts.sample_rate)
    for i, name in enumerate(["female_1", "female_2", "female_3", "male_1", "male_2", "male_3"]):
        try:
            finish(f"0{i + 2}_pocket_hazir_{name}", [tts.generate(t, voice=name, seed=7, emotion="sakin") for t in T], tts.sample_rate)
        except Exception as e:  # noqa: BLE001
            print("yok:", name, e)
elif which == "chatterbox":
    import torch
    _load = torch.load
    torch.load = lambda *a, **k: _load(*a, **{**k, "map_location": "cpu"})
    from chatterbox.mtl_tts import ChatterboxMultilingualTTS
    from huggingface_hub import hf_hub_download
    m = ChatterboxMultilingualTTS.from_pretrained(device="cpu")

    def run(name, ref, ex=0.5, cfg=0.5):
        chunks = []
        for t in T:
            kw = {"language_id": "tr", "exaggeration": ex, "cfg_weight": cfg}
            if ref:
                kw["audio_prompt_path"] = ref
            chunks.append(m.generate(t, **kw).squeeze(0).numpy())
        finish(name, chunks, m.sr)

    if ME:
        run("10_chatterbox_senin_sesin_dogal", ME)
        run("11_chatterbox_senin_sesin_duygulu", ME, ex=0.75, cfg=0.3)
    run("12_chatterbox_varsayilan_ses", None)
    for j, name in enumerate(["female_1", "male_1", "male_2"]):
        try:
            ref = hf_hub_download("wite-tech/pocket-tts-turkish", f"voices/{name}.wav")
            run(f"1{3 + j}_chatterbox_ornek_{name}", ref)
        except Exception as e:  # noqa: BLE001
            print("örnek ses yok:", name, e)

if which == "karikatur":
    # Çöp Adamla Tarih: senin sesin (Chatterbox, 10 numara ayarı) + karikatür efekti
    import torch
    _load = torch.load
    torch.load = lambda *a, **k: _load(*a, **{**k, "map_location": "cpu"})
    from chatterbox.mtl_tts import ChatterboxMultilingualTTS
    m = ChatterboxMultilingualTTS.from_pretrained(device="cpu")
    LINES = ["Dur, kaydırma! Sana bir sır vereyim. Bir zamanlar gemiler karada yürüdü. Hem de tek bir gecede!",
             "Yıl bin dört yüz elli üç. Yirmi bir yaşındaki Fatih Sultan Mehmet, İstanbul'u almaya kararlı."]
    base = {}
    for key, ex, cfg in (("dogal", 0.5, 0.5), ("canli", 0.7, 0.4)):
        base[key] = [m.generate(t, language_id="tr", audio_prompt_path=ME, exaggeration=ex, cfg_weight=cfg).squeeze(0).numpy() for t in LINES]
        finish(f"20_tarih_{key}_efektsiz", base[key], m.sr)
    import wave
    def cartoon(name, key, pitch, tempo, bright):
        raw = f"/tmp/k_{name}.wav"
        y = np.concatenate([np.concatenate([c.reshape(-1), np.zeros(int(m.sr * 0.6), np.float32)]) for c in base[key]])
        with wave.open(raw, "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(m.sr)
            w.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes())
        af = f"asetrate={int(m.sr * pitch)},aresample={m.sr},atempo={tempo / pitch:.3f}"
        if bright:
            af += ",equalizer=f=3500:t=q:w=1:g=4,equalizer=f=180:t=q:w=1:g=-3"
        af += ",highpass=f=90,acompressor=threshold=-20dB:ratio=3:attack=5:release=80,loudnorm=I=-15:TP=-1.5:LRA=6"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", af, "-ar", "44100", "-b:a", "128k",
                        os.path.join(out, name + ".mp3")], check=True)
        print("hazır:", name, flush=True)
    cartoon("21_karikatur_hafif", "dogal", 1.10, 1.12, False)
    cartoon("22_karikatur_orta", "dogal", 1.18, 1.15, True)
    cartoon("23_karikatur_belirgin", "dogal", 1.26, 1.18, True)
    cartoon("24_karikatur_orta_canli", "canli", 1.18, 1.12, True)
    cartoon("25_karikatur_belirgin_canli", "canli", 1.26, 1.15, True)
