# Live integration test record — 0.3

## Completed emulator smoke test

November 4, 2026: Mesen 0.9.8.0, 2,400 frames / 19 simulated months. Passed. Zero Lua RAM-write calls; zero text-drawing errors. Source: `Mesen-smoke-result.txt`. The demo used synthetic state over the running game. This is not proof of live campaign mutations.

## Still unverified

| Item | Result |
| --- | --- |
| ROM/scenario-specific month address and encoding | Not verified |
| Player stats and one-byte encoding | Not verified |
| Rival stat/owner table identity and ordering | Not verified |
| Neutral/unused owner encodings | Not verified |
| Post-conquest ownership changes in a real campaign | Not verified |
| P/H/O physical keyboard interactions | Not interactively tested |
| Mesen 2 executable | Not tested; API mocks only |
| Full campaign balance | Not tested |

For future integration, record ROM hash, emulator version, scenario, addresses, before/after displayed values, raw bytes, owner IDs, and screenshots for each controlled action. Repeat key observations in a second campaign state.
