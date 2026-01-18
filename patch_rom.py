#!/usr/bin/env python3
"""
Bandit Kings of Ancient China - ROM Patcher
Main script for applying enhancements to the ROM
"""

import argparse
import sys
import os
from colorama import init, Fore, Style

# Initialize colorama for colored output
init()

from tools import (
    ROMHandler,
    GeneralShuffler,
    StatRandomizer,
    GeographyModifier,
    GameEnhancements
)


def print_banner():
    """Print cool ASCII banner"""
    banner = f"""
{Fore.YELLOW}╔═══════════════════════════════════════════════════════════╗
║  BANDIT KINGS OF ANCIENT CHINA - Enhanced Edition        ║
║  ROM Patcher v1.0                                         ║
╚═══════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    print(banner)


def apply_preset_chaos(rom_path: str, output_path: str, seed: int = None):
    """Apply CHAOS preset - maximum randomization"""
    print(f"\n{Fore.RED}[CHAOS MODE]{Style.RESET_ALL} Applying maximum randomization...\n")

    try:
        rom = ROMHandler(rom_path)

        # Shuffle everything
        shuffler = GeneralShuffler(rom, seed)
        shuffler.shuffle_all_generals(preserve_groups=False)
        shuffler.scatter_heroes(30)

        # Randomize stats heavily
        randomizer = StatRandomizer(rom, seed)
        randomizer.randomize_all_stats(variance=0.9)
        randomizer.create_super_generals(10)
        randomizer.randomize_abilities()

        # Modify geography
        geo = GeographyModifier(rom, seed)
        geo.randomize_terrain()
        geo.shuffle_city_importance()
        geo.randomize_connections()
        geo.create_rich_poor_divide()

        # Apply chaos difficulty
        enhancements = GameEnhancements(rom, seed)
        enhancements.apply_all_enhancements(difficulty='chaos')

        rom.save(output_path)
        print(f"\n{Fore.GREEN}✓{Style.RESET_ALL} Chaos mode ROM saved to: {output_path}")
    except (FileNotFoundError, PermissionError, IOError, ValueError, IndexError) as e:
        print(f"\n{Fore.RED}✗ Error applying chaos preset:{Style.RESET_ALL} {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Fore.RED}✗ Unexpected error:{Style.RESET_ALL} {e}")
        sys.exit(1)


def apply_preset_balanced(rom_path: str, output_path: str, seed: int = None):
    """Apply BALANCED preset - moderate improvements"""
    print(f"\n{Fore.CYAN}[BALANCED MODE]{Style.RESET_ALL} Applying balanced enhancements...\n")

    try:
        rom = ROMHandler(rom_path)

        # Balanced general distribution
        shuffler = GeneralShuffler(rom, seed)
        shuffler.balance_factions()
        shuffler.scatter_heroes(15)

        # Moderate stat changes
        randomizer = StatRandomizer(rom, seed)
        randomizer.randomize_all_stats(variance=0.3)
        randomizer.create_specialists()
        randomizer.create_super_generals(5)

        # Strategic geography
        geo = GeographyModifier(rom, seed)
        geo.create_chokepoints(8)
        geo.create_border_regions()
        geo.balance_map_resources()

        # Balanced enhancements
        enhancements = GameEnhancements(rom, seed)
        enhancements.apply_all_enhancements(difficulty='normal')

        rom.save(output_path)
        print(f"\n{Fore.GREEN}✓{Style.RESET_ALL} Balanced ROM saved to: {output_path}")
    except (FileNotFoundError, PermissionError, IOError, ValueError, IndexError) as e:
        print(f"\n{Fore.RED}✗ Error applying balanced preset:{Style.RESET_ALL} {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Fore.RED}✗ Unexpected error:{Style.RESET_ALL} {e}")
        sys.exit(1)


def apply_preset_enhanced(rom_path: str, output_path: str, seed: int = None):
    """Apply ENHANCED preset - subtle improvements"""
    print(f"\n{Fore.GREEN}[ENHANCED MODE]{Style.RESET_ALL} Applying subtle enhancements...\n")

    try:
        rom = ROMHandler(rom_path)

        # Minimal shuffling, preserve feel
        shuffler = GeneralShuffler(rom, seed)
        shuffler.scatter_heroes(10)

        # Light stat tweaks
        randomizer = StatRandomizer(rom, seed)
        randomizer.randomize_all_stats(variance=0.15)
        randomizer.create_super_generals(3)

        # Minor geography changes
        geo = GeographyModifier(rom, seed)
        geo.create_chokepoints(5)
        geo.balance_map_resources()

        # Conservative enhancements
        enhancements = GameEnhancements(rom, seed)
        enhancements.create_legendary_items()
        enhancements.create_hidden_champions(5)
        enhancements.create_trade_hubs(4)

        rom.save(output_path)
        print(f"\n{Fore.GREEN}✓{Style.RESET_ALL} Enhanced ROM saved to: {output_path}")
    except (FileNotFoundError, PermissionError, IOError, ValueError, IndexError) as e:
        print(f"\n{Fore.RED}✗ Error applying enhanced preset:{Style.RESET_ALL} {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Fore.RED}✗ Unexpected error:{Style.RESET_ALL} {e}")
        sys.exit(1)


def apply_custom(args):
    """Apply custom modifications based on flags"""
    print(f"\n{Fore.MAGENTA}[CUSTOM MODE]{Style.RESET_ALL} Applying custom modifications...\n")

    try:
        rom = ROMHandler(args.input)
        seed = args.seed

        # Shuffle generals
        if args.shuffle_generals:
            print(f"{Fore.YELLOW}→{Style.RESET_ALL} Shuffling generals...")
            shuffler = GeneralShuffler(rom, seed)

            if args.preserve_groups:
                shuffler.shuffle_all_generals(preserve_groups=True)
            else:
                shuffler.shuffle_all_generals(preserve_groups=False)

            if args.wanderers:
                shuffler.scatter_heroes(args.wanderers)

        # Randomize stats
        if args.randomize_stats:
            print(f"{Fore.YELLOW}→{Style.RESET_ALL} Randomizing stats...")
            randomizer = StatRandomizer(rom, seed)
            randomizer.randomize_all_stats(variance=args.stat_variance)

            if args.create_specialists:
                randomizer.create_specialists()

            if args.super_generals > 0:
                randomizer.create_super_generals(args.super_generals)

            if args.randomize_abilities:
                randomizer.randomize_abilities()

        # Modify geography
        if args.modify_geography:
            print(f"{Fore.YELLOW}→{Style.RESET_ALL} Modifying geography...")
            geo = GeographyModifier(rom, seed)

            if args.randomize_terrain:
                geo.randomize_terrain()

            if args.shuffle_cities:
                geo.shuffle_city_importance()

            if args.chokepoints > 0:
                geo.create_chokepoints(args.chokepoints)

            if args.randomize_connections:
                geo.randomize_connections()

        # Apply enhancements
        if args.enhancements:
            print(f"{Fore.YELLOW}→{Style.RESET_ALL} Applying enhancements...")
            enhancements = GameEnhancements(rom, seed)
            enhancements.apply_all_enhancements(difficulty=args.difficulty)

        rom.save(args.output)
        print(f"\n{Fore.GREEN}✓{Style.RESET_ALL} Custom ROM saved to: {args.output}")
    except (FileNotFoundError, PermissionError, IOError, ValueError, IndexError) as e:
        print(f"\n{Fore.RED}✗ Error applying custom modifications:{Style.RESET_ALL} {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Fore.RED}✗ Unexpected error:{Style.RESET_ALL} {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Enhance Bandit Kings of Ancient China NES ROM',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Presets:
  chaos      - Maximum randomization, wild gameplay
  balanced   - Moderate changes, improved balance
  enhanced   - Subtle improvements, original feel

Examples:
  python patch_rom.py --preset chaos
  python patch_rom.py --preset balanced --seed 12345
  python patch_rom.py --shuffle-generals --randomize-stats
        """
    )

    # Basic options
    parser.add_argument('-i', '--input', default='bandit_kings_original.nes',
                       help='Input ROM file (default: bandit_kings_original.nes)')
    parser.add_argument('-o', '--output', default='bandit_kings_enhanced.nes',
                       help='Output ROM file (default: bandit_kings_enhanced.nes)')
    parser.add_argument('--seed', type=int, default=None,
                       help='Random seed for reproducible results')

    # Presets
    parser.add_argument('--preset', choices=['chaos', 'balanced', 'enhanced'],
                       help='Use a preset configuration')

    # General options
    parser.add_argument('--shuffle-generals', action='store_true',
                       help='Shuffle general placements')
    parser.add_argument('--preserve-groups', action='store_true',
                       help='Keep some character groups together when shuffling')
    parser.add_argument('--wanderers', type=int, default=15,
                       help='Number of wandering heroes (default: 15)')

    # Stat options
    parser.add_argument('--randomize-stats', action='store_true',
                       help='Randomize general statistics')
    parser.add_argument('--stat-variance', type=float, default=0.3,
                       help='Stat randomization variance 0.0-1.0 (default: 0.3)')
    parser.add_argument('--create-specialists', action='store_true',
                       help='Create specialist generals')
    parser.add_argument('--super-generals', type=int, default=5,
                       help='Number of super generals to create (default: 5)')
    parser.add_argument('--randomize-abilities', action='store_true',
                       help='Randomize special abilities')

    # Geography options
    parser.add_argument('--modify-geography', action='store_true',
                       help='Modify geography and terrain')
    parser.add_argument('--randomize-terrain', action='store_true',
                       help='Randomize terrain types')
    parser.add_argument('--shuffle-cities', action='store_true',
                       help='Shuffle city importance')
    parser.add_argument('--chokepoints', type=int, default=8,
                       help='Number of fortress chokepoints (default: 8)')
    parser.add_argument('--randomize-connections', action='store_true',
                       help='Randomize city connections')

    # Enhancement options
    parser.add_argument('--enhancements', action='store_true',
                       help='Apply gameplay enhancements')
    parser.add_argument('--difficulty', choices=['easy', 'normal', 'hard', 'chaos'],
                       default='normal', help='Difficulty level (default: normal)')

    args = parser.parse_args()

    print_banner()

    # Check if input file exists
    if not os.path.exists(args.input):
        print(f"{Fore.RED}✗ Error:{Style.RESET_ALL} Input ROM not found: {args.input}")
        print(f"\nPlease place your ROM file as: {args.input}")
        print("Or specify a different input file with -i/--input")
        sys.exit(1)

    # Apply preset or custom
    if args.preset:
        if args.preset == 'chaos':
            apply_preset_chaos(args.input, args.output, args.seed)
        elif args.preset == 'balanced':
            apply_preset_balanced(args.input, args.output, args.seed)
        elif args.preset == 'enhanced':
            apply_preset_enhanced(args.input, args.output, args.seed)
    else:
        # Check if any custom options specified
        has_custom = (args.shuffle_generals or args.randomize_stats or
                     args.modify_geography or args.enhancements)

        if not has_custom:
            print(f"{Fore.YELLOW}! No modifications specified{Style.RESET_ALL}")
            print("\nUse --preset for quick start, or specify custom options.")
            print("Run with --help to see all options.")
            sys.exit(1)

        apply_custom(args)

    print(f"\n{Fore.CYAN}═══════════════════════════════════════════════{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Success!{Style.RESET_ALL} Your enhanced ROM is ready to play!")
    print(f"{Fore.CYAN}═══════════════════════════════════════════════{Style.RESET_ALL}\n")


if __name__ == '__main__':
    main()
