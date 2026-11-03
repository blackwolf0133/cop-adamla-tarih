"""Görsel testi 2: stable-diffusion.cpp ile Apache-2.0 modeller (CPU).
Kullanım: python tools/gorsel_test2.py <zimage|klein> <sd-cli yolu> <çıktı>
- zimage: Tongyi-MAI Z-Image-Turbo (GGUF) + Qwen3-4B-Instruct-2507 + FLUX.1 VAE
- klein:  FLUX.2-klein-4B (GGUF) + Qwen3-4B + FLUX.2 VAE"""
import os, re, sys, time, subprocess
from huggingface_hub import list_repo_files, hf_hub_download

which, sd, out = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(out, exist_ok=True)

SPECS = {
    "zimage": {
        "diffusion": [("leejet/Z-Image-Turbo-GGUF", r"Q4_K\.gguf$|Q4_0\.gguf$")],
        "llm": [("unsloth/Qwen3-4B-Instruct-2507-GGUF", r"Q4_K_M\.gguf$")],
        "vae": [("Comfy-Org/z_image_turbo", r"vae/.*\.safetensors$"),
                ("black-forest-labs/FLUX.1-schnell", r"^ae\.safetensors$")],
        "steps": 8,
    },
    "klein": {
        "diffusion": [("leejet/FLUX.2-klein-4B-GGUF", r"Q4_K\.gguf$|Q4_0\.gguf$|Q8_0\.gguf$")],
        "llm": [("unsloth/Qwen3-4B-GGUF", r"Q4_K_M\.gguf$")],
        "vae": [("Comfy-Org/flux2-klein-4B", r"vae/.*\.safetensors$"),
                ("black-forest-labs/FLUX.2-klein-4B", r"^vae/.*\.safetensors$"),
                ("Comfy-Org/flux2-dev", r"vae/.*\.safetensors$")],
        "steps": 4,
    },
}


def fetch(cands):
    for repo, pat in cands:
        try:
            files = list_repo_files(repo)
        except Exception as e:  # noqa: BLE001
            print(f"  {repo}: erişilemedi ({e.__class__.__name__})")
            continue
        hits = sorted(f for f in files if re.search(pat, f))
        if hits:
            print(f"  {repo}: {hits[0]}")
            return hf_hub_download(repo, hits[0])
        print(f"  {repo}: eşleşme yok. Dosyalar: {files[:40]}")
    raise SystemExit("model bulunamadı")


spec = SPECS[which]
paths = {k: fetch(spec[k]) for k in ("diffusion", "llm", "vae")}

STYLE = ("Children's storybook illustration, hand-drawn watercolor and colored pencil with fine ink outlines, "
         "warm cozy autumn palette, soft golden light, textured cream paper, gentle and heartfelt mood. No text.")
MAN = "a young man with short black hair, wearing a mustard yellow scarf and an olive green jacket"
WOMAN = "a young woman with long brown hair, wearing a red knitted beanie and a brown wool coat"
SCENES = [
    f"On a rainy evening, {MAN} sits alone on a wooden park bench with his head down, looking sad. Heavy rain falls, "
    "puddles on the ground, glowing street lamps behind him.",
    "A rainy cobblestone street at dusk. Many people holding umbrellas walk away from the viewer into the distance. "
    "In the foreground stands an empty wooden bench, wet from the rain.",
    f"On a rainy street, {WOMAN} walks toward the viewer holding a large open umbrella above her head. "
    "She has a kind, caring expression. Raindrops fall around her, warm street lamps glow.",
    f"Under the rain, two people sit side by side on a wooden park bench sharing one open umbrella: on the left {MAN}, "
    f"on the right {WOMAN}. They sit quietly, her head resting on his shoulder.",
    f"After the rain at sunset, two people walk side by side up a grassy hill, seen from behind: {MAN} and {WOMAN}. "
    "The clouds are clearing, golden light, autumn trees.",
]

t0 = time.time()
for i, sc in enumerate(SCENES, 1):
    t = time.time()
    dst = os.path.join(out, f"{which}_sahne{i}.png")
    cmd = [sd, "--diffusion-model", paths["diffusion"], "--llm", paths["llm"], "--vae", paths["vae"],
           "-p", f"{sc} {STYLE}", "--cfg-scale", "1.0", "--steps", str(spec["steps"]),
           "--sampling-method", "euler", "-W", "832", "-H", "960", "-s", str(100 + i),
           "-t", str(os.cpu_count() or 4), "-o", dst]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0 or not os.path.exists(dst):
        print(r.stdout[-3000:], r.stderr[-3000:])
        raise SystemExit(f"sahne {i} başarısız")
    print(f"sahne {i}: {time.time() - t:.0f} sn", flush=True)
print(f"toplam: {time.time() - t0:.0f} sn")
