"""Keko Cevo & Hado Dayı - skeç seslendirme (Chatterbox Multilingual, MIT; hazır ses örnekleri Pocket TTS Turkish, CC-BY-4.0).
Her replik ayrı dosya: NN_K.mp3 (K: C=Cevo, H=Hado). Adana ağzı yazımla verilir."""
import os, sys, json, subprocess, wave
import numpy as np
import torch
_load = torch.load
torch.load = lambda *a, **k: _load(*a, **{**k, "map_location": "cpu"})
from chatterbox.mtl_tts import ChatterboxMultilingualTTS
from huggingface_hub import hf_hub_download

out = sys.argv[2]
os.makedirs(out, exist_ok=True)
skit = json.load(open(sys.argv[1], encoding="utf-8"))
m = ChatterboxMultilingualTTS.from_pretrained(device="cpu")
VOICES = {  # karakter -> (örnek ses, perde, yoğunluk, cfg)
    "C": ("male_1", 1.04, 0.8, 0.35),   # Cevo: genç, hızlı, kendinden emin
    "H": ("male_2", 0.90, 0.75, 0.4),   # Hado Dayı: kalın, ağır, göbekli
}
refs = {k: hf_hub_download("wite-tech/pocket-tts-turkish", f"voices/{v[0]}.wav") for k, v in VOICES.items()}
for i, (who, text) in enumerate(skit["lines"], 1):
    ref, pitch, ex, cfg = VOICES[who][0], *VOICES[who][1:]
    torch.manual_seed(100 + i)
    a = m.generate(text, language_id="tr", audio_prompt_path=refs[who], exaggeration=ex, cfg_weight=cfg).squeeze(0).numpy()
    raw = f"/tmp/l{i}.wav"
    with wave.open(raw, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(m.sr)
        w.writeframes((np.clip(a, -1, 1) * 32767).astype(np.int16).tobytes())
    af = f"asetrate={int(m.sr * pitch)},aresample={m.sr},atempo={1.08 / pitch:.3f}," \
         "highpass=f=80,acompressor=threshold=-18dB:ratio=2.5:attack=5:release=60,loudnorm=I=-15:TP=-1.5:LRA=7"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", af, "-ar", "44100", "-ac", "1",
                    os.path.join(out, f"{i:02d}_{who}.wav")], check=True)
    print("hazır:", i, who, flush=True)
