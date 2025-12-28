# Usage Examples

## Quick Start Examples

### 1. Maximum Chaos Mode
```bash
python3 patch_rom.py --preset chaos
```
Creates a completely wild experience:
- All generals randomly distributed
- Stats heavily randomized
- Terrain and geography shuffled
- Unpredictable gameplay every time

### 2. Balanced Enhancement
```bash
python3 patch_rom.py --preset balanced
```
The recommended preset:
- Generals distributed across factions fairly
- Moderate stat adjustments
- Strategic chokepoints added
- Enhanced but familiar gameplay

### 3. Subtle Improvements
```bash
python3 patch_rom.py --preset enhanced
```
For purists who want the original feel:
- Minimal changes to core game
- A few hidden champions to discover
- Some legendary item locations
- Trade hubs for economic gameplay

## Custom Modifications

### Shuffle Generals Only
```bash
python3 patch_rom.py \
  --shuffle-generals \
  --wanderers 20 \
  --output custom_generals.nes
```
Randomizes where generals start, creates 20 wandering heroes.

### Stat Randomization
```bash
python3 patch_rom.py \
  --randomize-stats \
  --stat-variance 0.5 \
  --super-generals 8 \
  --create-specialists \
  --output custom_stats.nes
```
Creates varied generals with specialists and super-powered heroes.

### Geography Overhaul
```bash
python3 patch_rom.py \
  --modify-geography \
  --randomize-terrain \
  --shuffle-cities \
  --chokepoints 12 \
  --randomize-connections \
  --output custom_map.nes
```
Completely restructures the game world.

### Everything Custom
```bash
python3 patch_rom.py \
  --shuffle-generals \
  --preserve-groups \
  --randomize-stats \
  --stat-variance 0.4 \
  --modify-geography \
  --enhancements \
  --difficulty hard \
  --super-generals 10 \
  --wanderers 25 \
  --output ultimate_challenge.nes
```

## Reproducible Builds

Use seeds to create the same ROM every time:

```bash
# Create with seed
python3 patch_rom.py --preset balanced --seed 42069

# Share the seed with friends to play the same version
python3 patch_rom.py --preset balanced --seed 42069
```

## Difficulty Variations

### Easy Mode (Beginner Friendly)
```bash
python3 patch_rom.py \
  --preset enhanced \
  --difficulty easy \
  --output easy_mode.nes
```

### Hard Mode (Veteran Players)
```bash
python3 patch_rom.py \
  --preset balanced \
  --difficulty hard \
  --output hard_mode.nes
```

### Chaos Mode (Roguelike Experience)
```bash
python3 patch_rom.py \
  --preset chaos \
  --difficulty chaos \
  --seed $(date +%s) \
  --output chaos_$(date +%Y%m%d_%H%M%S).nes
```
Creates a new unique ROM every time with timestamp.

## Theme-Based Builds

### "Bandit Paradise" - For the Thematic Player
```bash
python3 patch_rom.py \
  --shuffle-generals \
  --preserve-groups \
  --enhancements \
  --output bandit_paradise.nes
```
Uses enhancement features that create bandit havens and outlaw themes.

### "Empire Builder" - Economic Focus
```bash
python3 patch_rom.py \
  --modify-geography \
  --enhancements \
  --output empire_builder.nes
```
Creates trade hubs and economic centers for commerce-focused play.

### "Warlord Challenge" - Military Focus
```bash
python3 patch_rom.py \
  --modify-geography \
  --chokepoints 15 \
  --difficulty hard \
  --output warlord_challenge.nes
```
Creates heavily fortified regions for tactical warfare.

### "Hero Collector" - Recruitment Focus
```bash
python3 patch_rom.py \
  --shuffle-generals \
  --wanderers 40 \
  --enhancements \
  --output hero_collector.nes
```
Maximizes wandering heroes and recruitment opportunities.

## Advanced Usage

### Multiple Versions for Comparison
```bash
# Create three different versions
for preset in chaos balanced enhanced; do
  python3 patch_rom.py \
    --preset $preset \
    --seed 12345 \
    --output "bkoc_${preset}_seed12345.nes"
done
```

### Tournament Setup (Same ROM for All Players)
```bash
# Generate tournament ROM with specific seed
python3 patch_rom.py \
  --preset balanced \
  --seed 88888 \
  --output tournament_2024.nes

# All players use tournament_2024.nes
# Everyone has the same general/city layout
```

### Daily Challenge
```bash
# Create daily challenge based on date
python3 patch_rom.py \
  --preset chaos \
  --seed $(date +%Y%m%d) \
  --output daily_$(date +%Y%m%d).nes
```

## Scripting Examples

### Batch Generation
```bash
#!/bin/bash
# Generate 10 different chaos ROMs

for i in {1..10}; do
  echo "Generating ROM #$i..."
  python3 patch_rom.py \
    --preset chaos \
    --seed $i \
    --output "chaos_variant_$i.nes"
done
```

### Quality Presets
```bash
#!/bin/bash
# Create a "greatest hits" collection

# Casual friendly
python3 patch_rom.py --preset enhanced --output bkoc_casual.nes

# Hardcore challenge
python3 patch_rom.py --preset balanced --difficulty hard --output bkoc_hardcore.nes

# Speed run edition (balanced start)
python3 patch_rom.py --preset balanced --seed 99999 --output bkoc_speedrun.nes

# Chaos edition (for streamers)
python3 patch_rom.py --preset chaos --output bkoc_chaos.nes
```

## Testing Your Patches

After creating a patched ROM:

1. **Load in emulator** (FCEUX, Mesen, etc.)
2. **Check the intro** - Should play normally
3. **Start new game** - Verify it doesn't crash
4. **Check generals** - Open status screens to see changes
5. **Visit cities** - Verify resources and stats look reasonable
6. **Save state** - Test that saves work properly

## Troubleshooting

### Patch seems too extreme
- Lower `--stat-variance` (try 0.2 instead of 0.5)
- Use `--preserve-groups` when shuffling
- Try `enhanced` preset instead of `chaos`

### Game crashes or glitches
- Verify input ROM is correct version
- Try with a different preset
- Check emulator compatibility

### Want to revert
- Keep your original ROM safe
- Each patch creates a NEW file
- Original is never modified

## Pro Tips

1. **Always keep the original ROM safe and untouched**
2. **Use seeds for reproducible builds**
3. **Start with `balanced` preset before going chaos**
4. **Share seeds, not ROM files**
5. **Test in an emulator before playing seriously**
6. **Create multiple versions to find your favorite**
7. **Document your favorite seeds for future use**

## Community Challenges

Share your favorite configurations (seeds + options):

```bash
# Example community challenge
python3 patch_rom.py \
  --preset balanced \
  --seed 13579 \
  --difficulty hard \
  --wanderers 30 \
  --output community_challenge_01.nes
```

Players can recreate the exact same ROM and compete!

---

**Have fun and experiment! Every seed creates a unique adventure!**
