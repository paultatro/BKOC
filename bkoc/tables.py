"""Verified data tables in Bandit Kings of Ancient China (U), NES, MMC5.

Only layouts confirmed by inspecting the canonical ROM live here; see docs/CHANGES.md.
"""
import hashlib

CANONICAL_MD5 = "5ef1ba9461974f34b0633eaf063490dd"
ROM_SIZE = 393232

CHAR_TABLE = 0x03600C
CHAR_SLOT = 24
CHAR_COUNT = 256
NAME_OFF = 8
NAME_FIELD = 16
NAME_MAX = NAME_FIELD - 1
STAT_OFF = 4
STAT_LIMITS = (100, 100, 100, 50)  # max observed per stat byte 4..7; all minimums are 0

GAO_QIU = 0
LAST_SLOT = 255

PROVINCE_TABLE = 0x037808
PROVINCE_RECORD = 27
PROVINCE_COUNT = 48

WRITABLE = [(CHAR_TABLE, CHAR_TABLE + CHAR_SLOT * CHAR_COUNT)]


class RomError(ValueError):
    pass


class Rom:
    def __init__(self, data: bytes, check_md5: bool = True):
        if len(data) != ROM_SIZE or data[:4] != b"NES\x1a":
            raise RomError(f"Not a {ROM_SIZE}-byte iNES ROM")
        if check_md5 and hashlib.md5(data).hexdigest() != CANONICAL_MD5:
            raise RomError("ROM is not the canonical Bandit Kings of Ancient China (U) dump "
                           f"(expected MD5 {CANONICAL_MD5})")
        self.data = bytearray(data)

    @classmethod
    def load(cls, path, check_md5=True):
        with open(path, "rb") as f:
            return cls(f.read(), check_md5)

    def write_field(self, offset: int, new: bytes):
        end = offset + len(new)
        if not any(lo <= offset and end <= hi for lo, hi in WRITABLE):
            raise RomError(f"Write 0x{offset:06X}-0x{end:06X} is outside verified tables")
        self.data[offset:end] = new

    def slot(self, i: int) -> int:
        if not 0 <= i < CHAR_COUNT:
            raise RomError(f"Character slot {i} out of range")
        return CHAR_TABLE + CHAR_SLOT * i

    def name(self, i: int) -> str:
        o = self.slot(i) + NAME_OFF
        return bytes(self.data[o:o + NAME_FIELD]).split(b"\0")[0].decode("ascii")

    def set_name(self, i: int, name: str):
        raw = name.encode("ascii")
        if not 1 <= len(raw) <= NAME_MAX or any(c < 0x20 or c > 0x7E for c in raw):
            raise RomError(f"Nickname {name!r} must be 1-{NAME_MAX} printable ASCII characters")
        self.write_field(self.slot(i) + NAME_OFF, raw + b"\0" * (NAME_FIELD - len(raw)))

    def stats(self, i: int) -> tuple:
        o = self.slot(i) + STAT_OFF
        return tuple(self.data[o:o + 4])

    def set_stats(self, i: int, stats):
        if len(stats) != 4 or any(not 0 <= v <= hi for v, hi in zip(stats, STAT_LIMITS)):
            raise RomError(f"Stats {stats} out of range {STAT_LIMITS}")
        self.write_field(self.slot(i) + STAT_OFF, bytes(stats))

    def id_bytes(self, i: int) -> bytes:
        o = self.slot(i)
        return bytes(self.data[o:o + 4])

    def names(self):
        return [self.name(i) for i in range(CHAR_COUNT)]

    def count_text(self, text: str) -> int:
        b, n, start = text.encode("ascii"), 0, 0
        while (start := self.data.find(b, start)) >= 0:
            n += 1
            start += 1
        return n
