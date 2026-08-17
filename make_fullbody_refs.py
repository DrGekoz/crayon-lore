#!/usr/bin/env python3
"""Generate full-body plain-background character refs for the 5 original
Crayon Diet bots using Codex (GPT Image 2), matching the newer _single.png
refs (darrel_single.png, margaret_single.png). Uses each original bot image
as an identity ref.

Replicates the pipeline's Codex.generate_image pattern (per-call CODEX_HOME
isolation, temp-file payload, -i refs, deterministic "Saved at:" claim).
"""
import glob
import os
import re
import shutil
import subprocess
import tempfile
import uuid
from pathlib import Path

CAST_DIR = Path(r"F:\aaaaaVIBECODING\Crayon Lore\cast_refs\crayon_diet")

# (canonical label, source bot image, output filename)
CHARACTERS = [
    ("Duck Pope", "duck_pope.png", "duck_pope_single.png"),
    ("Broccolini Biceps", "broccolini_biceps.png", "broccolini_biceps_single.png"),
    ("Big Tony", "big_tony.png", "big_tony_single.png"),
    ("Bro-Tech", "bro_tech.png", "bro_tech_single.png"),
    ("Skibidi Sarah", "skibidi_sarah.png", "skibidi_sarah_single.png"),
]

HEADER = (
    "Use the attached reference image ONLY for the character's identity and "
    "appearance - keep their exact face, build, outfit, colours and design. "
    "Render them as a full-body character reference portrait:"
)
BODY = (
    "standing facing the camera, entire body head to feet, both feet on the "
    "ground, arms relaxed at sides, neutral expression, centered composition. "
    "EXACTLY ONE single character, absolutely no duplicate, no mirror image, "
    "no second figure, no multi-panel grid, no side-by-side thumbnails. "
    "Plain light grey studio background, flat even neutral lighting. "
    "Character reference portrait. Polished stylized 3D animated game-asset "
    "quality digital painting, clean, cinematic."
)

user_home = Path.home() / ".codex"


def _ps_quote(p: str) -> str:
    return "'" + p.replace("'", "''") + "'"


def _scan(generated: Path) -> dict:
    m = {}
    for p in (glob.glob(str(generated / "**" / "call_*.png"), recursive=True)
              + glob.glob(str(generated / "**" / "ig_*.png"), recursive=True)):
        m[os.path.abspath(p)] = os.path.getmtime(p)
    for d in glob.glob(str(generated / "*")):
        if os.path.isdir(d):
            m["dir:" + os.path.abspath(d)] = 0
    return m


def generate_one(label: str, ref: Path, out_path: Path) -> bool:
    prompt = f"{HEADER} {label}. {BODY}"
    _home = Path(tempfile.gettempdir()) / f"codex_home_{uuid.uuid4().hex[:12]}"
    _home.mkdir(parents=True, exist_ok=True)
    for _f in ("auth.json", "config.toml"):
        _src = user_home / _f
        if _src.is_file():
            try:
                shutil.copy2(_src, _home / _f)
            except Exception:
                pass
    env = dict(os.environ)
    env["CODEX_HOME"] = str(_home)
    generated = _home / "generated_images"
    generated.mkdir(parents=True, exist_ok=True)
    before = _scan(generated)

    tmp = os.path.join(tempfile.gettempdir(), f"codex_payload_{uuid.uuid4().hex[:8]}.txt")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write("/imagegen " + prompt)

    ref_args = f" -i {_ps_quote(os.path.abspath(ref))}"
    ps_cmd = (f"Get-Content -Raw '{tmp}' | codex exec --skip-git-repo-check "
              f"{ref_args}")
    cmd = ["powershell.exe", "-NoProfile", "-Command", ps_cmd]
    print(f"[CODEX] {label} -> {out_path.name} (ref: {ref.name})...")
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=900, env=env)
    except subprocess.TimeoutExpired:
        print(f"  [CODEX] {label}: TIMEOUT")
        shutil.rmtree(_home, ignore_errors=True)
        return False
    finally:
        try:
            os.remove(tmp)
        except Exception:
            pass

    out_text = (proc.stdout or "") + "\n" + (proc.stderr or "")
    out_text = re.sub(r"\x1b\[[0-9;]*[A-Za-z]", "", out_text)

    src = None
    m = re.search(
        r"(?:Saved\s+(?:at|to)|\b(?:image|output)\s+(?:written|saved)\s+(?:to|at))\s*[:=]?\s*"
        r"[`'\"\u2018\u2019\u201c\u201d]?\s*"
        r"([A-Za-z]:[^`'\"\u2018\u2019\u201c\u201d\r\n]+?\.(?:png|jpg|jpeg|webp))",
        out_text, re.IGNORECASE)
    if m:
        src = m.group(1)
        if not os.path.isfile(src):
            src = None
    if src is None:
        # fallback: newest unclaimed call_*.png/ig_*.png in the isolated dir
        after = _scan(generated)
        new_files = [k for k in after if not k.startswith("dir:")
                     and k not in before]
        if new_files:
            new_files.sort(key=lambda k: after[k], reverse=True)
            src = new_files[0]
    if src is None:
        print(f"  [CODEX] {label}: no output image found")
        shutil.rmtree(_home, ignore_errors=True)
        return False

    shutil.copyfile(src, str(out_path))
    print(f"  [CODEX] {label}: wrote {out_path} ({os.path.getsize(out_path)} bytes)")
    shutil.rmtree(_home, ignore_errors=True)
    return True


def main() -> None:
    CAST_DIR.mkdir(parents=True, exist_ok=True)
    ok = 0
    for label, ref_name, out_name in CHARACTERS:
        ref = CAST_DIR / ref_name
        out = CAST_DIR / out_name
        if not ref.is_file():
            print(f"[SKIP] {label}: missing source ref {ref_name}")
            continue
        if generate_one(label, ref, out):
            ok += 1
    print(f"\nDONE: {ok}/{len(CHARACTERS)} full-body refs generated.")


if __name__ == "__main__":
    main()
