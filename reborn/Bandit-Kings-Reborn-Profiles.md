# Configuration profiles — 0.4

Keep the default `dry_run=true` until the live map is verified. A profile does not supply game addresses.

| Setting | Learning the director | Standard | More pressure |
| --- | --- | --- | --- |
| difficulty | 1 | 2 | 3 |
| max_events_per_month | 2 | 3 | 3 |
| event_repeat_gap | 2 | 1 | 1 |
| policy | balanced | balanced | balanced |
| require_enemy_ownership | true | true | true |
| nemesis_rivals | false | false until table order verified | true only after verification |

Policy can be changed with P without restarting. H opens history; O hides the panel. Change the three key-name settings if they overlap your bindings. A lower event budget can delay a crisis; with a one-slot budget a due crisis skips that month's policy without charging it. A zero budget disables mutations, even during recovery.

Use `bandit-kings-reborn-demo.lua` for a simulated preview. Do not transfer its synthetic addresses into the live director.
