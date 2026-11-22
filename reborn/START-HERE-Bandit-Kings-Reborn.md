# Bandit Kings Reborn 0.3 — Council and Chronicle

November 4, 2026. An improved Mesen Lua director for Bandit Kings of Ancient China.

**Try the demo now. Live campaign effects still need a verified memory map.**

This release adds paid policies, advance crisis warnings, recovery months, rewards for trusted rule, and a readable session chronicle. It improves the October 4 kit; it is not a new ROM or a complete remake.

## Try it

1. Open your game in Mesen.
2. Open the Script Window, load `bandit-kings-reborn-demo.lua`, and run it.
3. Return focus to the game window. Press **P** to cycle policy, **H** to show history, and **O** to hide/show the panel.

The demo runs one simulated month every 120 emulated frames (about two seconds at normal NTSC speed). All director effects use fake values. The original game continues normally underneath it. The overlay explicitly says **DEMO**.

Only run one director/demo script at a time. The director reads keyboard keys without consuming them; rebind P/H/O in its CONFIG if those keys already control your game or emulator. You can also set `policy` in CONFIG if keyboard input is unavailable.

## Choices

| Policy | Monthly exchange | Extra effect |
| --- | --- | --- |
| Balanced | No cost | Preserve resources |
| Provision | 6 gold for up to 10 food | Halves the warned famine loss, rounded down, minimum 1 |
| Patronage | 8 food for up to 4 popularity | Reduces warned unrest loss from 2 to 1 |
| Drill | 5 gold for up to 4 training | Invest in troop training |

Policies stay selected until changed and resolve at the next observed month. Payment occurs only with a complete map, sufficient funds and a positive benefit. Food from provision is capped at 220; popularity and training at 100. Values already above these caps are preserved and no fee is charged. These are raw byte units in the prototype, not verified displayed resource amounts in the commercial game.

## What improved

- Crises are announced at least one processed month before they can strike. Prepare through normal play or a paid policy.
- A crisis month has no additional hostile director events, and the following month is a recovery month.
- Low food or troop values trigger recovery: hostile events stop and small relief benefits become available.
- Ordinary successful events cannot repeat in consecutive months by default.
- The monthly event limit is a hard cap, including policy and recovery events.
- The journal retains 128 entries, labels them DEMO/DRY/LIVE, and shows the newest entries with H. The script log receives every entry.
- The overlay is compact and drawn every frame instead of briefly appearing once every twenty frames.
- Rival boosts check current ownership on each affected row when mapped; the default blocks rival boosts without ownership data.

## Use with a real campaign

Use `bandit-kings-reborn-director.lua`, initially in its default **DRY RUN** mode. Its map intentionally contains no guessed addresses. Follow `Bandit-Kings-Reborn-Runbook.md` to verify month, stats, ownership, and table ordering before enabling writes. The demo's fake addresses are not the game's addresses.

The kit does not yet provide verified live campaign integration, officer personalities, tactical AI changes, or a ROM patch. Journal and director history restart after reset/load; they are not embedded in save states. A complete campaign balance test has not been performed.

## Verification

68 regression checks passed under Lua 5.1 and Lua 5.4. Mesen 0.9.8 ran the demo with the user's game for 2,400 frames / 19 simulated months with zero Lua RAM-write calls and zero text-drawing errors. Captured screens were visually inspected. Mesen 2 API shapes are covered by mocks; a Mesen 2 executable was not tested.

See `Bandit-Kings-Reborn-Review.md` for findings, evidence, and remaining work.
