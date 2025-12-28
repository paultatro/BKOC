# Bandit Kings of Ancient China - Enhanced Edition

## 🎮 Project Overview

A comprehensive ROM hacking toolkit for enhancing and randomizing the classic NES game "Bandit Kings of Ancient China" (水滸伝・天命の誓い Suikoden: Tenmei no Chikai) by KOEI.

## ✨ Features

### 🎲 General Shuffling
- **Complete Randomization**: Shuffle all 108 generals across 64 cities
- **Preserve Groups**: Option to keep historical character groups together
- **Wandering Heroes**: Create unaffiliated generals ready for recruitment
- **Faction Balancing**: Distribute generals evenly across factions
- **Mega Factions**: Create super-powerful enemy factions for challenge

### 📊 Stat Randomization
- **Controlled Variance**: Adjust how much stats vary (0.0 = none, 1.0 = complete chaos)
- **Specialists**: Create generals who excel in one area
- **Super Generals**: Generate legendary heroes with max stats
- **Archetypes**: Warriors, Strategists, Leaders, Lucky heroes, etc.
- **Ability Randomization**: Shuffle special abilities and weapon types
- **Weakness System**: Interesting strength/weakness combinations

### 🗺️ Geography Modification
- **Terrain Randomization**: Change terrain types affecting defense and movement
- **City Importance**: Shuffle which cities are major trade hubs vs small villages
- **Strategic Chokepoints**: Create heavily-fortified fortress cities
- **Connection Rewiring**: Change the strategic map layout
- **Economic Zones**: Create rich/poor regions for interesting dynamics
- **Border Regions**: Distinct areas with unique characteristics

### 💎 Innovative Enhancements
- **Legendary Items**: Cities with massive weapon caches
- **Difficulty Scaling**: Easy/Normal/Hard/Chaos modes
- **Hidden Champions**: Secret max-stat generals in remote locations
- **Trade Hubs**: Economic powerhouse cities
- **Bandit Havens**: Thematic outlaw strongholds
- **Dynamic Loyalty**: Varied loyalty creates betrayal opportunities
- **Recruitment Paradises**: Cities perfect for building your army

## 📁 Project Structure

```
BKOC/
├── patch_rom.py           # Main patcher script
├── quickstart.sh          # Quick start helper
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
├── EXAMPLES.md            # Usage examples
├── ROM_ACQUISITION.md     # How to legally obtain ROM
├── PROJECT_OVERVIEW.md    # This file
├── .gitignore            # Git ignore rules
│
├── tools/                 # Core hacking toolkit
│   ├── __init__.py
│   ├── rom_handler.py         # ROM read/write operations
│   ├── general_shuffler.py    # General distribution
│   ├── stat_randomizer.py     # Stat modifications
│   ├── geography_modifier.py  # Map/terrain changes
│   └── enhancements.py        # Gameplay improvements
│
├── data/                  # Reference data
│   └── reference_info.txt # Game mechanics reference
│
└── docs/                  # Documentation
    └── rom_structure.md   # ROM memory map
```

## 🚀 Quick Start

1. **Get the ROM** (see ROM_ACQUISITION.md)
   ```bash
   # Place your ROM as: bandit_kings_original.nes
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the patcher**
   ```bash
   # Easy mode
   ./quickstart.sh

   # Or choose a preset
   python3 patch_rom.py --preset balanced
   ```

4. **Play!**
   ```bash
   # Load bandit_kings_enhanced.nes in your NES emulator
   ```

## 🎯 Presets

### Chaos
Maximum randomization - wild unpredictable gameplay
```bash
python3 patch_rom.py --preset chaos
```

### Balanced (Recommended)
Moderate changes with improved balance
```bash
python3 patch_rom.py --preset balanced
```

### Enhanced
Subtle improvements keeping original feel
```bash
python3 patch_rom.py --preset enhanced
```

## 🛠️ Custom Options

Full control over every aspect:

```bash
python3 patch_rom.py \
  --shuffle-generals \
  --preserve-groups \
  --randomize-stats \
  --stat-variance 0.4 \
  --super-generals 10 \
  --modify-geography \
  --randomize-terrain \
  --chokepoints 12 \
  --enhancements \
  --difficulty hard \
  --seed 42069 \
  --output custom_rom.nes
```

See EXAMPLES.md for detailed examples.

## 🎲 Reproducible Builds

Use seeds to create identical ROMs:

```bash
# You and a friend can play the exact same version
python3 patch_rom.py --preset balanced --seed 12345
```

## 📖 Documentation

- **README.md** - Main documentation
- **EXAMPLES.md** - Usage examples and recipes
- **ROM_ACQUISITION.md** - How to legally obtain the ROM
- **docs/rom_structure.md** - Technical ROM memory map
- **data/reference_info.txt** - Game mechanics reference

## 🔧 Technical Details

### ROM Specifications
- **Platform**: NES (Nintendo Entertainment System)
- **Mapper**: MMC3 (Mapper 4)
- **PRG ROM**: 256 KB
- **CHR ROM**: 128 KB
- **Total Size**: ~256 KB

### Modification Areas
- **General Data**: 0x1C010-0x1C6BF (108 generals × 16 bytes)
- **City Data**: 0x1E010-0x1E80F (64 cities × 32 bytes)
- **Market Prices**: 0x22010-0x2210F
- **Production Rates**: 0x22110-0x2220F
- **AI Behavior**: 0x24010-0x2417F

### Safe Modifications
All modifications are safe and create NEW ROM files. Your original ROM is never modified.

## 🎮 Gameplay Impact

### What Gets Randomized
- ✅ General starting positions
- ✅ General stats (LDR/INT/STR/LCK)
- ✅ Special abilities and weapons
- ✅ City resources and production
- ✅ Terrain and geography
- ✅ AI behavior patterns

### What Stays the Same
- ❌ Game mechanics and rules
- ❌ Graphics and music
- ❌ Story events and triggers
- ❌ Core gameplay systems

## 🏆 Use Cases

### Single Player
- Fresh playthrough with new challenges
- Theme-based runs (economic, military, etc.)
- Difficulty variations
- Replayability through randomization

### Multiplayer
- Tournament mode with shared seed
- Daily challenges
- Racing competitions
- Co-op with same ROM

### Streaming
- Chaos mode for entertainment
- Viewer seed submissions
- Challenge runs
- Randomizer races

## 🔐 Legal & Safety

- ✅ For personal use only
- ✅ Requires legal ROM ownership
- ✅ Educational purposes
- ✅ Original ROM never modified
- ❌ Do not distribute ROM files
- ❌ Share seeds/patches only, not ROMs

See ROM_ACQUISITION.md for details on legally obtaining the game.

## 🤝 Contributing

Ideas for enhancements:
- Additional gameplay modes
- More specialized archetypes
- Historical accuracy options
- Custom scenario generators
- Balance improvements
- Bug fixes and optimizations

## 📊 Stats at a Glance

- **108 Generals** - All modifiable
- **64 Cities** - Fully customizable
- **16 Factions** - Can be rebalanced
- **16 Terrain Types** - Shuffleable
- **8 Special Abilities** - Randomizable
- **∞ Combinations** - Limited only by seeds

## 🎯 Design Philosophy

1. **Preserve Core Gameplay** - Don't break what makes the game fun
2. **Enhance Replayability** - Every playthrough feels different
3. **Maintain Balance** - Chaos is fun, but should be optional
4. **Stay True to Theme** - "Bandit Kings" outlaw aesthetic
5. **User Control** - Presets for quick start, options for customization

## 🌟 Special Thanks

- **KOEI** - Original game developers (1989)
- **NES ROM Hacking Community** - Tools and documentation
- **Water Margin** - The legendary Chinese novel that inspired it all

## 🔮 Future Possibilities

- GUI version of patcher
- Web-based ROM patcher
- Additional game modes
- Custom scenario builder
- AI personality editor
- Advanced diplomacy options
- Custom general creator

## 📝 Version History

- **v1.0** - Initial release
  - General shuffling
  - Stat randomization
  - Geography modification
  - Gameplay enhancements
  - Three presets (chaos/balanced/enhanced)
  - Full customization options

---

**Enhance your Bandit Kings experience - Every seed is a new adventure!** 🎲
