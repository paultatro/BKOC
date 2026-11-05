# Jade Amazon Patch — the one smooth change

## What it does

Renames one of the 108 heroes from "**She-devil**" to "**Jade Amazon**".

That's it. One change. Eleven bytes.

## Why this one

The ROM you asked me to review turned out to be identical to the clean
canonical 2023 dump (MD5 `5ef1ba9461974f34b0633eaf063490dd`) — so there
was nothing to "fix" from a previous redesign. Just a clean slate for
one tasteful improvement.

**The pick:** Hu Sanniang (扈三娘), one of the very few female heroes in
Water Margin / 108 Stars of Destiny. Her classical Chinese nickname is
一丈青 — literally *"Ten Feet of Jade,"* evoking a towering warrior
woman in green armor. KOEI's 1989 translators rendered it as
"She-devil" — both inaccurate and demeaning. "Jade Amazon" keeps the
warrior-woman spirit, matches the ROM's dramatic nickname style
("Blue Face Beast," "Red Maned Demon," "Jade Chin Li"), and is a real
step up every time she appears in menus and battle text.

## Why it can't break anything

| Concern | Status |
|---|---|
| File length changed? | No — 393,232 bytes before and after |
| iNES header touched? | No |
| Pointers/addresses shifted? | No — all bytes before 0x037454 and after 0x03745E are byte-identical to pristine |
| Cross-references broken? | No — "She-devil" appears exactly once in the entire ROM |
| Cascade damage? | No — change confined to a single 11-byte run inside the character's own 24-byte slot |

The character data table uses fixed-width 24-byte slots (8-byte stat
prefix + 16-byte name field). The old name "She-devil\\0" used 10 of those
16 bytes; the new name "Jade Amazon\\0" uses 12. The remaining 4 bytes
stay as zero padding, exactly as the ROM already stored them.

## How to apply

If you have the standard USA ROM (393,232 bytes, MD5
`5ef1ba9461974f34b0633eaf063490dd`):

```bash
python3 jade_amazon_patch.py <your_rom.nes> bandit_kings_jade_amazon.nes
```

Load `bandit_kings_jade_amazon.nes` in Mesen and recruit her.

## Technical diff

```
Offset 0x037454, 11 bytes changed:
  BEFORE: 53 68 65 2d 64 65 76 69 6c 00 00   "She-devil\0\0"
  AFTER:  4a 61 64 65 20 41 6d 61 7a 6f 6e   "Jade Amazon"

Slot @ 0x03744C (24 bytes):
  BEFORE: 8b 89 03 80 0f 46 0b 06 | She-devil.......
  AFTER:  8b 89 03 80 0f 46 0b 06 | Jade Amazon.....
          (stat prefix untouched) | (new 16-byte name field)
```
