# How to Obtain the ROM

## Legal Notice

This toolkit requires you to provide your own copy of "Bandit Kings of Ancient China" for the NES. We do not provide, host, or distribute ROM files.

## Legal Methods to Obtain the ROM

### 1. Dump from Your Own Cartridge (Recommended)

If you own the original NES cartridge, you can legally create a ROM backup:

**Equipment Needed:**
- Original NES cartridge of "Bandit Kings of Ancient China"
- Cartridge dumper device (such as):
  - Retrode 2
  - INLretro
  - Kazzo
  - NES cart reader (Arduino-based)

**Process:**
1. Connect your cartridge dumper to your computer
2. Insert your Bandit Kings cartridge
3. Use the dumper software to create a .nes file
4. Verify the ROM with MD5 checksum
5. Place the ROM in this directory as `bandit_kings_original.nes`

### 2. Digital Purchase

Check if the game is available through:
- **Nintendo Switch Online** (if available in NES library)
- **Virtual Console** (Wii/Wii U/3DS - if region available)
- **Official retro gaming collections**

Note: Digital versions may require extraction tools specific to each platform.

### 3. Archival Sources

For preservation and educational purposes, ROM files may be available from:
- Personal backups
- Legal ROM libraries (verify your jurisdiction)
- Game preservation organizations

**Always verify the legality in your region.**

## ROM Information

**Game Details:**
- **Title**: Bandit Kings of Ancient China
- **Japanese Title**: 水滸伝・天命の誓い (Suikoden: Tenmei no Chikai)
- **Developer**: KOEI
- **Publisher**: KOEI
- **Release**: 1989 (Japan), 1990 (USA)
- **Platform**: Nintendo Entertainment System (NES)

**Expected ROM File:**
- **Filename**: Place as `bandit_kings_original.nes`
- **Size**: ~256 KB (262,144 bytes)
- **Format**: iNES format (.nes)
- **Mapper**: MMC3 (Mapper 4)

**Verification:**

After obtaining your ROM, verify it's correct:

```bash
md5sum bandit_kings_original.nes
```

Common valid MD5 checksums (different releases exist):
- USA version: Various checksums exist for different releases
- If your ROM loads in an emulator and shows "Bandit Kings of Ancient China" on the title screen, it's likely correct

## Testing Your ROM

Before patching, test that your ROM works:

1. **Download an NES emulator**:
   - FCEUX (Windows/Linux/Mac)
   - Mesen (Windows/Linux)
   - Nestopia (Multi-platform)
   - RetroArch with NES core

2. **Load the ROM**:
   - Open your emulator
   - File → Load ROM → Select `bandit_kings_original.nes`
   - Verify the game starts and shows the title screen

3. **If it works**, you're ready to patch!

## Troubleshooting

### ROM doesn't load
- **Check file size**: Should be around 256 KB
- **Check extension**: Must be `.nes`
- **Try different emulator**: Some are more compatible

### Wrong game loads
- Verify you have the correct game
- Check the title screen
- Compare file size

### "File not found" error from patcher
- Ensure ROM is named exactly: `bandit_kings_original.nes`
- Place in the same directory as `patch_rom.py`
- Check file permissions (must be readable)

## Privacy & Safety

**Never:**
- Download ROMs from untrusted sources (malware risk)
- Share ROM files publicly (copyright violation)
- Distribute patched ROMs (use patch files instead)

**Always:**
- Use reputable dumping hardware
- Verify files with checksums
- Keep backups of your original dumps
- Respect copyright laws in your jurisdiction

## After You Have the ROM

Once you have `bandit_kings_original.nes` in this directory:

```bash
# Quick start
./quickstart.sh

# Or manual
python3 patch_rom.py --preset balanced
```

## Questions?

**Q: Is ROM hacking legal?**
A: Modifying your own legally-obtained ROM for personal use is generally legal in most jurisdictions. Distribution of ROMs is typically not legal.

**Q: Can I share my patched ROM?**
A: No. Share the patcher scripts instead (this repository), not the ROM files.

**Q: What if I can't find the cartridge?**
A: The game is relatively rare. Check retro game stores, online marketplaces, or game collecting communities.

---

*This document is for educational purposes. Users are responsible for complying with copyright laws in their jurisdiction.*
