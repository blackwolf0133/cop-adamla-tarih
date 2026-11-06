"""VoxCPM2 (Apache-2.0) ve Trendyol-TTS ses denemesi. Kullanım: python tools/voxcpm_test.py <voxcpm|trendyol> <çıktı>"""
import os, sys, subprocess, time
import numpy as np, soundfile as sf
from voxcpm import VoxCPM
from huggingface_hub import hf_hub_download

which, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
T = ["Hayat, kimin gerçekten yanında olduğunu bazen en zor gününde gösterir. Ama biri kalır.",
     "Yıl bin dört yüz elli üç. Bir gecede, gemiler karadan yürüyerek Haliç'e indirildi!"]
ADANA = ["Ula dayı, kırk dört derece olmuş, şu klimayı açak mı gari?",
         "Hee, açmayak da napak! Ama kimseye deme haa, Adanalı sıcaktan korkmaz!"]
ME = "/tmp/ref.wav" if os.path.exists("/tmp/ref.wav") else None
repo = "openbmb/VoxCPM2" if which == "voxcpm" else "Trendyol/Trendyol-TTS"
t0 = time.time()
m = VoxCPM.from_pretrained(repo, load_denoiser=False, optimize=False)
print("yüklendi", round(time.time() - t0), "sn", flush=True)
SR = m.tts_model.sample_rate


def gen(text, **kw):
    t = time.time()
    w = m.generate(text=text, cfg_value=2.0, inference_timesteps=10, **kw)
    print(f"  {len(w)/SR:.1f} sn ses, {time.time()-t:.0f} sn sürdü", flush=True)
    return w


def save(name, chunks):
    y = np.concatenate([np.concatenate([np.asarray(c, np.float32), np.zeros(int(SR * 0.7), np.float32)]) for c in chunks])
    raw = f"/tmp/{name}.wav"
    sf.write(raw, y, SR)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", "highpass=f=60,loudnorm=I=-16:TP=-1.5:LRA=8",
                    "-ar", "44100", "-b:a", "160k", os.path.join(out, name + ".mp3")], check=True)
    print("hazır:", name, flush=True)


def safe(name, fn):
    try:
        save(name, fn())
    except Exception as e:  # noqa: BLE001
        print("HATA", name, e, flush=True)


pre = "40" if which == "voxcpm" else "60"
# 1) Yazıyla tasarlanan sesler
safe(f"{pre}_{which}_tasarim_sicak_erkek", lambda: [gen("(A middle-aged Turkish man, warm deep voice, calm heartfelt storytelling)" + t) for t in T])
safe(f"{pre[0]}1_{which}_tasarim_yumusak_kadin", lambda: [gen("(A young Turkish woman, soft warm voice, gentle and emotional)" + t) for t in T])
safe(f"{pre[0]}2_{which}_tasarim_canli_anlatici", lambda: [gen("(An energetic Turkish male documentary narrator, curious, lively and expressive)" + t) for t in T])
# 2) Hazır ses örneklerinden klon (Bir Satır Hayat male_2, Para Atlası male_1)
for j, v in enumerate(["male_2", "male_1"]):
    ref = hf_hub_download("wite-tech/pocket-tts-turkish", f"voices/{v}.wav")
    safe(f"{pre[0]}{3+j}_{which}_klon_{v}", lambda ref=ref: [gen(t, reference_wav_path=ref) for t in T])
# 3) Senin sesin
if ME:
    safe(f"{pre[0]}5_{which}_klon_senin_sesin", lambda: [gen("(natural, lively tone)" + t, reference_wav_path=ME) for t in T])
    try:
        from faster_whisper import WhisperModel
        segs, _ = WhisperModel("small", device="cpu", compute_type="int8").transcribe(ME, language="tr")
        ref_text = " ".join(s.text for s in segs).strip()
        print("kayıt metni:", ref_text, flush=True)
        safe(f"{pre[0]}6_{which}_tam_klon_senin_sesin",
             lambda: [gen(t, prompt_wav_path=ME, prompt_text=ref_text, reference_wav_path=ME) for t in T])
    except Exception as e:  # noqa: BLE001
        print("tam klon atlandı:", e)
# 4) Adana şivesi denemesi (tasarım)
safe(f"{pre[0]}7_{which}_adana_sivesi", lambda: [
    gen("(A young man from Adana, Turkey, strong southern Turkish dialect, street-smart, fast and funny)" + ADANA[0]),
    gen("(An older heavy man from Adana, Turkey, deep raspy voice, strong southern dialect, humorous)" + ADANA[1])])
print("toplam", round(time.time() - t0), "sn")
