# Bandit Kings Reborn: Calibration Worksheet

Use this during one clean Mesen session. Save state before each test, run one action, record the top candidate, reload, and repeat once. An address is trustworthy when it wins twice. If polling is noisy, use `bandit-kings-write-trace.lua` to shortlist candidates, then confirm exact values with Address Lab.

After each confirmed address, copy it into `Bandit-Kings-Address-Map-Template.lua`. Paste the finished `addresses = { ... }` block into the director only after the core values are stable.

| Director Field | Test 1 Candidate | Test 2 Candidate | Confirmed Address | Notes |
| --- | --- | --- | --- | --- |
| `month` |  |  |  | Advance one month. Look for +1 or wrap. |
| `player_gold` |  |  |  | Spend or gain a known amount. |
| `player_food` |  |  |  | Buy, sell, or consume a known amount. |
| `player_troops` |  |  |  | Recruit or transfer a known amount. |
| `player_training` |  |  |  | Train once from a known value. |
| `player_popularity` |  |  |  | Tax or trigger a known popularity shift. |
| `enemy_gold_start` |  |  |  | Inspect several enemy provinces; look for adjacent table bytes. |
| `enemy_gold_count` |  |  |  | Count confirmed adjacent enemy gold entries. |
| `enemy_gold_stride` |  |  |  | Use `1` if adjacent; otherwise record byte spacing. |
| `enemy_food_start` |  |  |  | Same method as enemy gold. |
| `enemy_food_count` |  |  |  | Count confirmed adjacent enemy food entries. |
| `enemy_food_stride` |  |  |  | Use `1` if adjacent; otherwise record byte spacing. |
| `enemy_troops_start` |  |  |  | Transfer, spy, or compare enemy troop changes. |
| `enemy_troops_count` |  |  |  | Count confirmed adjacent enemy troop entries. |
| `enemy_troops_stride` |  |  |  | Use `1` if adjacent; otherwise record byte spacing. |
| `enemy_loyalty_start` |  |  |  | Find adjacent officer/province loyalty values if visible. |
| `enemy_loyalty_count` |  |  |  | Count confirmed adjacent loyalty entries. |
| `enemy_loyalty_stride` |  |  |  | Use `1` if adjacent; otherwise record byte spacing. |

## First Campaign Settings

Once you have at least `month`, `player_gold`, `player_food`, `player_troops`, and one enemy table:

```lua
difficulty = 2,
show_overlay = true,
```

After two or three years of in-game time without obvious weirdness:

```lua
difficulty = 3,
```

Save states are your friend during calibration. After calibration, play without rewinds if you want the director to feel mean in the right way.

## Additional 0.3 requirements

Record the verified player faction-ID address, rival ownership table start/count/stride, neutral and unused ID encodings, and evidence that owner/stat rows share entity order. Test capture of a rival slot. Record whether the calendar is 0–11 or 1–12. Only unsigned one-byte stat fields are supported. No entry in this worksheet is supplied as a verified address.
