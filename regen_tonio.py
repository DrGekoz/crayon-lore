# Regenerate Tonio as a young anthropomorphic MOZZARELLA BALL (matches the
# adult big_tony ref form) - NOT a human. Joe 2026-08-16.
import os, sys, traceback
os.environ["IMAGE_BACKEND"] = "codex"
os.environ["IMAGE_MODEL"] = "gpt-image-2"
sys.path.insert(0, r"F:\aaaaaVIBECODING\Crayon Lore")
import providers

BASE = r"F:\aaaaaVIBECODING\Crayon Lore\cast_refs\crayon_diet"
ref = os.path.join(BASE, "big_tony.png")
out = os.path.join(BASE, "tonio.png")

prompt = (
    "The exact same character as the reference image, but as a YOUNG, small "
    "mozzarella ball. He is NOT a human and NOT a humanoid: he is a round, plump, "
    "glossy sphere of soft creamy-white fresh mozzarella cheese, with a smooth "
    "slightly porous rind, two big expressive dark eyes, a loud confident proud "
    "young don-in-training expression, and short thick little cheese arms and "
    "hands. Keep the identical mozzarella-ball body form, creamy white cheese "
    "texture, and retro food-mascot style from the reference, just de-aged and "
    "youthful: smaller, softer, rounder, brighter, no grey. Full body standing, "
    "plain light grey studio background, flat even neutral lighting. character "
    "reference portrait. EXACTLY ONE single character, absolutely no duplicate, "
    "no mirror image, no second figure."
)

try:
    ok = providers.generate_image(prompt, seed=20260816 + sum(ord(c) for c in "tonio"),
                                  out_path=out, backend="codex", model="gpt-image-2",
                                  ref_images=[ref], upscale=False)
    sz = os.path.getsize(out) if os.path.isfile(out) else 0
    print(f"tonio {'OK' if ok and sz > 1000 else 'FAIL'} -> {out} ({sz//1024}KB)")
    if sz > 1000:
        from PIL import Image
        im = Image.open(out); im.load()
        print("size:", im.size)
except Exception:
    traceback.print_exc()
