# Runbook — version 0.4

## Immediate demo

Load your game in Mesen, then load and run `bandit-kings-reborn-demo.lua` in its Script Window. The panel must say DEMO. P cycles policy; H opens the journal; O hides the overlay. Watch a warning appear, choose the matching preparation, and see the later crisis and recovery. The demo uses fake RAM and does not apply its events to the game.

## Establish a live map

1. Keep a separate copy of your game save and record the exact ROM hash/scenario.
2. Use `bandit-kings-memory-scout.lua` to locate candidates; default scope is internal RAM `$0000–$07FF`. Investigate cartridge RAM `$6000–$7FFF` separately if necessary.
3. Use `bandit-kings-write-trace.lua` for one controlled action and `bandit-kings-address-lab.lua` for repeatable before/after checks.
4. Confirm month encoding and a complete 12-month range. Default range is 1–12; set `month_min=0, month_max=11` for verified 0–11 encoding.
5. Confirm each stat is one unsigned byte and belongs to the intended player entity. Never map only one byte of a wider value.
6. Record values in the address template and calibration worksheet. Keep unknowns nil/zero.
7. Confirm `player_owner` and the matching `enemy_owner_*` table. Configure `neutral_owner_values`. Verify player, rival, neutral, unused and captured rows. Every rival table must share the owner table's entity order.
8. Copy the confirmed map into the director. Start with `dry_run=true`, `nemesis_rivals=false`, and difficulty 1 or 2.
9. Check the script log against expected changes for several month transitions and a captured province. The default ownership guard blocks rival boosts when ownership is unavailable. Do not use the fake demo map.
10. After this evidence is clean, use `dry_run=false` on a disposable campaign copy. Verify each effect in the game itself and record results. Restore your save if the observed values differ from the predictions.

Only run one director at a time. The policy and ordinary event prices are prototype byte-unit tuning and need balancing after the real map is established.

## Session behavior

At startup, the first stable month establishes the baseline and causes no event. A month change must remain stable for `month_stable_frames` frames. Rapid changes during cooldown coalesce to the final observed month; missed turns are not replayed in a burst. Reset/load clears the journal and rebaselines the month. The director is not serialized into save states.

`max_events_per_month` is a hard cap. Recovery takes first priority. An affordable selected policy normally comes next. A due crisis gets priority over a policy if only one slot is available. Unaffordable or capped policies cost nothing. A successfully delivered crisis prevents additional hostile events that month.

For an advanced, verified fixed enemy-only table, `require_enemy_ownership=false` permits rows without ownership mapping. This deliberately removes the default protection and requires manual recalibration when ownership changes. A provided ownership map is still honored.
