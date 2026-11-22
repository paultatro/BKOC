# Bandit Kings Reborn 0.4 — start here

Two mods for *Bandit Kings of Ancient China* (NES) that work together in Mesen:

| Part | What it is | Changes the ROM? | Works today? |
|---|---|---|---|
| **Shuffle Edition** (`bkoc_shuffle.py`, `bkoc/`) | Builds a new ROM with nickname fixes, shuffled character stats and new generals | Yes, makes a new copy | Yes |
| **Campaign Director** (`reborn/`) | A Lua overlay with policies, warned crises, recovery months and a chronicle | No | Demo yes; live mode needs RAM calibration |

They're independent. You can play a shuffled ROM, run the director on top of it, or both.

## 1. Make a shuffled ROM
Follow [BEGINNER_GUIDE.md](BEGINNER_GUIDE.md), or run:

```
python bkoc_shuffle.py "Bandit Kings of Ancient China (U).nes" my_game.nes --seed 42
```

You need the untouched US ROM (393,232 bytes). Every build writes a spoiler log next to the new ROM.

## 2. Try the director
1. Open the game (original or shuffled) in Mesen.
2. Choose Debug → Script Window, open `reborn/bandit-kings-reborn-demo.lua`, and click Run.
3. **Click back on the game window.** While the Script Window has focus, Mesen sends no buttons
   to the game, so the controller seems dead.
4. **P** cycles policy, **H** shows the history, and **O** hides the panel. The demo uses fake values and says **DEMO**.

Full details are in `reborn/START-HERE-Bandit-Kings-Reborn.md`. For live mode, see `reborn/Bandit-Kings-Reborn-Runbook.md`.

## If the controls don't respond
See the troubleshooting section in `reborn/Bandit-Kings-Reborn-Troubleshooting.md`.
