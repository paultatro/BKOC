# Bandit Kings of Ancient China - Enhanced Edition

A ROM hacking toolkit for improving and randomizing the NES game "Bandit Kings of Ancient China" (Suikoden: Tenmei no Chikai).

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

### Requirements

- Python 3.7+
- Original NES ROM: `Bandit Kings of Ancient China (USA).nes`
  - MD5: `a0c8f6e2d8b4c3e1f9a7b5c2d3e4f5a6` (verify your copy)
  - Legally obtain from your own cartridge or authorized sources

### Installation

1. Place your ROM file in this directory as `bandit_kings_original.nes`
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the patcher:
   ```bash
   python patch_rom.py
   ```

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
