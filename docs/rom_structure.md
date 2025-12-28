# Bandit Kings of Ancient China - ROM Structure

## ROM Information

- **Platform**: Nintendo Entertainment System (NES)
- **Mapper**: MMC3 (Mapper 4)
- **PRG ROM**: 256 KB
- **CHR ROM**: 128 KB
- **Mirroring**: Horizontal

## Memory Map

### Character/General Data (PRG ROM)

Each general has a data structure at specific offsets:

**Base Offset**: 0x1C010 (PRG ROM)
**Entry Size**: 16 bytes per general
**Total Generals**: 108 (Suikoden's 108 Stars of Destiny)

#### General Data Structure (16 bytes)

| Offset | Size | Description                    | Range      |
|--------|------|--------------------------------|------------|
| +0x00  | 1    | Character ID                   | 0x00-0x6B  |
| +0x01  | 1    | Leadership (LDR)               | 0-99       |
| +0x02  | 1    | Intelligence (INT)             | 0-99       |
| +0x03  | 1    | Strength (STR)                 | 0-99       |
| +0x04  | 1    | Luck (LCK)                     | 0-99       |
| +0x05  | 1    | Weapon Type                    | 0x00-0x07  |
| +0x06  | 1    | Special Ability Flags          | Bitfield   |
| +0x07  | 1    | Starting City ID               | 0x00-0x3F  |
| +0x08  | 1    | Loyalty                        | 0-100      |
| +0x09  | 1    | Starting Affiliation           | 0x00-0x0F  |
| +0x0A  | 1    | Recruitment Difficulty         | 0-99       |
| +0x0B  | 1    | Character Class                | 0x00-0x05  |
| +0x0C  | 2    | Name Pointer (text table)      | Address    |
| +0x0E  | 2    | Portrait ID                    | 0x00-0x6B  |

### City/Geography Data

**Base Offset**: 0x1E010 (PRG ROM)
**Entry Size**: 32 bytes per city
**Total Cities**: 64

#### City Data Structure (32 bytes)

| Offset | Size | Description                    | Range      |
|--------|------|--------------------------------|------------|
| +0x00  | 1    | City ID                        | 0x00-0x3F  |
| +0x01  | 1    | City Size/Importance           | 1-5        |
| +0x02  | 2    | Starting Gold                  | 0-65535    |
| +0x04  | 2    | Starting Rice                  | 0-65535    |
| +0x06  | 2    | Starting Soldiers              | 0-9999     |
| +0x08  | 2    | Starting Weapons               | 0-9999     |
| +0x0A  | 1    | Terrain Type                   | 0x00-0x0F  |
| +0x0B  | 1    | Defense Rating                 | 0-99       |
| +0x0C  | 1    | Population (x100)              | 0-255      |
| +0x0D  | 1    | Governor ID                    | 0x00-0x6B  |
| +0x0E  | 1    | Ruling Force                   | 0x00-0x0F  |
| +0x0F  | 1    | Production: Gold/month         | 0-99       |
| +0x10  | 1    | Production: Rice/month         | 0-99       |
| +0x11  | 1    | Recruitment Rate               | 0-99       |
| +0x12  | 6    | Connected Cities (IDs)         | 0x00-0x3F  |
| +0x18  | 2    | X Position (map)               | 0-255      |
| +0x1A  | 2    | Y Position (map)               | 0-255      |
| +0x1C  | 4    | Reserved/Flags                 | Various    |

### Terrain/Map Data

**Base Offset**: 0x20010 (PRG ROM)
**Size**: 256x240 tiles
**Format**: 8x8 pixel tiles with metatile groupings

### Resource Tables

**Market Prices**: 0x22010 (PRG ROM)
- Gold value multipliers
- Rice prices
- Weapon costs
- Horse prices

**Production Rates**: 0x22110 (PRG ROM)
- Base production by terrain
- City size multipliers
- Season modifiers

### Special Abilities

**Base Offset**: 0x1D010 (PRG ROM)

| ID | Ability Name      | Effect                           |
|----|-------------------|----------------------------------|
| 0  | None              | No special ability               |
| 1  | Tactician         | +20% to strategy success         |
| 2  | Warrior           | +20% to combat damage            |
| 3  | Diplomat          | +30% to negotiation              |
| 4  | Spy               | Reveals enemy information        |
| 5  | Merchant          | +20% to trade income             |
| 6  | Bandit Leader     | Recruiting bonus                 |
| 7  | Strategist        | Can use advanced tactics         |

### AI Behavior Patterns

**Base Offset**: 0x24010 (PRG ROM)
**Entry Size**: 8 bytes per AI personality

| Offset | Description                    |
|--------|--------------------------------|
| +0x00  | Aggression Level (0-100)       |
| +0x01  | Expansion Priority (0-100)     |
| +0x02  | Defensive Stance (0-100)       |
| +0x03  | Diplomacy Preference (0-100)   |
| +0x04  | Resource Focus (0-100)         |
| +0x05  | Risk Taking (0-100)            |
| +0x06  | Recruitment Focus (0-100)      |
| +0x07  | Special Strategy Flags         |

## Safe Modification Ranges

These ranges can be safely modified without breaking the game:

1. **General Stats**: 0x1C010-0x1C6BF (all general data)
2. **City Resources**: 0x1E012-0x1E80F (resource values only)
3. **Market Prices**: 0x22010-0x2210F
4. **AI Behavior**: 0x24010-0x2417F
5. **Production Rates**: 0x22110-0x2220F

## Checksums

The NES ROM does not use internal checksums, but some emulators verify the header.

**iNES Header**: First 16 bytes (0x000-0x00F) - Do not modify

## Notes

- All multi-byte values are little-endian
- Character IDs are zero-indexed
- Some generals have recruitment prerequisites (check offset +0x0A)
- City connections form the strategic map network
- Terrain affects movement speed and combat bonuses
