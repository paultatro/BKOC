# Release 0.4 — Reborn merged with Shuffle Edition

Released November 22, 2026. Built on 0.3, which was imported unchanged and matched its own SHA-256 list.

## New in 0.4
- One kit: the Lua director (this folder) now ships with the Shuffle Edition ROM builder (`bkoc_shuffle.py`). See `START-HERE.md` at the top of the kit.
- Fix: a warned crisis that could not change anything, such as unrest at popularity 0, used up the only monthly slot. With `max_events_per_month = 1` the paid policy then never ran again. The policy now uses the slot whenever the crisis delivers nothing.
- Fix: a mapped rival-ownership table was ignored unless `player_owner` was also mapped. With `require_enemy_ownership = false`, neutral rows could then be boosted. A mapped owner table is now always honored, and the player check is added when `player_owner` is mapped.
- Fix: Memory Scout, Write Trace and Address Lab drew their panel only one frame in ten, so it flickered or barely showed. They now draw every frame and re-rank only every tenth frame. The Scout panel is taller, so its fourth row is no longer clipped.
- The test suite has 74 checks under Lua 5.1 and 5.4 (68 before, plus 3 regression checks run under both versions). Each new check fails on the 0.3 code.
- `CHECKSUMS.md` is now generated for the whole kit by `make_kit.py`. The 0.3 checksum list and manifest were removed.

## Unchanged limits
The live RAM map is still empty, so live mode needs calibration (see the Runbook). Mesen 2 support is tested only through API mocks, and full campaign balance hasn't been tested.

# Release 0.3 — Council and Chronicle

Released November 4, 2026, from the October 4 Bandit Kings Reborn maintenance build.

The director now offers preparation and recovery alongside pressure. P cycles Balanced, Provision, Patronage and Drill. H toggles the readable journal; O toggles the overlay. Each paid policy resolves once per processed month, checks its complete exchange first, and reports the actual benefit.

Crises are selected and announced before they can resolve in a later month. Paid provision and patronage mitigate the matching warned crisis. A crisis suppresses additional hostile events that month and allows a subsequent recovery month. Low food/troops also suspend hostile pressure. Popularity of at least 65 can attract food donations when stores are below 180.

`max_events_per_month` is now a hard limit, including policies and relief. The old `high_pressure_bonus_event` setting is removed. Twists and habit thresholds no longer silently exceed the limit. With one slot and a due crisis, the crisis takes priority over the policy; no policy fee is charged. With zero slots, nothing mutates.

Ordinary events require an intervening month before repeating. No-change attempts consume no slot and start no cooldown. A pending crisis retains its threat when it cannot resolve, including during recovery.

The journal keeps 128 entries and prints its retained entries when the script stops. The overlay redraws every frame, labels fake simulation clearly, and uses a 29-pixel compact panel.

Ownership data is read before each rival-row mutation. Defaults block all rival boosts without an ownership map. Player-owned, neutral, and unmapped owner rows are excluded. A captured nemesis is reselected from eligible rows. Ownership fields do not count toward the legacy `cfg 10` core-field count.

Month values must be in a configured 12-month range and stable for three frames by default. Reset/load clears pending threats, policy runtime selection, audits, event cooldowns, fake state and journal. Bad booleans, overlapping/incomplete tables, missing or duplicate hotkeys, and invalid bounds are rejected.

The demo is generated from the current director, with only self-test and nemesis enabled. Tests verify their parity.

Known limitations: no verified game RAM map; unsigned one-byte stats only; no exact save/rewind persistence; no tested full-campaign balance; Mesen 2 tested through API mocks only. Older copies and original game/save files were preserved.
