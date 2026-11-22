# Mod kit — Council and Chronicle 0.4

This kit adds a Lua campaign director beside Bandit Kings of Ancient China in Mesen. Its interface and fake-memory demo work now. Its live game effects require a calibrated address map.

Start with `START-HERE-Bandit-Kings-Reborn.md`. Use the runbook for live integration, event catalog for exact implemented behavior, profiles for difficulty choices, review for evidence and limitations, and the calibration worksheet/template for game-specific data.

The design direction is preparation, consequence and recovery: let the player see a coming crisis, spend scarce resources to prepare, and read a short record of what happened. Policies and visible forecasts make the director less arbitrary; cooldowns and a hard cap limit repeated punishment. Dynamic ownership checks keep supported rival mutations attached to rivals after territory changes.

This implementation does not add officer biographies, traits, relationships, defections, strategic commands, tactical combat AI, provinces, save capacity, dynasty succession, or new ROM assets. A coalition event is a resource effect, not a new game diplomacy system. A nemesis is a guarded table slot, not an identified historical character. Those larger ambitions require separate game integration work.

The director, demo and calibration scripts are editable Lua. The Python verification suite requires `lupa==2.8` and runs from this folder. Real Mesen testing used the official headless test-runner API and the user's existing ROM in an isolated directory. No game ROM or emulator executable is distributed in this kit.
