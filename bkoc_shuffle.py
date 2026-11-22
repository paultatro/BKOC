#!/usr/bin/env python3
"""Build a shuffled Bandit Kings of Ancient China ROM.

    python3 bkoc_shuffle.py "Bandit Kings of Ancient China (U).nes" shuffled.nes --seed 1234
"""
import argparse
import os
import sys

from bkoc import Rom, RomError, build


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("input", help="canonical Bandit Kings of Ancient China (U) ROM")
    p.add_argument("output", help="where to write the new ROM")
    p.add_argument("--seed", type=int, help="same seed + options = same ROM (random if omitted)")
    p.add_argument("--no-stats", action="store_true", help="don't shuffle character stats")
    p.add_argument("--chaos", action="store_true",
                   help="shuffle stats across everyone instead of within power tiers")
    p.add_argument("--tier-size", type=int, default=16,
                   help="characters per power tier for the stat shuffle (default 16)")
    p.add_argument("--new-generals", type=int, default=8, help="new generals to add (0-20, default 8)")
    p.add_argument("--gaoqiu", choices=["classic", "stronger", "weaker"], default="classic",
                   help="Gao Qiu's power preset (experimental, default classic)")
    a = p.parse_args()

    seed = a.seed if a.seed is not None else int.from_bytes(os.urandom(4), "big")
    try:
        rom = Rom.load(a.input)
        log = build(rom, seed, stats=not a.no_stats, chaos=a.chaos, tier_size=a.tier_size,
                    new_generals=a.new_generals, gaoqiu=a.gaoqiu)
    except (RomError, ValueError, OSError) as e:
        sys.exit(f"error: {e}")

    with open(a.output, "wb") as f:
        f.write(rom.data)
    spoiler = os.path.splitext(a.output)[0] + ".spoiler.txt"
    with open(spoiler, "w") as f:
        f.write("\n".join(log) + "\n")
    print(f"seed {seed}: wrote {a.output} and {spoiler}")


if __name__ == "__main__":
    main()
