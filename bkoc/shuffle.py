"""Seeded shuffles over the verified character table.

Only stat bytes 4-7 and the nickname field are written; ID/flag bytes 0-3 are never touched.
"""
import random
from .tables import Rom, GAO_QIU, LAST_SLOT

# Slot 1 (Tattooed Priest) is the only character with stat byte 7 = 0, which may be a marker.
PINNED = {1}
SHUFFLABLE = [i for i in range(GAO_QIU + 1, LAST_SLOT) if i not in PINNED]

# Slots whose portrait would contradict a new, unrelated general.
KEEP_IDENTITY = {"Golden Lotus"}

NEW_GENERAL_NAMES = [
    "Salt Smuggler", "Iron Lantern", "River Ghost", "Bronze Gong", "Night Owl",
    "Ferry Wolf", "Ash Phoenix", "Rope Dancer", "Hill Hermit", "Thirsty Blade",
    "Red Abacus", "Jade Gambler", "Paper Tiger", "Lantern Thief", "Copper Hound",
    "Mist Walker", "Toll Breaker", "Ink Assassin", "Silk Bandit", "Grey Heron",
]

GAO_QIU_POWER = {"classic": 76, "stronger": 95, "weaker": 55}


def power(stats):
    return sum(stats)


def shuffle_stats(rom: Rom, rng: random.Random, tier_size: int = 16, chaos: bool = False):
    """Swap whole stat blocks between characters of similar overall power (or all, with chaos)."""
    ranked = sorted(SHUFFLABLE, key=lambda i: (-power(rom.stats(i)), i))
    groups = [ranked] if chaos else [ranked[k:k + tier_size] for k in range(0, len(ranked), tier_size)]
    for group in groups:
        blocks = [rom.stats(i) for i in group]
        rng.shuffle(blocks)
        for i, b in zip(group, blocks):
            rom.set_stats(i, b)


def new_general_slots(rom: Rom, n: int):
    """The n weakest non-story slots: non-star ID space (byte 1 high bit), unique nickname."""
    eligible = [i for i in SHUFFLABLE
                if rom.id_bytes(i)[1] & 0x80
                and rom.name(i) not in KEEP_IDENTITY
                and rom.count_text(rom.name(i)) == 1]
    eligible.sort(key=lambda i: (power(rom.stats(i)), i))
    return eligible[:n]


def add_new_generals(rom: Rom, rng: random.Random, n: int):
    if n <= 0:
        return []
    taken = set(rom.names())
    names = [x for x in NEW_GENERAL_NAMES if x not in taken]
    if n > len(names):
        raise ValueError(f"At most {len(names)} new generals are available")
    slots = new_general_slots(rom, n)
    if len(slots) < n:
        raise ValueError(f"Only {len(slots)} slots can safely host new generals")
    # Mid-table characters (ranks 30-150) are worth recruiting but not game-breaking.
    ranked = sorted(SHUFFLABLE, key=lambda i: -power(rom.stats(i)))[30:150]
    pool = [rom.stats(i) for i in ranked]
    added = []
    for slot, name in zip(slots, rng.sample(names, n)):
        old = rom.name(slot)
        rom.set_name(slot, name)
        rom.set_stats(slot, tuple(rng.choice(pool)[k] for k in range(4)))
        added.append((slot, old, name))
    return added


def set_gao_qiu(rom: Rom, preset: str):
    s = rom.stats(GAO_QIU)
    rom.set_stats(GAO_QIU, (GAO_QIU_POWER[preset],) + s[1:])
