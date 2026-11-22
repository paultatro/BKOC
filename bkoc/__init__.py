from .tables import Rom, RomError
from .fixes import apply_fixes
from .shuffle import shuffle_stats, add_new_generals, set_gao_qiu


def build(rom: Rom, seed: int, stats=True, chaos=False, tier_size=16, new_generals=8,
          gaoqiu="classic"):
    """Apply fixes and shuffles in a fixed order; returns the spoiler log lines."""
    import random
    original = Rom(bytes(rom.data), check_md5=False)
    rng = random.Random(seed)
    log = [f"Bandit Kings Shuffle Edition  seed={seed}",
           f"options: stats={'chaos' if chaos and stats else stats} tier_size={tier_size} "
           f"new_generals={new_generals} gaoqiu={gaoqiu}", "", "== Fixes =="]
    log += apply_fixes(rom)
    added = add_new_generals(rom, rng, new_generals)
    if stats:
        shuffle_stats(rom, rng, tier_size, chaos)
    set_gao_qiu(rom, gaoqiu)

    log += ["", "== New generals =="]
    log += [f"slot {s:3d}: {new!r} (replaces {old!r})" for s, old, new in added] or ["none"]
    log += ["", "== Character changes (stats are bytes 4-7 of each slot) =="]
    for i in range(256):
        a, b = original.stats(i), rom.stats(i)
        if a != b or original.name(i) != rom.name(i):
            log.append(f"slot {i:3d} {rom.name(i):16s} {a} -> {b}")
    return log
