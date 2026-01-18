"""
Stat Randomizer for Bandit Kings of Ancient China
Rebalances and randomizes general statistics for varied gameplay
"""

import random
from typing import Dict, List, Tuple
from .rom_handler import ROMHandler


class StatRandomizer:
    """Randomizes and rebalances general statistics"""

    def __init__(self, rom: ROMHandler, seed: int = None):
        self.rom = rom
        if seed is not None:
            random.seed(seed)

    def randomize_all_stats(self, variance: float = 0.3):
        """
        Randomize all general stats with controlled variance

        Args:
            variance: How much to vary from original (0.0 = no change, 1.0 = completely random)
        """
        # Validate input
        if not 0.0 <= variance <= 1.0:
            raise ValueError(f"variance must be between 0.0 and 1.0, got {variance}")

        print(f"Randomizing all general stats (variance: {variance})...")

        for gen_id in range(self.rom.TOTAL_GENERALS):
            general = self.rom.read_general(gen_id)

            # Randomize each stat
            new_stats = {
                'leadership': self._randomize_stat(general['leadership'], variance),
                'intelligence': self._randomize_stat(general['intelligence'], variance),
                'strength': self._randomize_stat(general['strength'], variance),
                'luck': self._randomize_stat(general['luck'], variance),
            }

            self.rom.write_general(gen_id, new_stats)

        print(f"Randomized stats for {self.rom.TOTAL_GENERALS} generals")

    def _randomize_stat(self, original: int, variance: float) -> int:
        """
        Randomize a single stat value

        Args:
            original: Original stat value
            variance: How much to vary (0.0 - 1.0)

        Returns:
            New stat value (clamped to 0-99)
        """
        if variance == 0:
            return original

        # Calculate variance range
        max_change = int(99 * variance)
        change = random.randint(-max_change, max_change)

        # If completely random variance
        if variance >= 0.9:
            return random.randint(1, 99)

        # Apply change and clamp
        new_value = original + change
        return max(1, min(99, new_value))

    def create_super_generals(self, count: int = 5):
        """
        Create a few extremely powerful generals

        Args:
            count: Number of super generals to create
        """
        # Validate input
        if count < 0:
            raise ValueError(f"count must be non-negative, got {count}")
        if count > self.rom.TOTAL_GENERALS:
            raise ValueError(f"count ({count}) cannot exceed total generals ({self.rom.TOTAL_GENERALS})")

        print(f"Creating {count} super generals...")

        generals = list(range(self.rom.TOTAL_GENERALS))
        random.shuffle(generals)

        for i in range(min(count, len(generals))):
            gen_id = generals[i]

            super_stats = {
                'leadership': random.randint(90, 99),
                'intelligence': random.randint(90, 99),
                'strength': random.randint(90, 99),
                'luck': random.randint(85, 99),
                'special_ability': random.randint(5, 7),  # Powerful abilities
            }

            self.rom.write_general(gen_id, super_stats)

    def create_specialists(self):
        """
        Create specialists - generals who excel in one area but are weak in others
        """
        print("Creating specialist generals...")

        stat_types = ['leadership', 'intelligence', 'strength', 'luck']

        for gen_id in range(self.rom.TOTAL_GENERALS):
            if random.random() < 0.3:  # 30% chance to be specialist
                # Pick specialty
                specialty = random.choice(stat_types)

                stats = {
                    'leadership': random.randint(20, 40),
                    'intelligence': random.randint(20, 40),
                    'strength': random.randint(20, 40),
                    'luck': random.randint(20, 40),
                }

                # Boost specialty stat
                stats[specialty] = random.randint(80, 99)

                # Sometimes boost a secondary stat
                if random.random() < 0.3:
                    secondary = random.choice([s for s in stat_types if s != specialty])
                    stats[secondary] = random.randint(60, 75)

                self.rom.write_general(gen_id, stats)

    def balance_stat_totals(self, target_total: int = 200):
        """
        Balance all generals to have similar total stats

        Args:
            target_total: Target sum of all four main stats
        """
        # Validate input - target_total should be reasonable (4-396 for 4 stats with range 1-99)
        if not 4 <= target_total <= 396:
            raise ValueError(f"target_total must be between 4 and 396, got {target_total}")

        print(f"Balancing generals to {target_total} total stat points...")

        for gen_id in range(self.rom.TOTAL_GENERALS):
            general = self.rom.read_general(gen_id)

            # Get current stats
            stats = {
                'leadership': general['leadership'],
                'intelligence': general['intelligence'],
                'strength': general['strength'],
                'luck': general['luck'],
            }

            # Calculate current total
            current_total = sum(stats.values())

            if current_total == 0:
                current_total = 1  # Avoid division by zero

            # Scale to target
            scale_factor = target_total / current_total

            new_stats = {}
            for stat_name, value in stats.items():
                new_value = int(value * scale_factor)
                # Add some randomness
                new_value += random.randint(-5, 5)
                new_stats[stat_name] = max(1, min(99, new_value))

            # Ensure we hit the target (adjust largest stat if needed)
            current_sum = sum(new_stats.values())
            if current_sum != target_total:
                diff = target_total - current_sum
                # Find stat with most room to adjust
                if diff > 0:
                    # Need to increase
                    stat_to_adjust = max(new_stats.keys(),
                                       key=lambda k: 99 - new_stats[k])
                else:
                    # Need to decrease
                    stat_to_adjust = max(new_stats.keys(),
                                       key=lambda k: new_stats[k] - 1)

                new_stats[stat_to_adjust] = max(1, min(99,
                                                       new_stats[stat_to_adjust] + diff))

            self.rom.write_general(gen_id, new_stats)

    def randomize_abilities(self):
        """Randomize special abilities and weapon types"""
        print("Randomizing special abilities and weapons...")

        for gen_id in range(self.rom.TOTAL_GENERALS):
            new_data = {
                'weapon_type': random.randint(0, 7),
                'special_ability': random.randint(0, 7),
                'character_class': random.randint(0, 5),
            }

            self.rom.write_general(gen_id, new_data)

    def create_weakness_system(self):
        """
        Create interesting weakness/strength combinations
        Some generals great at war, terrible at politics, etc.
        """
        print("Creating weakness/strength system...")

        for gen_id in range(self.rom.TOTAL_GENERALS):
            # Roll for archetype
            archetype = random.choice([
                'warrior',      # High STR, low INT
                'strategist',   # High INT, low STR
                'leader',       # High LDR, balanced
                'lucky',        # High LCK, low everything else
                'balanced',     # All moderate
                'unstable',     # Random high/low
            ])

            stats = self._get_archetype_stats(archetype)
            self.rom.write_general(gen_id, stats)

    def _get_archetype_stats(self, archetype: str) -> Dict:
        """Generate stats based on archetype"""
        if archetype == 'warrior':
            return {
                'strength': random.randint(75, 95),
                'leadership': random.randint(40, 60),
                'intelligence': random.randint(20, 40),
                'luck': random.randint(30, 50),
            }
        elif archetype == 'strategist':
            return {
                'intelligence': random.randint(75, 95),
                'leadership': random.randint(50, 70),
                'strength': random.randint(20, 40),
                'luck': random.randint(30, 50),
            }
        elif archetype == 'leader':
            return {
                'leadership': random.randint(80, 99),
                'intelligence': random.randint(50, 70),
                'strength': random.randint(50, 70),
                'luck': random.randint(40, 60),
            }
        elif archetype == 'lucky':
            return {
                'luck': random.randint(85, 99),
                'leadership': random.randint(20, 50),
                'intelligence': random.randint(20, 50),
                'strength': random.randint(20, 50),
            }
        elif archetype == 'balanced':
            base = random.randint(45, 60)
            # Ensure all values stay in 1-99 range by clamping
            return {
                'leadership': max(1, min(99, base + random.randint(-10, 10))),
                'intelligence': max(1, min(99, base + random.randint(-10, 10))),
                'strength': max(1, min(99, base + random.randint(-10, 10))),
                'luck': max(1, min(99, base + random.randint(-10, 10))),
            }
        else:  # unstable
            return {
                'leadership': random.randint(1, 99),
                'intelligence': random.randint(1, 99),
                'strength': random.randint(1, 99),
                'luck': random.randint(1, 99),
            }
