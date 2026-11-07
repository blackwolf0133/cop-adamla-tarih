"""Ses modeli karşılaştırması (Kasım 2026): aynı 3 cümle, SENİN SESİNLE, farklı modeller.
Hepsi ticari kullanıma açık lisanslı. Hiçbir şey paylaşmaz, sadece mp3 üretir.
Kullanım: python tools/ses_yeni.py <chatterbox|moss|orkhon|voxcpm|azure> <çıktı_klasörü>"""
import os, sys, subprocess, time, glob
import numpy as np
import soundfile as sf

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine.numbers import seslendirme_metni  # noqa: E402

HAM = ["Dur, kaydırma! Bir zamanlar bir lale soğanı için koca bir ev verdiler. İnanmıyor musun?",
       "Yıl 1636. Hollanda'da herkes lale alıp satıyor. Fiyatlar her gün biraz daha yükseliyor.",
       "Ve Şubat 1637'de bir açık artırmada kimse alıcı çıkmaz. Fiyatlar bir anda çöker!"]
T = [seslendirme_metni(t) for t in HAM]
which, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
ME = "/tmp/ref.wav"
if which != "azure" and not os.path.exists(ME):
    sys.exit("Ses kaydı (/tmp/ref.wav) yok: VOICE_KEY secret'ı gerekli.")
NO = {"chatterbox": "1_simdiki_chatterbox", "moss": "2_moss_tts_nano", "orkhon": "3_orkhon_tts", "voxcpm": "4_voxcpm2", "azure": "5_microsoft"}[which]
t0 = time.time()


def bitir(parcalar, sr, ek=""):
    y = np.concatenate([np.concatenate([np.asarray(p, np.float32).reshape(-1), np.zeros(int(sr * 0.6), np.float32)])
                        for p in parcalar])
    raw = f"/tmp/{NO}{ek}.wav"
    sf.write(raw, y, sr)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af",
                    "highpass=f=70,acompressor=threshold=-18dB:ratio=2.5:attack=5:release=60,loudnorm=I=-16:TP=-1.5:LRA=6",
                    "-ar", "44100", "-b:a", "160k", os.path.join(out, f"{NO}{ek}.mp3")], check=True)
    print(f"hazır: {NO}{ek} ({time.time() - t0:.0f} sn)", flush=True)


def oku(yol):
    a, sr = sf.read(yol, dtype="float32")
    return (a.mean(axis=1) if a.ndim > 1 else a), sr


if which == "chatterbox":
    import torch
    _load = torch.load
    torch.load = lambda *a, **k: _load(*a, **{**k, "map_location": "cpu"})
    from chatterbox.mtl_tts import ChatterboxMultilingualTTS
    m = ChatterboxMultilingualTTS.from_pretrained(device="cpu")
    parts = []
    for i, t in enumerate(T):
        torch.manual_seed(7 + i)
        parts.append(m.generate(t, language_id="tr", audio_prompt_path=ME, exaggeration=0.5, cfg_weight=0.5).squeeze(0).numpy())
    bitir(parts, m.sr)

elif which == "moss":
    # MOSS-TTS-Nano (OpenMOSS, Nisan 2026, Apache-2.0): 0.1B, CPU'da hızlı, Türkçe destekli klon
    for ayar, ek in (({}, ""), ({"--audio-temperature": "1.2"}, "_sakin")):
        parts, sr = [], 48000
        for i, t in enumerate(T):
            wav = f"/tmp/moss_{i}{ek}.wav"
            cmd = [sys.executable, "infer.py", "--device", "cpu", "--prompt-audio-path", ME, "--text", t,
                   "--output-audio-path", wav, "--disable-wetext-processing", "--seed", str(7 + i)]
            for k, v in ayar.items():
                cmd += [k, v]
            subprocess.run(cmd, check=True, cwd="/tmp/moss")
            a, sr = oku(wav)
            parts.append(a)
        bitir(parts, sr, ek)

elif which == "orkhon":
    # Orkhon-TTS (Hasan Can Solakoğlu, Apache-2.0): Türkçe'ye özel eğitilmiş F5-TTS
    from huggingface_hub import hf_hub_download, list_repo_files
    repo = "hcsolakoglu/Orkhon-TTS"
    files = list_repo_files(repo)
    print("dosyalar:", files, flush=True)
    ckpt = sorted([f for f in files if f.endswith((".safetensors", ".pt"))])[-1]
    vocab = [f for f in files if f.endswith("vocab.txt")][0]
    ckpt, vocab = hf_hub_download(repo, ckpt), hf_hub_download(repo, vocab)
    from faster_whisper import WhisperModel
    ref12 = "/tmp/ref12.wav"  # F5 en fazla ~12 sn referans ister
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", ME, "-t", "11", "-ac", "1", "-ar", "24000", ref12], check=True)
    segs, _ = WhisperModel("small", device="cpu", compute_type="int8").transcribe(ref12, language="tr")
    ref_text = " ".join(s.text for s in segs).strip()
    print("kayıt metni:", ref_text, flush=True)
    from f5_tts.api import F5TTS
    son = None
    for model in ("F5TTS_v1_Base", "F5TTS_Base"):
        try:
            tts = F5TTS(model=model, ckpt_file=ckpt, vocab_file=vocab, device="cpu")
            parts = []
            for i, t in enumerate(T):
                wav, sr, _ = tts.infer(ref_file=ref12, ref_text=ref_text, gen_text=t, seed=7 + i, nfe_step=32)
                parts.append(wav)
            bitir(parts, sr)
            break
        except Exception as e:  # noqa: BLE001
            son = e
            print(f"{model} olmadı: {e}", flush=True)
    else:
        raise SystemExit(f"Orkhon çalışmadı: {son}")

elif which == "voxcpm":
    # VoxCPM2 (OpenBMB, Apache-2.0): daha önce denenmişti, aynı cümlelerle kıyas için
    from voxcpm import VoxCPM
    from faster_whisper import WhisperModel
    m = VoxCPM.from_pretrained("openbmb/VoxCPM2", load_denoiser=False, optimize=False)
    segs, _ = WhisperModel("small", device="cpu", compute_type="int8").transcribe(ME, language="tr")
    ref_text = " ".join(s.text for s in segs).strip()
    parts = [m.generate(text=t, cfg_value=2.0, inference_timesteps=10, prompt_wav_path=ME, prompt_text=ref_text,
                        reference_wav_path=ME) for t in T]
    bitir(parts, m.tts_model.sample_rate)

elif which == "azure":
    # Microsoft Azure sinir ağı sesleri. Örnekler için edge-tts (aynı sesler); kalıcı kullanımda resmi Azure anahtarı.
    import asyncio, edge_tts
    SESLER = [("tr-TR-AhmetNeural", "+0%", "ahmet"), ("tr-TR-AhmetNeural", "+10%", "ahmet_hizli"),
              ("tr-TR-EmelNeural", "+0%", "emel"),
              ("en-US-AndrewMultilingualNeural", "+0%", "andrew_cokdilli"),
              ("en-US-BrianMultilingualNeural", "+0%", "brian_cokdilli"),
              ("de-DE-FlorianMultilingualNeural", "+0%", "florian_cokdilli"),
              ("fr-FR-RemyMultilingualNeural", "+0%", "remy_cokdilli"),
              ("en-US-AvaMultilingualNeural", "+0%", "ava_cokdilli_kadin")]

    async def uret(ses, hiz, t, yol):
        await edge_tts.Communicate(t, ses, rate=hiz).save(yol)

    for ses, hiz, ad in SESLER:
        try:
            parts, sr = [], 24000
            for i, t in enumerate(T):
                mp3, wav = f"/tmp/az_{ad}_{i}.mp3", f"/tmp/az_{ad}_{i}.wav"
                asyncio.run(uret(ses, hiz, t, mp3))
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp3, "-ar", "24000", "-ac", "1", wav], check=True)
                a, sr = oku(wav)
                parts.append(a)
            bitir(parts, sr, "_" + ad)
        except Exception as e:  # noqa: BLE001
            print("olmadı:", ses, e, flush=True)

print("toplam", round(time.time() - t0), "sn")
