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
else:
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
