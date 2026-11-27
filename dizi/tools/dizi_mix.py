"""Çapkın Nihat: ses miksi. Ses (voice.wav) + müzik (Kevin MacLeod, CC BY 4.0; yoksa sentetik gerilim pedi)
+ ortam (gece odası / sabah) + efektler (cues.json: render.mjs --cues yazar).

  python dizi/tools/dizi_mix.py dizi/stories/D01 [muzik.mp3]

Çıktı: <bolum>/audio/mix.wav (-14 LUFS)."""
import json
import os
import pathlib
import subprocess
import sys

import numpy as np

SR = 48000
story = pathlib.Path(sys.argv[1])
muzik_yolu = sys.argv[2] if len(sys.argv) > 2 else None
cues = json.load(open(story / "audio" / "cues.json", encoding="utf-8"))
DUR = cues["DUR"]
N = int(DUR * SR)
rng = np.random.default_rng(11)


def load(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()


def save(p, x):
    x = np.clip(x, -1, 1)
    st = np.stack([x, x], 1)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", str(p)],
                   input=st.astype(np.float32).tobytes(), check=True)


def band(x, lo, hi):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    m = 1 / (1 + (lo / np.maximum(f, 1)) ** 4) / (1 + (f / hi) ** 4)
    return np.fft.irfft(X * m, len(x))


def env_ad(n, a, d):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / max(d, 1e-4))


def put(buf, t, x, g=1.0):
    i = int(t * SR)
    j = min(len(buf), i + len(x))
    if 0 <= i < len(buf) and j > i:
        buf[i:j] += x[:j - i] * g


def db(v):
    return 10 ** (v / 20)


# ------------------------------------------------------------------ efektler
def titresim(dur):            # telefon titreşimi: komodin üstünde iki kısa vızz
    n = int(dur * SR)
    t = np.arange(n) / SR
    tone = np.sign(np.sin(2 * np.pi * 168 * t)) * .5 + np.sin(2 * np.pi * 336 * t) * .3
    gate = ((t % .55) < .32).astype(float)
    gate = np.convolve(gate, np.ones(400) / 400, "same")
    return band(tone * gate, 90, 2400) * .5


def bildirim():               # yumuşak iki notalı bildirim
    out = np.zeros(int(.9 * SR))
    for k, (f, t0) in enumerate([(1318.5, 0), (1760, .12)]):
        n = int(.7 * SR)
        t = np.arange(n) / SR
        x = (np.sin(2 * np.pi * f * t) + .3 * np.sin(2 * np.pi * f * 2 * t)) * env_ad(n, .004, .18)
        put(out, t0, x, .35)
    return out


def kalp(dur):                # kalp atışı (lup-dup), ~72 bpm
    out = np.zeros(int(dur * SR))
    for b in np.arange(0, dur - .3, 60 / 72):
        for dt, g in [(0, 1), (.16, .7)]:
            n = int(.25 * SR)
            t = np.arange(n) / SR
            put(out, b + dt, np.sin(2 * np.pi * (52 + 30 * np.exp(-t * 40)) * t) * env_ad(n, .002, .07), g * .9)
    return out


def klik():
    n = int(.08 * SR)
    return band(rng.standard_normal(n), 1500, 7000) * env_ad(n, .0003, .006) * .6 + \
        np.sin(2 * np.pi * 900 * np.arange(n) / SR) * env_ad(n, .0005, .01) * .2


def whoosh(dur=.45):
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = rng.standard_normal(n)
    sw = np.sin(np.pi * t / dur) ** 2
    return (band(x, 300, 2200) * .55 + band(x, 2200, 6000) * .2) * sw * .5


def kumas(dur=.6):
    n = int(dur * SR)
    t = np.arange(n) / SR
    return band(rng.standard_normal(n), 800, 5000) * (np.sin(np.pi * t / dur) ** 1.5) * (.6 + .4 * np.sin(t * 40)) * .25


def kapi():                   # kilit dili + kısa gıcırtı
    out = np.zeros(int(1.0 * SR))
    put(out, 0, klik(), 1.2)
    put(out, .09, klik(), .8)
    n = int(.55 * SR)
    t = np.arange(n) / SR
    f = 520 + 160 * np.sin(t * 7)
    put(out, .25, np.sin(2 * np.pi * np.cumsum(f) / SR) * band(rng.standard_normal(n), 300, 3000) * .15 * np.sin(np.pi * t / .55), 1)
    return out


def kapi_kapan():
    n = int(.6 * SR)
    t = np.arange(n) / SR
    return np.sin(2 * np.pi * (60 + 40 * np.exp(-t * 30)) * t) * env_ad(n, .002, .12) * .9 + \
        band(rng.standard_normal(n), 200, 2000) * env_ad(n, .001, .05) * .4


def vurgu():                  # son cümle: alçak darbe + yükselen nefes
    n = int(2.4 * SR)
    t = np.arange(n) / SR
    boom = np.sin(2 * np.pi * (44 + 30 * np.exp(-t * 6)) * t) * env_ad(n, .004, .9) * .9
    return boom


def gece_ortam(n):            # oda tonu + uzak şehir uğultusu
    x = rng.standard_normal(n)
    return band(x, 40, 300) * .05 + band(x, 300, 1200) * .012


def sabah_ortam(n):           # hafif dış ses + ara ara kuş
    out = band(rng.standard_normal(n), 200, 3000) * .012
    t = 0.3
    while t < n / SR - .5:
        m = int(.18 * SR)
        tt = np.arange(m) / SR
        f = 3200 + 900 * np.sin(tt * 60)
        put(out, t, np.sin(2 * np.pi * np.cumsum(f) / SR) * env_ad(m, .01, .05) * .05)
        t += rng.uniform(.6, 1.8)
    return out


# ------------------------------------------------------------------ müzik
def sentetik_ped(n):          # yedek: Do minörde yumuşak gerilim pedi + seyrek piyano
    t = np.arange(n) / SR
    x = np.zeros(n)
    for f, g in [(65.4, .5), (98.0, .35), (155.6, .25), (196.0, .18)]:
        x += np.sin(2 * np.pi * f * t + np.sin(t * .3) * .4) * g
    x = band(x, 40, 1200) * .12 * (0.8 + .2 * np.sin(t * .5))
    notes = [523.3, 466.2, 392.0, 311.1, 392.0, 349.2]
    for i, tt in enumerate(np.arange(1.0, n / SR - 1, 2.4)):
        m = int(2.2 * SR)
        u = np.arange(m) / SR
        f = notes[i % len(notes)]
        put(x, tt, (np.sin(2 * np.pi * f * u) + .4 * np.sin(4 * np.pi * f * u)) * env_ad(m, .005, .8) * .06)
    return x


voice = load(story / "voice" / "voice.wav")[:N]
voice = np.pad(voice, (0, max(0, N - len(voice))))
music = None
if muzik_yolu and os.path.exists(muzik_yolu):
    try:
        m = load(muzik_yolu)
        if len(m) < N:
            m = np.tile(m, int(np.ceil(N / len(m))))
        music = m[:N]
        music = music / (np.percentile(np.abs(music), 99.5) + 1e-6) * .5
        print("müzik:", muzik_yolu)
    except Exception as e:  # noqa: BLE001
        print("müzik okunamadı:", e)
if music is None:
    music = sentetik_ped(N)
    music = music / (np.percentile(np.abs(music), 99.5) + 1e-6) * .5

# ducking: ses varken müzik %45 daha kısık (yumuşak zarf)
hop = SR // 50
venv = np.sqrt(np.convolve(voice ** 2, np.ones(hop) / hop, "same"))
act = (venv > np.percentile(venv, 60) * .5).astype(float)
act = np.convolve(act, np.ones(SR // 4) / (SR // 4), "same")
duck = 1 - .45 * np.clip(act, 0, 1)
mg = np.full(N, db(-17))
sfx = np.zeros(N)
amb = np.zeros(N)
for c in cues["cues"]:
    t, typ, d = c["t"], c["type"], c.get("dur", 1.0)
    if typ == "titresim":
        put(sfx, t, titresim(d), db(-12))
    elif typ == "bildirim":
        put(sfx, t, bildirim(), db(-10))
    elif typ == "kalp":
        put(sfx, t, kalp(d), db(-9))
    elif typ == "klik":
        put(sfx, t, klik(), db(-9))
    elif typ == "whoosh":
        put(sfx, t - .2, whoosh(), db(-14))
    elif typ == "kumas":
        put(sfx, t, kumas(), db(-12))
    elif typ == "kapi":
        put(sfx, t, kapi(), db(-10))
    elif typ == "kapi_kapan":
        put(sfx, t, kapi_kapan(), db(-9))
    elif typ == "vurgu":
        put(sfx, t, vurgu(), db(-8))
    elif typ == "gece":
        put(amb, t, gece_ortam(int(d * SR)), 1)
    elif typ == "sabah":
        put(amb, t, sabah_ortam(int(d * SR)), 1)
    elif typ == "son":                                  # son kart: müzik öne çıkar
        i0 = int(t * SR)
        mg[i0:] = np.linspace(db(-17), db(-8), N - i0)
        duck[i0:] = 1
# başta 0.3 sn yumuşak giriş, sonda 1.2 sn sönüş
fade = np.ones(N)
fade[:int(.3 * SR)] = np.linspace(0, 1, int(.3 * SR))
fade[-int(1.2 * SR):] = np.linspace(1, 0, int(1.2 * SR))
mix = (voice + music * mg * duck + sfx + amb * db(-6)) * fade
out = story / "audio"
out.mkdir(exist_ok=True)
save(out / "mix_ham.wav", mix)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(out / "mix_ham.wav"), "-af", "loudnorm=I=-14:TP=-2:LRA=9",
                "-ar", str(SR), str(out / "mix.wav")], check=True)
os.remove(out / "mix_ham.wav")
print("mix ->", out / "mix.wav", f"{DUR:.1f} sn")
