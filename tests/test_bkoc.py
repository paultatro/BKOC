"""Run with:  BKOC_ROM=/path/to/rom.nes python3 -m unittest discover tests"""
import os
import unittest

from bkoc import Rom, RomError, build
from bkoc.tables import CHAR_TABLE, CHAR_SLOT, CHAR_COUNT, PROVINCE_TABLE, PROVINCE_RECORD, \
    PROVINCE_COUNT, STAT_LIMITS, WRITABLE

ROM_PATH = os.environ.get("BKOC_ROM", "bandit_kings_original.nes")


@unittest.skipUnless(os.path.exists(ROM_PATH), f"set BKOC_ROM to the canonical ROM ({ROM_PATH} missing)")
class BuildTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(ROM_PATH, "rb") as f:
            cls.original = f.read()

    def make(self, seed=7, **kw):
        rom = Rom(self.original)
        log = build(rom, seed, **kw)
        return bytes(rom.data), log

    def test_deterministic(self):
        self.assertEqual(self.make(42)[0], self.make(42)[0])
        self.assertNotEqual(self.make(42)[0], self.make(43)[0])

    def test_changes_confined_to_verified_tables(self):
        for kw in ({}, {"chaos": True, "new_generals": 20, "gaoqiu": "stronger"}):
            out, _ = self.make(**kw)
            self.assertEqual(len(out), len(self.original))
            self.assertEqual(out[:16], self.original[:16])
            for i, (a, b) in enumerate(zip(self.original, out)):
                if a != b:
                    self.assertTrue(any(lo <= i < hi for lo, hi in WRITABLE), hex(i))
                    self.assertGreaterEqual((i - CHAR_TABLE) % CHAR_SLOT, 4, f"ID byte changed at {i:#x}")

    def test_stats_in_range_and_tier_totals_kept(self):
        out, _ = self.make(new_generals=0)
        rom = Rom(out, check_md5=False)
        orig = Rom(self.original)
        for i in range(CHAR_COUNT):
            for v, hi in zip(rom.stats(i), STAT_LIMITS):
                self.assertTrue(0 <= v <= hi)
        # Shuffle only permutes blocks among slots 2-254, so the multiset is unchanged.
        self.assertEqual(sorted(orig.stats(i) for i in range(2, 255)),
                         sorted(rom.stats(i) for i in range(2, 255)))
        self.assertEqual(rom.stats(1), orig.stats(1))
        self.assertTrue(all(rom.stats(i)[3] >= 1 for i in range(2, 255)))

    def test_unique_nicknames_and_fixes(self):
        out, log = self.make(new_generals=20)
        names = Rom(out, check_md5=False).names()
        self.assertEqual(len(names), len(set(names)))
        for bad in ("She-devil", "Like Ren Gui", "Stayed by None", "Heavens Guard"):
            self.assertNotIn(bad, names)
        self.assertEqual(names.count("Winged Tiger"), 1)

    def test_story_names_untouched(self):
        out, _ = self.make(new_generals=20)
        rom = Rom(out, check_md5=False)
        self.assertIn("Golden Lotus", rom.names())
        self.assertEqual(rom.name(0), "Evil Gao Qiu")
        self.assertEqual(rom.name(255), "Lan")

    def test_map_untouched(self):
        out, _ = self.make(chaos=True, new_generals=20)
        end = PROVINCE_TABLE + PROVINCE_RECORD * PROVINCE_COUNT
        self.assertEqual(out[PROVINCE_TABLE:end], self.original[PROVINCE_TABLE:end])

    def test_rejects_wrong_rom(self):
        with self.assertRaises(RomError):
            Rom(self.original[:-1] + b"\0")


if __name__ == "__main__":
    unittest.main()
