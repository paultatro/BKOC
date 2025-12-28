# Bandit Kings of Ancient China - Enhanced Edition

A ROM hacking toolkit for improving and randomizing the NES game "Bandit Kings of Ancient China" (Suikoden: Tenmei no Chikai).

## 🚀 NEW? Start Here!

**👉 [BEGINNER_GUIDE.md](BEGINNER_GUIDE.md) - Complete step-by-step installation guide**

**Or run the setup helper:**
```bash
cd /home/user/BKOC
./setup_helper.sh
```

This will check your installation and guide you through the process!

## Features

- **General Shuffle**: Randomize all generals' starting locations and affiliations
- **Stat Randomization**: Rebalance and randomize general statistics for varied gameplay
- **Geography Modification**: Alter terrain, cities, and resource distributions
- **Resource Rebalancing**: Adjust gold, rice, soldiers, and weapons across the map
- **Innovative Enhancements**:
  - Balanced difficulty modes
  - Hidden character stat boosts
  - Enhanced AI behavior patterns
  - Dynamic resource scaling

## Setup

### For Beginners

**📖 Read the complete guide:** [BEGINNER_GUIDE.md](BEGINNER_GUIDE.md)

**Or run the automatic setup helper:**
```bash
cd /home/user/BKOC
./setup_helper.sh
```

### Quick Setup (If You Know What You're Doing)

1. Place your ROM file as `bandit_kings_original.nes` in this directory
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the patcher:
   ```bash
   python3 patch_rom.py --preset balanced
   ```

### Requirements

- Python 3.7+
- Original NES ROM: `Bandit Kings of Ancient China (USA).nes`
  - Legally obtain from your own cartridge (see [ROM_ACQUISITION.md](ROM_ACQUISITION.md))

## Usage

### Quick Patch
```bash
python patch_rom.py --preset balanced
```

### Custom Options
```bash
python patch_rom.py \
  --shuffle-generals \
  --randomize-stats \
  --modify-geography \
  --rebalance-resources \
  --difficulty hard \
  --output bandit_kings_enhanced.nes
```

### Available Presets
- `chaos`: Maximum randomization, wild stat variations
- `balanced`: Moderate changes, improved balance
- `enhanced`: Subtle improvements, original feel
- `custom`: Use individual flags

## Modifications

### General Shuffle
- Randomizes starting positions of all 108 generals
- Maintains some historical character groupings (optional)
- Ensures game remains winnable

### Stat Randomization
- Intelligence (INT)
- Leadership (LDR)
- Strength (STR)
- Luck (LCK)
- Weapon proficiency
- Special abilities

### Geography Changes
- Terrain type variations
- City size and importance adjustments
- Travel route modifications
- Strategic chokepoint rebalancing

### Resource Modifications
- Starting resources for all forces
- City production rates
- Market prices and availability
- Hidden treasure locations

## ROM Structure Documentation

See `docs/rom_structure.md` for detailed memory mapping and data structures.

## Safety

All modifications create a new ROM file - your original is never modified.

## Legal

This toolkit is for educational purposes and personal use only. You must own a legal copy of the game to use these tools.

## Credits

- Original game: KOEI (1989)
- ROM hacking tools and documentation: BKOC Enhancement Project
