# Troubleshooting — 0.4

**MAP REQUIRED / no events:** The live map is empty by default. Use the demo for an immediate preview, or calibrate the real map. Do not borrow demo addresses.

**DEMO appears but the game values do not change:** Expected. The director is changing a fake campaign only.

**Rival events do nothing:** The ownership guard is enabled. Confirm player-owner address, rival owner rows, neutral values, active rows, and matching entity order. Missing/short owner tables block affected rows. A capped rival value also produces no change.

**P/H/O does not respond:** Focus the game window, check that the script is running, and use key names accepted by your emulator. These keys are not intercepted from the game. Rebind them if they conflict. If the API is absent, configure the starting policy in the file.

**A policy did not charge or pay out:** It may be unaffordable, unmapped or already at its benefit cap, or there may be no budget slot. Recovery has first priority; with one slot a due crisis has priority over policy. The selection remains for later months.

**Crises wait:** Recovery postpones crises. A crisis also waits if there is no slot or no target it can change. Threat is retained.

**Two quick month changes become one:** The cooldown deliberately coalesces rapid changes to the latest observed month. Values must also be stable for three frames by default. Set the correct 0–11 or 1–12 range after verification.

**History disappears on loading:** Expected. Director state is session-local; copying the script log preserves a readable record, but loading a save does not restore director history.

**The panel covers something:** O hides it; H closes the expanded journal. Events continue while it is hidden.

**Configuration error at startup:** Read the named field in the script log. All booleans must be actual true/false values; tables need a start/count pair and positive stride; addresses cannot overlap; key names must be distinct; only supported unsigned-byte RAM addresses are accepted.

**Controls do nothing (title screen plays, buttons dead):** Click once on the game picture. While the Script Window or any other window has focus, Mesen sends no buttons to the game, because Background Input is off by default. None of these scripts override controller input. If it still happens without any script running, load the untouched original ROM in the same Mesen. If that works but a shuffled ROM doesn't, report it with the ROM's seed and options.
