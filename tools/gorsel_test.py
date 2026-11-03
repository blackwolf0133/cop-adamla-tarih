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

# Not: CLIP 77 jeton sınırı var; sahne + kısa stil, karakterler kısa ve ayırt edici
STYLE = "watercolor storybook illustration, ink outlines, warm autumn colors, soft light"
NEG = ("photo, realistic, 3d, text, letters, watermark, deformed, extra fingers, blurry, "
       "two women, two girls, hat instead of umbrella")
MAN = "a young man (short black hair, mustard scarf, green jacket)"
WOMAN = "a young woman (long brown hair, red beanie, brown coat)"

SCENES = [
    f"rainy evening, {MAN} sitting alone on a park bench, head down, heavy rain, raindrops, wet street lamps",
    "rainy evening, many people with umbrellas walking away down a wet cobblestone street, empty bench, raindrops",
    f"rainy evening, {WOMAN} holding an open umbrella, walking towards the viewer, raindrops, street lamps",
    f"rainy evening, a man and a woman sitting together on a park bench under one open umbrella, {MAN}, {WOMAN}, raindrops",
    f"sunset after rain, a man and a woman walking side by side up a hill, smiling, {MAN}, {WOMAN}, golden light",
]

for i, sc in enumerate(SCENES, 1):
    t = time.time()
    img = pipe(prompt=f"{sc}, {STYLE}", negative_prompt=NEG, num_inference_steps=6, guidance_scale=2.0,
               width=896, height=1024, generator=torch.Generator().manual_seed(1000 + i)).images[0]
    img.save(os.path.join(out, f"{which}_sahne{i}.png"))
    print(f"sahne {i}: {time.time() - t:.0f} sn", flush=True)
print(f"toplam: {time.time() - t0:.0f} sn")
