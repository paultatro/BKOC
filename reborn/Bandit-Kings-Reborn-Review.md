# Review and verification — November 4, 2026

## Source selected

The user confirmed the October 4 **Bandit Kings Reborn** kit as the intended target. It was found in the June 27 Codex project outputs. The separate Lantern Lords NES ROM was not changed. The connected Drive Mesen folder contained emulator assets and the original game, not a newer Reborn script in the folders inspected.

Baseline director SHA-256: `63186AD999B34CF1CC8F6A64130C4BCBB863CF060C97557F2FB7836C21BC3924`.

## Review findings and changes

| Finding | Change in 0.3 |
| --- | --- |
| Most variety came from unexplained losses or rival boosts | Added paid council policies, warning periods, recovery, and goodwill rewards |
| Multiple budget bonuses could exceed the configured monthly limit | Made that setting a hard cap, including policy/relief; tested zero and one-slot budgets |
| A crisis could arrive without an actionable warning | Select a crisis first, resolve no earlier than the next processed month, and show its preparation hint |
| Recovery only triggered at extremely low aggregate pressure | Detect food/troop distress directly and suspend hostile events |
| Repeated events could feel arbitrary and relentless | Per-event cooldown after successful delivery and a recovery month after crises |
| Four short log entries were not a usable chronicle | Added a bounded 128-entry, month-numbered journal with wrapped display and DEMO/DRY/LIVE labeling |
| One-frame drawings were issued every twenty frames | Draw every frame; native emulator test and screenshot inspection confirm the display |
| Fixed rival slots could become player-owned | Added a dynamic, read-only ownership filter and eligible nemesis selection |
| Glitching month values could create phantom turns | Added calendar range checks and stable-value sampling |
| Reset/load retained stale audit and fake-state details | Reset those fields and pending plans together |
| Demo could diverge from the maintained source | Generate it from the director and compare it in regression tests |

## Evidence

`verify-bandit-kings.py`: **68 checks passed**, 34 each under Lua 5.1 and Lua 5.4 using lupa 2.8. Tests execute the Lua source. They cover transactions, affordability/caps, mitigation, warning timing, recovery, repeat spacing, hard budgets, ownership/capture, keyboard edges, zero-based calendar wrap, glitches, reset, dry-run behavior, deterministic random numbers, drawing failures, source/demo parity, and legacy/modern API shapes.

`Mesen-smoke-result.txt`: **passed** in Mesen **0.9.8.0**, using the user's existing game copied into an isolated test directory. The real emulator ran **2,400 frames**, **19 simulated months**, **0 Lua RAM-write calls**, **32,137 text-draw calls**, and **0 text-draw errors**. Provision, patronage, drill, crises and recovery all appear in the retained log. Demo simulation does not verify real game addresses or campaign effects. Screenshot captures at frames 601 and 1201 were inspected for legibility and clipping.

The source was checked against the [legacy Mesen Lua API](https://www.mesen.ca/docs/apireference.html), [keyboard input reference](https://www.mesen.ca/docs/apireference/input.html), and [Mesen 2 Lua API source](https://github.com/SourMesen/Mesen2/blob/master/UI/Debugger/Documentation/LuaDocumentation.json). Actual Mesen 2 execution and physical keyboard interactions were not tested.

## Remaining integration work

The supplied map is still empty. No addresses are presented as verified. This remains a calibration prototype: the demo works immediately, but live changes need verified addresses and ownership semantics for the specific ROM/scenario. Unsigned one-byte access is the only implemented stat encoding; multi-byte, BCD, or compressed values must not be mapped as bytes. Player addresses also need to stay attached to the intended entity as the campaign changes.

The 0.3 ownership guard excludes rows based on provided IDs. It cannot discover those IDs, establish that a row represents an active entity, or infer table order. Neutral/unused owner values must be calibrated. With no ownership map, default rival mutations are blocked.

A full end-to-end commercial-game campaign has not been playtested. No claim is made that the scripts change tactical AI, add personalities/relationships, or implement the complete earlier design bible. Journal history is session-local and restarts on reset/load. Exact save-state/rewind replay remains unsupported.
