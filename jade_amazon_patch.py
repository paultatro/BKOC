#!/usr/bin/env python3
"""
Apply the "Jade Amazon" nickname polish to Bandit Kings of Ancient China.

ONE smooth change, no structural impact, no incongruity risk:
    Rename Hu Sanniang's nickname from "She-devil" to "Jade Amazon".

Context:
    In the Water Margin source novel, Hu Sanniang (扈三娘) is one of the
    few female heroes among the 108 Stars of Destiny. Her traditional
    nickname is 一丈青 (yi zhang qing) — literally "Ten Feet of Jade" —
    evoking her towering stature in green/jade armor as a warrior woman.

    The 1989 KOEI English translation rendered this as "She-devil", both
    inaccurate and demeaning. "Jade Amazon" preserves the warrior-woman
    spirit of the original Chinese while matching the ROM's dramatic
    nickname style (cf. "Blue Face Beast", "Red Maned Demon").

Technical details:
    - ROM offset 0x037454 (PRG bank 13, offset 0x20E4)
    - Fixed 24-byte character slot: 8-byte stat prefix + 16-byte name field
    - "She-devil\\0" (10 bytes) overwritten with "Jade Amazon\\0" (12 bytes)
    - Remaining name-field bytes zero-padded (as original did)
    - No bytes outside the slot are touched
    - File length, iNES header, PRG/CHR banks, all other data unchanged
    - String appears only once in the ROM → no broken cross-references

Usage:
    python3 jade_amazon_patch.py <input_rom.nes> <output_rom.nes>

If called with no arguments it looks for ./bandit_kings_original.nes and
writes ./bandit_kings_jade_amazon.nes.
"""
import sys, hashlib, os

OFFSET        = 0x037454
OLD_NAME      = b"She-devil"
NEW_NAME      = b"Jade Amazon"
NAME_FIELD    = 16  # bytes of name-field space in each 24-byte slot
EXPECTED_SIZE = 393232   # standard iNES: 16 header + 16*16K PRG + 16*8K CHR

def patch(rom: bytearray) -> bytearray:
    if len(rom) != EXPECTED_SIZE:
        raise ValueError(f"Expected {EXPECTED_SIZE}-byte iNES ROM, got {len(rom)}")
    if rom[:4] != b"NES\x1a":
        raise ValueError("Not an iNES ROM (bad magic)")
    if rom[OFFSET:OFFSET+len(OLD_NAME)] != OLD_NAME:
        raise ValueError(
            f"Bytes at 0x{OFFSET:06X} are not {OLD_NAME!r}. "
            f"Is this the right ROM dump? Expected canonical Bandit Kings "
            f"of Ancient China (U)."
        )
    patched = bytearray(rom)
    patched[OFFSET:OFFSET+NAME_FIELD] = NEW_NAME + b"\x00" * (NAME_FIELD - len(NEW_NAME))
    return patched

def main():
    if len(sys.argv) >= 3:
        in_path, out_path = sys.argv[1], sys.argv[2]
    else:
        in_path  = "bandit_kings_original.nes"
        out_path = "bandit_kings_jade_amazon.nes"

    if not os.path.exists(in_path):
        print(f"Input ROM not found: {in_path}", file=sys.stderr)
        sys.exit(1)

    with open(in_path, "rb") as f:
        rom = f.read()
    print(f"Loaded: {in_path} ({len(rom)} bytes, md5={hashlib.md5(rom).hexdigest()})")

    patched = patch(bytearray(rom))
    with open(out_path, "wb") as f:
        f.write(patched)
    print(f"Wrote:  {out_path} ({len(patched)} bytes, md5={hashlib.md5(bytes(patched)).hexdigest()})")
    print(f"Changed 11 bytes at 0x{OFFSET:06X}: {OLD_NAME.decode()!r} -> {NEW_NAME.decode()!r}")

if __name__ == "__main__":
    main()
