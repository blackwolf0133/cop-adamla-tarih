"""Çapkın Nihat: bölüm sesi. Her satırı kendi sesiyle (Gemini TTS) okutur, iç sesi yakın/yankılı, konuşmaları kuru işler,
satırları aralıklarla birleştirir, kelime saatlerini (faster-whisper) çıkarır, dudak zarfını yazar.

  python dizi/tools/ses_uret.py dizi/stories/D01

Girdi:  <bolum>/voice/satirlar.json  {"sesler": {kim: {voice, fx, tempo}}, "satirlar": [{id, kim, metin, ara}]}
Çıktı:  <bolum>/voice/voice.wav, words.json ({"words": [...], "lines": [...]}), env.json, satir/<id>.wav
Ortam:  GEMINI_API_KEY, GEMINI_TTS_MODELS (isteğe bağlı), TTS_ENGINE=sessiz (yerel deneme: süre tahmini, sessizlik)"""
import base64
import difflib
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request

import numpy as np

SR = 48000
MODELLER = os.environ.get("GEMINI_TTS_MODELS",
                          "gemini-3.1-flash-tts-preview,gemini-3.8-flash-lite-tts,gemini-2.5-flash-preview-tts").split(",")
FX = {
    # iç ses: yakın mikrofon, yumuşak, hafif oda yankısı (düşünce gibi)
    "ic": "highpass=f=110,lowpass=f=8500,equalizer=f=220:t=q:w=1:g=2.5,acompressor=threshold=-24dB:ratio=3:attack=6:release=150,"
          "aecho=0.8:0.55:38|67:0.16|0.10",
    # yüksek sesle söylenen: odada, kuru
    "oda": "highpass=f=90,lowpass=f=10500,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120",
}


def _norm(t):
    t = t.replace("İ", "i").replace("I", "ı").lower()
    return re.sub(r"[^a-zçğıöşü0-9 ]+", " ", t).split()


_SON = {"model": None}


def tts(metin, ses):
    key = os.environ["GEMINI_API_KEY"]
    son = None
    sira = [m.strip() for m in MODELLER if m.strip()]
    if _SON["model"] in sira:
        sira.remove(_SON["model"]); sira.insert(0, _SON["model"])
    for model in sira:
        dil = True
        for deneme in range(4):
            sc = {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": ses}}}
            if dil:
                sc["languageCode"] = "tr-TR"
            govde = {"generationConfig": {"responseModalities": ["AUDIO"], "speechConfig": sc},
                     "contents": [{"role": "user", "parts": [{"text": metin}]}]}
            req = urllib.request.Request(
                f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
                data=json.dumps(govde).encode(), headers={"x-goog-api-key": key, "Content-Type": "application/json"})
            try:
                r = json.load(urllib.request.urlopen(req, timeout=180))
                pcm = base64.b64decode(r["candidates"][0]["content"]["parts"][0]["inlineData"]["data"])
                print(f"  {model} · {ses}", flush=True)
                _SON["model"] = model
                return np.frombuffer(pcm, dtype="<i2").astype(np.float32) / 32768
            except urllib.error.HTTPError as e:
                msg = e.read().decode()[:240]
                son = f"{model}: HTTP {e.code} {msg}"
                print("::warning::" + son, flush=True)
                if e.code == 400 and dil and "language" in msg.lower():
                    dil = False
                    continue
                if e.code == 429 and "minute" not in msg.lower() and "per_minute" not in msg.lower():
                    break
                if e.code in (429, 500, 503):
                    time.sleep(20 * (deneme + 1))
                    continue
                break
            except (KeyError, IndexError, TimeoutError, urllib.error.URLError) as e:
                son = f"{model}: {e}"
                print("::warning::" + son, flush=True)
                time.sleep(4)
    raise RuntimeError(son)


def ffmpeg_isle(x24, af, tempo):
    """24 kHz ham ses -> başı/sonu kırpılmış, efektli 48 kHz mono float."""
    trim = ("silenceremove=start_periods=1:start_threshold=-46dB,areverse,"
            "silenceremove=start_periods=1:start_threshold=-46dB,areverse,")
    chain = trim + (f"atempo={tempo}," if abs(tempo - 1) > .005 else "") + af
    raw = (np.clip(x24, -1, 1) * 32767).astype("<i2").tobytes()
    out = subprocess.run(["ffmpeg", "-v", "error", "-f", "s16le", "-ar", "24000", "-ac", "1", "-i", "-", "-af", chain,
                          "-ar", str(SR), "-ac", "1", "-f", "f32le", "-"], input=raw, capture_output=True, check=True).stdout
    return np.frombuffer(out, np.float32).copy()


def yaz(path, x):
    raw = (np.clip(x, -1, 1) * 32767).astype("<i2").tobytes()
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "-", path], input=raw, check=True)


_W = {}


def whisper():
    if "m" not in _W:
        from faster_whisper import WhisperModel
        _W["m"] = WhisperModel(os.environ.get("WHISPER_MODEL", "small"), device="cpu", compute_type="int8")
    return _W["m"]


def dok(x):
    """(döküm metni, [(kelime, bas, bit)]) — x: 48 kHz mono."""
    # 16 kHz diziyi doğrudan ver (PyAV ile dosya açma sürüm uyumsuzluğuna takılmasın)
    raw = (np.clip(x, -1, 1) * 32767).astype("<i2").tobytes()
    a16 = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "-",
                                        "-ar", "16000", "-f", "f32le", "-"], input=raw, capture_output=True, check=True).stdout, np.float32)
    segs, _ = whisper().transcribe(a16, language="tr", beam_size=5, word_timestamps=True)
    kel = []
    for s in segs:
        for w in (s.words or []):
            kel.append((w.word.strip(), float(w.start), float(w.end)))
    return " ".join(k[0] for k in kel), kel


def hizala(metin, x, bas):
    """Satırın kelimelerine saat ver: whisper kelimeleri eşleşirse onun saatleri, eşleşmeyenler aradan paylaştırılır."""
    yazi = metin.split()
    dur = len(x) / SR
    try:
        _, kel = dok(x)
    except Exception as e:  # noqa: BLE001
        print("::warning::whisper yok:", e)
        kel = []
    sn = [" ".join(_norm(w)) for w in yazi]
    hn = [" ".join(_norm(k[0])) for k in kel]
    t = [None] * len(yazi)
    sm = difflib.SequenceMatcher(None, sn, hn, autojunk=False)
    for a, b, n in sm.get_matching_blocks():
        for k in range(n):
            t[a + k] = (kel[b + k][1], kel[b + k][2])
    # boşlukları doldur: harf sayısına göre, komşu bilinen saatler arasında
    L = [max(1, len("".join(_norm(w)))) for w in yazi]
    i = 0
    while i < len(yazi):
        if t[i] is not None:
            i += 1
            continue
        j = i
        while j < len(yazi) and t[j] is None:
            j += 1
        a0 = t[i - 1][1] if i > 0 else 0.0
        b0 = t[j][0] if j < len(yazi) else dur
        tot = sum(L[i:j])
        c = a0
        for k in range(i, j):
            d = (b0 - a0) * L[k] / tot
            t[k] = (c, c + d)
            c += d
        i = j
    return [{"word": w, "start": round(bas + a, 3), "end": round(bas + b, 3)} for w, (a, b) in zip(yazi, t)]


def main(bolum):
    vd = os.path.join(bolum, "voice")
    cfg = json.load(open(os.path.join(vd, "satirlar.json"), encoding="utf-8"))
    os.makedirs(os.path.join(vd, "satir"), exist_ok=True)
    sessiz = os.environ.get("TTS_ENGINE") == "sessiz"
    parcalar, words, lines = [], [], []
    t = 0.25
    for s in cfg["satirlar"]:
        ses = cfg["sesler"][s["kim"]]
        print(f"{s['id']} [{s['kim']}] {s['metin']}", flush=True)
        if sessiz:
            x = np.zeros(int(SR * max(.8, len(s["metin"]) * .075)), np.float32)
        else:
            en_iyi = None
            for deneme in range(3):
                x = ffmpeg_isle(tts(s["metin"], ses["voice"]), FX[ses.get("fx", "oda")], ses.get("tempo", 1.0))
                try:
                    dokum, _ = dok(x)
                    puan = difflib.SequenceMatcher(None, "".join(_norm(s["metin"])), "".join(_norm(dokum))).ratio()
                except Exception:  # noqa: BLE001
                    dokum, puan = "", 1.0
                print(f"  okunuş {puan:.2f}: {dokum}", flush=True)
                if en_iyi is None or puan > en_iyi[0]:
                    en_iyi = (puan, x)
                if puan >= .9:
                    break
                time.sleep(4)
            x = en_iyi[1]
            time.sleep(3)
        yaz(os.path.join(vd, "satir", s["id"] + ".wav"), x)
        t += s.get("ara", .35) if parcalar else 0
        bas = t
        lines.append({"id": s["id"], "kim": s["kim"], "start": round(bas, 3), "end": round(bas + len(x) / SR, 3), "text": s["metin"]})
        for w in hizala(s["metin"], x, bas) if not sessiz else [
                {"word": w, "start": round(bas + i * len(x) / SR / len(s["metin"].split()), 3),
                 "end": round(bas + (i + 1) * len(x) / SR / len(s["metin"].split()), 3)} for i, w in enumerate(s["metin"].split())]:
            w.update({"line": s["id"], "kim": s["kim"]})
            words.append(w)
        parcalar.append((bas, x))
        t = bas + len(x) / SR
    toplam = t + 0.4
    v = np.zeros(int(SR * toplam) + SR, np.float32)
    for bas, x in parcalar:
        i = int(bas * SR)
        v[i:i + len(x)] += x
    v = v[:int(SR * toplam)]
    ham = os.path.join(vd, "ham.wav")
    yaz(ham, v)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", ham, "-af", "loudnorm=I=-16:TP=-1.5:LRA=9", "-ar", str(SR),
                    os.path.join(vd, "voice.wav")], check=True)
    os.remove(ham)
    json.dump({"words": words, "lines": lines, "dur": round(toplam, 3)},
              open(os.path.join(vd, "words.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), "zarf.py"), os.path.join(vd, "voice.wav"),
                    os.path.join(vd, "env.json")], check=True)
    print(f"Toplam {toplam:.1f} sn, {len(words)} kelime, {len(words) / toplam:.2f} kelime/sn")


if __name__ == "__main__":
    main(sys.argv[1])
