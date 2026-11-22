"""Data fixes applied to every build. Each target string occurs once in the ROM (inside its
own character slot), so renaming it cannot desync story text or menus."""
from .tables import Rom, RomError

# slot, old nickname, new nickname, reason
NAME_FIXES = [
    (216, "She-devil", "Jade Amazon",
     "Hu Sanniang's nickname (Ten Feet of Jade) was translated as a slur"),
    (194, "Winged Tiger", "Mountain Tiger",
     "Two characters shared 'Winged Tiger'; slot 64 (108-star Lei Heng) keeps it"),
    (91, "Like Ren Gui", "Rival Ren Gui",
     "Guo Sheng's nickname means 'Rival of Ren Gui', not 'Like Ren Gui'"),
    (112, "Stayed by None", "Unstoppable",
     "Mu Hong's nickname reads as garbled English; 'Unstoppable' is the usual rendering"),
    (177, "Heavens Guard", "Heaven's Guard",
     "Missing apostrophe; every other 'Heaven's' nickname has one"),
]


def apply_fixes(rom: Rom):
    log = []
    for slot, old, new, why in NAME_FIXES:
        if rom.name(slot) != old:
            raise RomError(f"Slot {slot} is {rom.name(slot)!r}, expected {old!r}")
        # The duplicate nickname legitimately occurs twice: once in each of the two slots.
        if rom.count_text(old) != rom.names().count(old):
            raise RomError(f"{old!r} is referenced outside its slot; refusing to rename")
        rom.set_name(slot, new)
        log.append(f"slot {slot:3d}: {old!r} -> {new!r}  ({why})")
    return log
