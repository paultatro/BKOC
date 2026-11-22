#!/usr/bin/env python3
"""Package Bandit Kings Reborn as a zip (scripts + docs + ROM shuffler, never a ROM).

    python3 make_kit.py            -> dist/Bandit-Kings-Reborn-<VERSION>-Kit.zip
"""
import hashlib
import sys
import zipfile
from pathlib import Path

VERSION = "0.4"
ROOT = Path(__file__).resolve().parent
TOP = ["START-HERE.md", "README.md", "BEGINNER_GUIDE.md", "bkoc_shuffle.py"]
TREES = ["bkoc", "reborn", "docs", "tests"]
FORBIDDEN_SUFFIXES = {".nes", ".sav", ".mst", ".rgd", ".fds", ".zip"}
SKIP_PARTS = {"__pycache__"}


def kit_files():
    files = [ROOT / f for f in TOP]
    for tree in TREES:
        files += sorted(p for p in (ROOT / tree).rglob("*")
                        if p.is_file() and not SKIP_PARTS & set(p.parts)
                        and not p.name.endswith(".spoiler.txt"))
    for p in files:
        if not p.exists():
            sys.exit(f"missing kit file: {p.relative_to(ROOT)}")
        if p.suffix.lower() in FORBIDDEN_SUFFIXES:
            sys.exit(f"refusing to package game/emulator data: {p.relative_to(ROOT)}")
    return files


def main():
    name = f"Bandit-Kings-Reborn-{VERSION}-Kit"
    out = ROOT / "dist" / f"{name}.zip"
    out.parent.mkdir(exist_ok=True)
    rows = []
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for p in kit_files():
            rel = p.relative_to(ROOT).as_posix()
            data = p.read_bytes()
            rows.append(f"| `{rel}` | `{hashlib.sha256(data).hexdigest()}` |")
            z.writestr(f"{name}/{rel}", data)
        z.writestr(f"{name}/CHECKSUMS.md",
                   f"# SHA-256 checksums — {VERSION}\n\n| File | SHA-256 |\n| --- | --- |\n"
                   + "\n".join(rows) + "\n")
    print(f"wrote {out.relative_to(ROOT)} ({len(rows)} files, "
          f"sha256 {hashlib.sha256(out.read_bytes()).hexdigest()})")


if __name__ == "__main__":
    main()
