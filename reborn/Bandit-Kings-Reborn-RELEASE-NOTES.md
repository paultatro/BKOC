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
