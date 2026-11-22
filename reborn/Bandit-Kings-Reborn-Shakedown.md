# Shakedown — 0.3

## Already verified

- 68 Lua regression checks pass across Lua 5.1/5.4.
- Real Mesen 0.9.8 demo: 2,400 frames, 19 simulated months, zero Lua game-memory writes, zero text-drawing errors.
- Captured compact/history display fits the NES screen.

## Check for your live map

- First stable month does not trigger events; subsequent verified month changes do.
- The panel says DRY RUN before real writes are enabled.
- Every mapped field is an unsigned one-byte value with stable entity identity.
- Ownership filtering excludes player, neutral, unused, and newly captured rows.
- Paid policies use the intended resources and show the expected capped benefit.
- Crisis warnings precede the crisis; recovery suppresses hostile events.
- Monthly event count never exceeds the configured limit.
- Save load resets journal/pending crisis and rebaselines the current month.
- Your physical P/H/O bindings work without affecting base-game controls.

Record actual game results in `Bandit-Kings-Reborn-Live-Test-Report.md`. Mock tests and a fake-memory demo cannot establish these facts for a real campaign.
