"""Görsel testi (yeni duygusal kanal): açık lisanslı modelle 5 sahne çizer.
Kullanım: python tools/gorsel_test.py <vega|sdxl> <çıktı_klasörü>
- vega: segmind/Segmind-Vega + segmind/Segmind-VegaRT (Apache-2.0)
- sdxl: stabilityai/stable-diffusion-xl-base-1.0 + latent-consistency/lcm-lora-sdxl (OpenRAIL++-M)"""
import os, sys, time
import torch
from diffusers import AutoPipelineForText2Image, LCMScheduler

which, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
torch.set_num_threads(os.cpu_count() or 4)

MODELS = {
    "vega": ("segmind/Segmind-Vega", "segmind/Segmind-VegaRT"),
    "sdxl": ("stabilityai/stable-diffusion-xl-base-1.0", "latent-consistency/lcm-lora-sdxl"),
}
base, lora = MODELS[which]
t0 = time.time()
pipe = AutoPipelineForText2Image.from_pretrained(base, torch_dtype=torch.float32, variant="fp16", use_safetensors=True)
pipe.scheduler = LCMScheduler.from_config(pipe.scheduler.config)
pipe.load_lora_weights(lora)
pipe.fuse_lora()
pipe.set_progress_bar_config(disable=True)
print(f"model yüklendi: {time.time() - t0:.0f} sn")

STYLE = ("storybook illustration, watercolor and colored pencil, hand-drawn ink outlines, warm cozy autumn colors, "
         "soft golden light, cream paper texture, children's picture book art, gentle, highly detailed")
NEG = "photo, photorealistic, 3d render, text, letters, words, watermark, signature, ugly, deformed, extra fingers, blurry, lowres"
MAN = "a young man with short dark hair wearing a mustard yellow scarf and an olive green jacket"
WOMAN = "a young woman with long brown hair wearing a red knitted beanie and a brown coat"

SCENES = [
    f"{MAN} sitting alone on a wooden park bench in the rain at dusk, head down, sad, wet autumn street, glowing street lamps",
    "a crowd of people with umbrellas walking away down a rainy cobblestone street at dusk, an empty wooden bench in the foreground, lonely",
    f"{WOMAN} walking towards the viewer holding a big umbrella on a rainy cobblestone street, warm street lamps, kind caring face",
    f"{WOMAN} and {MAN} sitting side by side on a wooden park bench under one umbrella in the rain, quiet comfort, autumn leaves, street lamps",
    f"{MAN} and {WOMAN} walking together up a grassy hill at sunset, smiling, autumn trees, golden warm light, clouds clearing",
]

for i, sc in enumerate(SCENES, 1):
    t = time.time()
    img = pipe(prompt=f"{sc}, {STYLE}", negative_prompt=NEG, num_inference_steps=6, guidance_scale=1.5,
               width=896, height=1024, generator=torch.Generator().manual_seed(1000 + i)).images[0]
    img.save(os.path.join(out, f"{which}_sahne{i}.png"))
    print(f"sahne {i}: {time.time() - t:.0f} sn", flush=True)
print(f"toplam: {time.time() - t0:.0f} sn")
