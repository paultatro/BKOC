# What Shuffle Edition changes, and how it was verified

Target ROM: *Bandit Kings of Ancient China (U)*, 393,232 bytes, MD5
`5ef1ba9461974f34b0633eaf063490dd`. iNES mapper 5 (MMC5), battery-backed save, 16×16 KB PRG and 16×8 KB CHR.

## Verified tables

### Character table — the only region the tool writes
- File offset `0x03600C`: 256 slots × 24 bytes.
- Bytes 0–3 are ID/flag bytes and are **never written**. Slot 0 (Gao Qiu) is `ff ff ff ff`.
  108-Star heroes have byte 1 = `00`; other characters have its high bit set.
- Bytes 4–7 are stats. Bytes 4–6 range 0–100 and byte 7 ranges 0–50 across all 256 slots.
  Which stat is which hasn't been confirmed in-game, so the shuffle moves all four bytes as one
  block and never needs to know.
- Bytes 8–23 are the nickname: up to 15 ASCII characters, zero-padded. The US version names
  every character **only** by nickname (story text says "Leopard Headed kills the agents of
  Gao Qiu"), so renaming one is only safe if that string appears nowhere else. The tool
  checks this on every rename.

### Province table — read only
- File offset `0x037808`: 27-byte records, 48 named provinces. Each record holds map grid
  coordinates, screen coordinates, up to 8 neighbors ending in `ff`, a type value from 0 to 7,
  and an 11-character name plus one value byte.
- All neighbor links are two-way, so there are no map bugs to fix. The tool never writes here.

## Fixes (always applied)

| Slot | Was | Now | Why |
|---|---|---|---|
| 216 | She-devil | Jade Amazon | Hu Sanniang's 一丈青 ("Ten Feet of Jade") was translated as a slur |
| 194 | Winged Tiger | Mountain Tiger | Duplicate nickname; slot 64 (108-Star Lei Heng, 插翅虎) keeps it |
| 91 | Like Ren Gui | Rival Ren Gui | Guo Sheng's 賽仁貴 means "Rival of Ren Gui" |
| 112 | Stayed by None | Unstoppable | Mu Hong's 沒遮攔 is usually rendered "Unstoppable" |
| 177 | Heavens Guard | Heaven's Guard | Missing apostrophe |

## Shuffles

- **Stats:** the 253 characters in slots 2–254 are ranked by stat total and split into tiers
  of 16. Stat blocks are permuted within each tier. `--chaos` uses one tier. The set of stat
  blocks is unchanged, so total power in the game stays the same.
  - Gao Qiu (0), Tattooed Priest (1) and Lan (255) are pinned. Slot 1 is the only character
    whose byte 7 is 0, which may be a marker.
- **New generals:** the N weakest slots from the non-Star ID space are renamed. A slot is skipped
  if its nickname appears anywhere else in the ROM or it is a named story figure (Golden Lotus).
  Each new general gets stats sampled from mid-table characters (ranks 30–150).
- **Gao Qiu:** sets his byte 4 to 76 (classic), 95 (stronger) or 55 (weaker). It's his only
  non-zero stat, but its in-game effect is unconfirmed, so this is experimental.

## Checklist to run in Mesen

No headless emulator was available for this build. Please check:

1. The ROM boots to the title screen and a new game starts in each scenario.
2. Play 3–4 turns: move, recruit, and fight one battle with no crash or garbled text.
3. Open a hero's status screen and compare it with the spoiler log. For example, seed 1101
   gives Welcome Rain the stat block (91, 75, 84, 17). Note which on-screen stats those numbers
   are; that tells us which byte is which.
4. Find a renamed character (Jade Amazon, Unstoppable) and a new general in a province list.
5. Save to the battery, reload, and check that the names and stats persist.

## Next steps (not yet done)

- **Starting provinces and province economy:** not in either table above. To find them: start a
  new game in Mesen, open Debug → Memory Tools, search RAM/SRAM for one province's displayed
  gold or food value, and note the address. With that address, the ROM table that initializes
  it can be traced, and the shuffle can then be added safely.
- **Stat labels:** step 3 of the checklist will name bytes 4–7. That would allow per-stat
  shuffles and a properly understood Gao Qiu preset.
