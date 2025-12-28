"""
General Shuffler for Bandit Kings of Ancient China
Randomizes general placements, affiliations, and creates interesting scenarios
"""

import random
from typing import List, Dict, Set
from .rom_handler import ROMHandler


class GeneralShuffler:
    """Shuffles generals across cities and factions"""

    def __init__(self, rom: ROMHandler, seed: int = None):
        self.rom = rom
        if seed is not None:
            random.seed(seed)

    def shuffle_all_generals(self, preserve_groups: bool = False):
        """
        Shuffle all generals across cities and factions

        Args:
            preserve_groups: If True, keeps some historical character groups together
        """
        print("Shuffling all generals...")

        # Read all generals
        generals = []
        for i in range(self.rom.TOTAL_GENERALS):
            gen = self.rom.read_general(i)
            gen['original_id'] = i
            generals.append(gen)

        # Get all valid cities
        cities = list(range(self.rom.TOTAL_CITIES))

        # Shuffle cities for generals
        if preserve_groups:
            shuffled_positions = self._shuffle_with_groups(generals, cities)
        else:
            shuffled_positions = self._shuffle_completely_random(generals, cities)

        # Apply shuffled positions
        for general, new_city, new_affiliation in shuffled_positions:
            gen_id = general['original_id']
            self.rom.write_general(gen_id, {
                'starting_city': new_city,
                'affiliation': new_affiliation
            })

        print(f"Shuffled {len(generals)} generals across {len(cities)} cities")

    def _shuffle_completely_random(self, generals: List[Dict], cities: List[int]) -> List:
        """Completely random shuffle"""
        results = []

        # Define factions (0-15)
        factions = list(range(16))

        for general in generals:
            # Random city
            city = random.choice(cities)
            # Random faction
            faction = random.choice(factions)

            results.append((general, city, faction))

        return results

    def _shuffle_with_groups(self, generals: List[Dict], cities: List[int]) -> List:
        """
        Shuffle while keeping some character groups together
        Simulates historical alliances and friendships
        """
        results = []

        # Define character groups (based on stats similarity and lore)
        # This creates more interesting clustered starts
        num_groups = 12
        group_size = len(generals) // num_groups

        # Shuffle generals first
        shuffled_generals = generals.copy()
        random.shuffle(shuffled_generals)

        # Assign groups to cities
        for group_idx in range(num_groups):
            start = group_idx * group_size
            end = start + group_size if group_idx < num_groups - 1 else len(shuffled_generals)
            group = shuffled_generals[start:end]

            # Pick a central city for this group
            central_city = random.choice(cities)
            faction = random.randint(0, 15)

            # Get nearby cities (simulate by picking a cluster)
            city_cluster = [central_city]
            other_cities = [c for c in cities if c != central_city]
            random.shuffle(other_cities)
            city_cluster.extend(other_cities[:min(5, len(group) - 1)])

            # Assign group members to cluster
            for i, general in enumerate(group):
                city = city_cluster[i % len(city_cluster)]
                # Some variety in faction within group
                group_faction = faction if random.random() < 0.7 else random.randint(0, 15)
                results.append((general, city, group_faction))

        return results

    def create_mega_faction(self, faction_id: int, num_generals: int = 30):
        """
        Create one mega-faction with many generals for extra challenge
        """
        print(f"Creating mega-faction {faction_id} with {num_generals} generals...")

        generals = list(range(self.rom.TOTAL_GENERALS))
        random.shuffle(generals)

        # Assign first N generals to the mega-faction
        for i in range(min(num_generals, len(generals))):
            gen_id = generals[i]
            self.rom.write_general(gen_id, {
                'affiliation': faction_id,
                'loyalty': random.randint(80, 100)  # High loyalty
            })

    def scatter_heroes(self, num_wanderers: int = 20):
        """
        Make some generals start as wanderers (no affiliation)
        Creates recruitment opportunities
        """
        print(f"Creating {num_wanderers} wandering heroes...")

        generals = list(range(self.rom.TOTAL_GENERALS))
        random.shuffle(generals)

        # Make them wanderers (affiliation 0xFF typically means unaffiliated)
        for i in range(min(num_wanderers, len(generals))):
            gen_id = generals[i]
            city = random.randint(0, self.rom.TOTAL_CITIES - 1)

            self.rom.write_general(gen_id, {
                'affiliation': 0xFF,
                'starting_city': city,
                'loyalty': 0,  # No loyalty to anyone
                'recruitment_difficulty': random.randint(30, 80)
            })

    def balance_factions(self):
        """
        Distribute generals evenly across factions for balanced start
        """
        print("Balancing generals across factions...")

        num_factions = 8  # Use 8 main factions
        generals_per_faction = self.rom.TOTAL_GENERALS // num_factions

        generals = list(range(self.rom.TOTAL_GENERALS))
        random.shuffle(generals)

        for faction in range(num_factions):
            start = faction * generals_per_faction
            end = start + generals_per_faction
            if faction == num_factions - 1:
                end = len(generals)  # Last faction gets remainder

            for gen_id in generals[start:end]:
                city = random.randint(0, self.rom.TOTAL_CITIES - 1)
                self.rom.write_general(gen_id, {
                    'affiliation': faction,
                    'starting_city': city
                })

        print(f"Distributed {len(generals)} generals across {num_factions} factions")
