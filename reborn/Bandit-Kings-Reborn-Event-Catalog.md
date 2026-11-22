# Event catalog — version 0.4

All events operate on configured one-byte values. None discovers addresses or rewrites game AI.

| Event | Eligibility and effect |
| --- | --- |
| Provision | 6 player gold buys up to 10 food, capped at 220; paid policy halves a warned famine loss |
| Patronage | 8 player food buys up to 4 popularity, capped at 100; paid policy reduces warned unrest loss to 1 |
| Drill | 5 player gold buys up to 4 training, capped at 100 |
| Goodwill | Popularity at least 65 and food below 180: up to +4 food, 35% candidate chance, subject to budget/cooldown |
| Recovery | Food below 18 or troops below 18: +6 food and/or +4 troops; no hostile events in the month |
| Rival economy | Raises eligible rival gold/food; doctrine, twist and nemesis may increase bonuses |
| Rival armies | Raises eligible rival troops/loyalty; does not reduce existing above-cap values |
| Coalition | Raises eligible rival gold/troops; does not create actual diplomatic alliances |
| Nemesis pressure | Extra stat boosts to a currently eligible rival table index; not a named-officer AI |
| Supply strain | Troops above 90 consume extra food |
| Court conspiracy | Lowers configured player popularity/loyalty |
| Steward/rot/rumor/drill loss | Random ordinary pressure, weighted by current twist |
| Habit response | Responds to sustained large stores, army size or low trust with the corresponding pressure |
| Warned famine | Food loss after at least one warning month; provision mitigates it |
| Warned unrest | Popularity -2; paid patronage changes this to -1 |
| Warned rival levy | Adds troops to eligible rival rows |

Threat accrues during non-recovery months. At threshold, a mapped crisis is chosen and announced for the next processed month. It retains its identity if postponed. It resolves only if it can change a value and has a budget slot. Recovery postpones it. If a target has become unavailable, the pending crisis remains until it can resolve or the session resets.

Ordinary event types have an intervening-month cooldown after successful delivery by default. Policies, recovery and crises are exempt. Announcements and policy selection are journal entries, not mutation events. Nominal losses in older event messages can exceed the actual loss when a resource reaches zero; use dry-run old/new values to inspect exact changes. Policy/goodwill messages report actual benefits.

Twists change weights or amounts for six processed months by default. They do not schedule extra events beyond the hard monthly cap. Balanced policy costs nothing. Defaults remain difficulty 3 and three events/month; lower the difficulty for initial calibration.
