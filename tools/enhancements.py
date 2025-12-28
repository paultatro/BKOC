"""
Innovative Enhancements for Bandit Kings of Ancient China
Creative modifications to improve gameplay experience
"""

import random
from typing import List, Dict
from .rom_handler import ROMHandler


class GameEnhancements:
    """Innovative gameplay enhancements"""

    def __init__(self, rom: ROMHandler, seed: int = None):
        self.rom = rom
        if seed is not None:
            random.seed(seed)

    def create_legendary_items(self):
        """
        Boost certain cities to have 'legendary' weapons or special bonuses
        """
        print("Creating legendary item locations...")

        num_legendary = 5
        cities = list(range(self.rom.TOTAL_CITIES))
        random.shuffle(cities)

        for i in range(min(num_legendary, len(cities))):
            city_id = cities[i]
            city = self.rom.read_city(city_id)

            # Legendary city gets massive weapon stockpile
            self.rom.write_city(city_id, {
                'weapons': 9999,  # Max weapons
                'defense': min(99, city['defense'] + 20),
            })

        print(f"Created {num_legendary} legendary weapon caches")

    def implement_difficulty_scaling(self, difficulty: str = 'normal'):
        """
        Adjust overall game difficulty

        Args:
            difficulty: 'easy', 'normal', 'hard', 'chaos'
        """
        print(f"Implementing {difficulty} difficulty scaling...")

        if difficulty == 'easy':
            self._apply_easy_mode()
        elif difficulty == 'hard':
            self._apply_hard_mode()
        elif difficulty == 'chaos':
            self._apply_chaos_mode()
        else:
            print("Normal difficulty - no scaling applied")

    def _apply_easy_mode(self):
        """Make game easier for beginners"""
        # Boost player-likely starting positions
        for city_id in range(5):  # First few cities likely player controlled
            city = self.rom.read_city(city_id)
            self.rom.write_city(city_id, {
                'gold': int(city['gold'] * 1.5),
                'rice': int(city['rice'] * 1.5),
                'soldiers': int(city['soldiers'] * 1.3),
                'weapons': int(city['weapons'] * 1.3),
            })

        # Reduce AI general stats slightly
        for gen_id in range(self.rom.TOTAL_GENERALS):
            general = self.rom.read_general(gen_id)
            if gen_id > 10:  # Don't nerf first 10 (likely player generals)
                self.rom.write_general(gen_id, {
                    'leadership': max(1, general['leadership'] - 10),
                    'intelligence': max(1, general['intelligence'] - 10),
                })

    def _apply_hard_mode(self):
        """Make game significantly harder"""
        # Create powerful enemy factions
        for faction in range(1, 8):
            # Find all generals in this faction
            faction_generals = []
            for gen_id in range(self.rom.TOTAL_GENERALS):
                gen = self.rom.read_general(gen_id)
                if gen['affiliation'] == faction:
                    faction_generals.append(gen_id)

            # Boost their stats
            for gen_id in faction_generals:
                gen = self.rom.read_general(gen_id)
                self.rom.write_general(gen_id, {
                    'leadership': min(99, gen['leadership'] + 15),
                    'intelligence': min(99, gen['intelligence'] + 15),
                    'strength': min(99, gen['strength'] + 10),
                })

        # Give AI factions more resources
        for city_id in range(self.rom.TOTAL_CITIES):
            city = self.rom.read_city(city_id)
            if city['ruling_force'] != 0:  # Not player
                self.rom.write_city(city_id, {
                    'gold': int(city['gold'] * 1.4),
                    'rice': int(city['rice'] * 1.4),
                    'soldiers': int(city['soldiers'] * 1.3),
                })

    def _apply_chaos_mode(self):
        """Complete chaos - anything goes"""
        # Random everything
        for city_id in range(self.rom.TOTAL_CITIES):
            self.rom.write_city(city_id, {
                'gold': random.randint(100, 30000),
                'rice': random.randint(100, 25000),
                'soldiers': random.randint(50, 9999),
                'weapons': random.randint(50, 9999),
                'defense': random.randint(1, 99),
                'gold_production': random.randint(5, 99),
                'rice_production': random.randint(5, 99),
            })

        # Random general stats
        for gen_id in range(self.rom.TOTAL_GENERALS):
            self.rom.write_general(gen_id, {
                'leadership': random.randint(1, 99),
                'intelligence': random.randint(1, 99),
                'strength': random.randint(1, 99),
                'luck': random.randint(1, 99),
            })

    def create_hidden_champions(self, count: int = 10):
        """
        Create hidden champion generals with max stats in unexpected locations
        """
        print(f"Creating {count} hidden champions...")

        generals = list(range(self.rom.TOTAL_GENERALS))
        random.shuffle(generals)

        for i in range(min(count, len(generals))):
            gen_id = generals[i]

            # Max out their stats
            self.rom.write_general(gen_id, {
                'leadership': 99,
                'intelligence': 99,
                'strength': 99,
                'luck': 99,
                'special_ability': 7,  # Best ability
                'loyalty': 100,
            })

            # Put them in random remote location
            remote_city = random.randint(20, self.rom.TOTAL_CITIES - 1)
            self.rom.write_general(gen_id, {
                'starting_city': remote_city,
                'affiliation': 0xFF,  # Unaffiliated
                'recruitment_difficulty': 90,  # Hard to recruit
            })

    def implement_season_variations(self):
        """
        Modify production rates to simulate seasonal variations
        """
        print("Implementing seasonal production variations...")

        for city_id in range(self.rom.TOTAL_CITIES):
            city = self.rom.read_city(city_id)

            # Rice production varies more (agriculture seasonal)
            rice_var = random.randint(0, 30)
            # Gold production varies less (trade more stable)
            gold_var = random.randint(0, 15)

            self.rom.write_city(city_id, {
                'rice_production': max(1, city['rice_production'] + rice_var - 15),
                'gold_production': max(1, city['gold_production'] + gold_var - 7),
            })

    def create_trade_hubs(self, count: int = 6):
        """
        Create major trade hub cities with excellent gold generation
        """
        print(f"Creating {count} trade hubs...")

        cities = list(range(self.rom.TOTAL_CITIES))
        random.shuffle(cities)

        for i in range(min(count, len(cities))):
            city_id = cities[i]

            self.rom.write_city(city_id, {
                'gold': random.randint(15000, 30000),
                'gold_production': random.randint(85, 99),
                'size': 5,  # Major city
                'population': random.randint(200, 255),
                'terrain': 6,  # Coast (for trade)
            })

    def create_recruitment_paradises(self, count: int = 5):
        """
        Create cities where recruitment is extremely easy
        """
        print(f"Creating {count} recruitment paradise cities...")

        cities = list(range(self.rom.TOTAL_CITIES))
        random.shuffle(cities)

        for i in range(min(count, len(cities))):
            city_id = cities[i]

            self.rom.write_city(city_id, {
                'recruitment_rate': 99,
                'population': 255,
            })

            # Put some wandering heroes here
            generals = list(range(self.rom.TOTAL_GENERALS))
            random.shuffle(generals)

            for j in range(min(3, len(generals))):
                gen_id = generals[j]
                self.rom.write_general(gen_id, {
                    'starting_city': city_id,
                    'affiliation': 0xFF,
                    'recruitment_difficulty': random.randint(20, 50),
                })

    def implement_dynamic_loyalty(self):
        """
        Make loyalty more varied and interesting
        """
        print("Implementing dynamic loyalty system...")

        for gen_id in range(self.rom.TOTAL_GENERALS):
            general = self.rom.read_general(gen_id)

            # Different loyalty levels based on position
            if general['affiliation'] == 0xFF:  # Wanderer
                loyalty = 0
            else:
                # Varied loyalty creates betrayal opportunities
                loyalty_roll = random.random()
                if loyalty_roll < 0.2:  # 20% very loyal
                    loyalty = random.randint(90, 100)
                elif loyalty_roll < 0.5:  # 30% moderately loyal
                    loyalty = random.randint(60, 85)
                elif loyalty_roll < 0.8:  # 30% questionable loyalty
                    loyalty = random.randint(30, 60)
                else:  # 20% disloyal (ready to switch)
                    loyalty = random.randint(1, 30)

            self.rom.write_general(gen_id, {'loyalty': loyalty})

    def create_bandit_havens(self, count: int = 8):
        """
        Create bandit havens - cities with lots of soldiers but poor economy
        Perfect for the 'Bandit Kings' theme
        """
        print(f"Creating {count} bandit havens...")

        cities = list(range(self.rom.TOTAL_CITIES))
        random.shuffle(cities)

        for i in range(min(count, len(cities))):
            city_id = cities[i]

            self.rom.write_city(city_id, {
                'soldiers': random.randint(6000, 9999),
                'weapons': random.randint(4000, 7000),
                'gold': random.randint(500, 2000),  # Poor
                'rice': random.randint(800, 2500),  # Limited food
                'terrain': random.choice([1, 2, 4]),  # Forest, Mountain, or Swamp
                'defense': random.randint(70, 90),  # Well defended
            })

    def apply_all_enhancements(self, difficulty: str = 'normal'):
        """
        Apply a complete suite of enhancements
        """
        print("Applying all gameplay enhancements...")

        self.create_legendary_items()
        self.implement_difficulty_scaling(difficulty)
        self.create_hidden_champions(8)
        self.create_trade_hubs(6)
        self.create_recruitment_paradises(5)
        self.implement_dynamic_loyalty()
        self.create_bandit_havens(8)

        print("All enhancements applied!")
