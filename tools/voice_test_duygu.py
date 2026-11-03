"""Duygusal ses testi (yeni kanal için): kullanıcının klonlanmış sesiyle, bize ait bir metni
farklı duygu/hız ayarlarında okur; altına yumuşak, prosedürel (telifsiz) piyano yatağı koyar."""
import os, sys, subprocess
import numpy as np
from pocket_tts_turkish import TurkishTTS, save_wav

# Tamamen bize ait metin (başka sayfalardan alınmadı)
LINES = [
    "Hayat, kimin gerçekten yanında olduğunu bazen en zor gününde gösterir.",
    "Kalabalık dağılır. Sesler azalır.",
    "Ama biri kalır.",
    "Hiçbir şey söylemeden, sadece yanına oturur.",
    "İşte o insanı, asla kaybetme.",
]
PAUSE = [0.8, 0.9, 1.0, 0.9, 1.4]

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
SR_OUT = 44100


def write_wav(path, a, sr):
    import wave
    a = np.clip(a, -1, 1)
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((a * 32767).astype(np.int16).tobytes())


def piano_bed(seconds, sr=SR_OUT):
    """Yumuşak arpej: Am - F - C - G, sönümlenen harmonikli tonlar (tamamen sentetik, telifsiz)."""
    chords = [[57, 60, 64, 69], [53, 57, 60, 65], [48, 55, 60, 64], [55, 59, 62, 67]]
    beat = 0.55
    n = int(seconds * sr) + sr * 3
    buf = np.zeros(n, dtype=np.float32)
    t_note = np.arange(int(sr * 2.6)) / sr
    env = np.exp(-t_note * 2.2) * (1 - np.exp(-t_note * 80))
    pos, i = 0.0, 0
    while pos < seconds + 1:
        ch = chords[(i // 8) % 4]
        note = ch[[0, 1, 2, 3, 2, 1, 2, 3][i % 8]]
        f = 440 * 2 ** ((note - 69) / 12)
        tone = (np.sin(2 * np.pi * f * t_note) + 0.35 * np.sin(4 * np.pi * f * t_note)
                + 0.12 * np.sin(6 * np.pi * f * t_note)) * env
        if i % 8 == 0:  # bas
            fb = f / 2
            tone += 0.6 * np.sin(2 * np.pi * fb * t_note) * np.exp(-t_note * 1.2)
        s = int(pos * sr)
        e = min(n, s + len(tone))
        buf[s:e] += tone[: e - s] * 0.22
        pos += beat
        i += 1
    return buf[: int(seconds * sr)]


tts = TurkishTTS.from_pretrained(device="cpu")
if not os.path.exists("/tmp/ref.wav"):
    sys.exit("Ses kaydı yok (VOICE_KEY)")
me = tts.voice_from_file("/tmp/ref.wav")

VARIANTS = [
    # ad, duygu, hız, müzik
    ("1_sakin_yavas_muzikli", "sakin", 1.0, True),
    ("2_uzgun_yavas_muzikli", "üzgün", 1.0, True),
    ("3_normal_yavas_muzikli", None, 1.0, True),
    ("4_sakin_biraz_hizli_muzikli", "sakin", 1.1, True),
    ("5_sakin_yavas_muziksiz", "sakin", 1.0, False),
]

for name, emo, tempo, music in VARIANTS:
    parts = []
    for line, p in zip(LINES, PAUSE):
        kw = {"voice": me, "seed": 7}
        if emo:
            kw["emotion"] = emo
        parts.append(tts.generate(line, **kw))
        parts.append(np.zeros(int(tts.sample_rate * p), dtype=np.float32))
    raw = os.path.join(out, name + "_raw.wav")
    save_wav(raw, np.concatenate(parts), tts.sample_rate)
    voice = os.path.join(out, name + "_v.wav")
    af = (f"atempo={tempo}," if abs(tempo - 1) > 0.01 else "") + \
        "highpass=f=70,lowpass=f=11000,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120," \
        "aecho=0.8:0.6:45|90:0.18|0.10,loudnorm=I=-16:TP=-1.5:LRA=7"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", af, "-ar", str(SR_OUT), "-ac", "1", voice], check=True)
    mp3 = os.path.join(out, name + ".mp3")
    if music:
        dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                             "-of", "csv=p=0", voice]).decode())
        bed = piano_bed(dur + 1.5)
        bed = bed / (np.abs(bed).max() + 1e-6) * 0.9
        bw = os.path.join(out, name + "_m.wav")
        write_wav(bw, bed, SR_OUT)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", voice, "-i", bw, "-filter_complex",
                        "[1]aecho=0.8:0.7:120|240:0.3|0.2,volume=0.13,afade=t=in:d=1.2,afade=t=out:st="
                        f"{dur:.2f}:d=1.5[m];[0]adelay=600|600,apad=pad_dur=1.5[v];[v][m]amix=inputs=2:duration=shortest:normalize=0",
                        "-b:a", "128k", mp3], check=True)
        os.remove(bw)
    else:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", voice, "-b:a", "128k", mp3], check=True)
    for f in (raw, voice):
        os.remove(f)
    print("hazır:", name)
