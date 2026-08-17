# Crayon Lore - pre-generate YOUNG ref images from the original cast images.
# Uses the codex backend (GPT Image 2) with the adult cast PNG attached as an
# identity/style ref so the de-aged version matches the same character.
# Joe 2026-08-16.
import os, sys, traceback

os.environ["IMAGE_BACKEND"] = "codex"
os.environ["IMAGE_MODEL"] = "gpt-image-2"

BASE = r"F:\aaaaaVIBECODING\Crayon Lore\cast_refs\crayon_diet"

# name -> (adult ref, out file, prompt)
JOBS = [
    ("tonio", "big_tony.png", "tonio.png",
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
     "no mirror image, no second figure."),
    ("duck_young", "duck_pope.png", "duck_young.png",
     "The exact same character as the reference image, but as a young, small, "
     "ordinary Peking duck. Keep the same duck's face, colouring and warm wise "
     "eyes, but young and youthful: a smaller, softer, bright-eyed young duck, just "
     "before it became the Duck Pope. Full body standing facing the camera, both "
     "feet on the ground, neutral expression. EXACTLY ONE single duck, absolutely "
     "no duplicate, no mirror image, no second figure. Plain light grey studio "
     "background, flat even neutral lighting. character reference portrait."),
    ("bro_tech_young", "bro_tech.png", "bro_tech_young.png",
     "The exact same character as the reference image, but as a young KID in a "
     "dead-end town. Keep his exact face, energy and hustler look, but de-aged into "
     "a teenage boy: youthful face, a cheap hoodie, sly ambitious grin, phone in "
     "one hand. Full body standing facing the camera, entire body head to feet, "
     "both feet on the ground, arms relaxed at sides, neutral expression. EXACTLY "
     "ONE single person, absolutely no duplicate, no mirror image, no second "
     "figure. Plain light grey studio background, flat even neutral lighting. "
     "character reference portrait."),
]

sys.path.insert(0, r"F:\aaaaaVIBECODING\Crayon Lore")
import providers

def main():
    for name, ref, out, prompt in JOBS:
        ref_path = os.path.join(BASE, ref)
        out_path = os.path.join(BASE, out)
        print(f"\n=== {name}: ref={ref_path} -> {out_path} ===")
        if not os.path.isfile(ref_path):
            print(f"  SKIP: ref missing {ref_path}")
            continue
        try:
            ok = providers.generate_image(
                prompt, seed=20260816 + sum(ord(c) for c in name),
                out_path=out_path, backend="codex", model="gpt-image-2",
                ref_images=[ref_path], upscale=False)
            sz = os.path.getsize(out_path) if os.path.isfile(out_path) else 0
            print(f"  {'OK' if ok and sz > 1000 else 'FAIL'} -> {out_path} ({sz//1024}KB)")
        except Exception:
            traceback.print_exc()

if __name__ == "__main__":
    main()
