# Bandit Kings of Ancient China — Shuffle Edition

A seeded randomizer and fix pack for the NES game *Bandit Kings of Ancient China* (KOEI, 1990).
It only edits data tables that have been verified in the ROM, writes every change in place, and
never shifts a byte. See [docs/CHANGES.md](docs/CHANGES.md) for exactly what is changed and why.

This repository is also **Bandit Kings Reborn 0.4**: the ROM shuffler here plus the Reborn
campaign-director Lua overlay for Mesen in [`reborn/`](reborn/). Start with [START-HERE.md](START-HERE.md).
To build the kit zip, run `python3 make_kit.py`.

New to this? Read [BEGINNER_GUIDE.md](BEGINNER_GUIDE.md).

## What it does

| Feature | Default | Notes |
|---|---|---|
| Nickname fixes | always | "She-devil" → "Jade Amazon", duplicate "Winged Tiger" fixed, three translation fixes |
| Stat shuffle | on | Swaps whole stat blocks between characters of similar power (tiers of 16) |
| Chaos stat shuffle | `--chaos` | Swaps stat blocks across everyone, so any character can be a powerhouse |
| New generals | 8 | Replaces the weakest non-story filler characters with new named generals that have mid-level stats |
| Gao Qiu power | `classic` | `--gaoqiu stronger` / `weaker` (experimental: the effect hasn't been confirmed in-game) |

Never touched: the map, province connections, story text, ID/flag bytes, Gao Qiu's and Lan's
identities, and named story characters.

## Usage

Requires Python 3.8+ (standard library only) and the canonical ROM
`Bandit Kings of Ancient China (U).nes` (393,232 bytes, MD5 `5ef1ba9461974f34b0633eaf063490dd`).

```bash
python3 bkoc_shuffle.py "Bandit Kings of Ancient China (U).nes" my_game.nes --seed 1101
python3 bkoc_shuffle.py rom.nes chaos.nes --chaos --new-generals 20 --gaoqiu stronger
python3 bkoc_shuffle.py rom.nes fixes_only.nes --no-stats --new-generals 0
```

Each build also writes `<output>.spoiler.txt`, which lists every change. The same seed and
options always produce the same ROM.

## Tests

```bash
BKOC_ROM="Bandit Kings of Ancient China (U).nes" python3 -m unittest discover tests
```

## Not done yet

Shuffling starting provinces and province gold/food/troops needs the scenario setup tables.
They aren't in the character or province tables, and finding them safely needs an
emulator's RAM search. See "Next steps" in docs/CHANGES.md.

ROMs are not included or committed; bring your own legally owned copy.
