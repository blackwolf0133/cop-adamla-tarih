"""Adana ağzı skeç ses testi: iki karakterli diyalog, kullanıcının klonlanmış sesiyle.
Şive yazımla verilir (diyon, gari, ula...). Varyantlar ikinci karakter için farklı ses dener."""
import os, sys, subprocess
import numpy as np
from pocket_tts_turkish import TurkishTTS, save_wav

# (konuşan, metin, duygu) — tamamen özgün skeç
SKIT = [
    ("B", "Abi kırk dört derece ula! Şu klimayı açak mı?", "şaşkın"),
    ("K", "Ne klimesi la! Adanalı klima açmaz. Sıcağı terbiye eder.", "kızgın"),
    ("B", "Nasıl terbiye ediyon abi?", None),
    ("K", "Bak. Bi bardak acılı şalgam içecen, sıcak utanıp kaçacak.", "sakin"),
    ("B", "Abi... şalgam bitmiş.", "üzgün"),
    ("K", "Aç gari klimayı! Aç aç! Ama kimseye deme haa!", "şaşkın"),
]
out = sys.argv[1]
os.makedirs(out, exist_ok=True)
tts = TurkishTTS.from_pretrained(device="cpu")
if not os.path.exists("/tmp/ref.wav"):
    sys.exit("ses kaydı yok")
me = tts.voice_from_file("/tmp/ref.wav")
SR = 44100


def gen(voice, text, emo, pitch=1.0, tempo=1.12):
    kw = {"voice": voice, "seed": 11}
    if emo:
        kw["emotion"] = emo
    raw = "/tmp/_r.wav"
    save_wav(raw, tts.generate(text, **kw), tts.sample_rate)
    af = []
    if pitch != 1.0:
        af.append(f"asetrate={int(tts.sample_rate * pitch)},aresample={tts.sample_rate}")
        tempo = tempo / pitch
    af.append(f"atempo={tempo:.3f}")
    af.append("highpass=f=70,acompressor=threshold=-18dB:ratio=2.5:attack=5:release=60,loudnorm=I=-16:TP=-1.5:LRA=7")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", ",".join(af), "-ar", str(SR), "-ac", "1", "/tmp/_o.wav"], check=True)
    import wave
    with wave.open("/tmp/_o.wav") as w:
        return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768


VARIANTS = [
    # ad, Kâzım sesi, Bayram sesi, Bayram perdesi
    ("1_kazim_senin_sesin__bayram_senin_sesin_tiz", me, me, 1.16),
    ("2_kazim_senin_sesin__bayram_hazir_ses", me, "male_3", 1.0),
    ("3_kazim_senin_sesin__bayram_hazir_ses2", me, "male_2", 1.05),
]
for name, kv, bv, bp in VARIANTS:
    parts = []
    for who, text, emo in SKIT:
        a = gen(kv, text, emo) if who == "K" else gen(bv, text, emo, pitch=bp)
        parts += [a, np.zeros(int(SR * 0.35), np.float32)]
    y = np.concatenate(parts)
    import wave
    wav = os.path.join(out, name + ".wav")
    with wave.open(wav, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes())
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", wav, "-b:a", "128k", wav[:-4] + ".mp3"], check=True)
    os.remove(wav)
    print("hazır:", name)
