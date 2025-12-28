"""
Geography Modifier for Bandit Kings of Ancient China
Modifies terrain, city properties, and strategic landscape
"""

import random
from typing import List, Dict
from .rom_handler import ROMHandler


class GeographyModifier:
    """Modifies geography, cities, and terrain"""

    def __init__(self, rom: ROMHandler, seed: int = None):
        self.rom = rom
        if seed is not None:
            random.seed(seed)

    def randomize_terrain(self):
        """Randomize terrain types for all cities"""
        print("Randomizing terrain types...")

        # Terrain types: 0=Plains, 1=Forest, 2=Mountains, 3=Desert,
        # 4=Swamp, 5=River, 6=Coast, 7=Highlands, etc.
        terrain_types = list(range(16))

        for city_id in range(self.rom.TOTAL_CITIES):
            city = self.rom.read_city(city_id)

            # Random terrain
            new_terrain = random.choice(terrain_types)

            # Adjust defense based on terrain
            defense_bonus = {
                0: 0,   # Plains - no bonus
                1: 10,  # Forest - some cover
                2: 25,  # Mountains - excellent defense
                3: -5,  # Desert - exposure penalty
                4: 15,  # Swamp - hard to attack
                5: 5,   # River - minor bonus
                6: 8,   # Coast - some protection
                7: 20,  # Highlands - good position
            }

            base_defense = city['defense']
            bonus = defense_bonus.get(new_terrain % 8, 0)
            new_defense = max(0, min(99, base_defense + bonus))

            self.rom.write_city(city_id, {
                'terrain': new_terrain,
                'defense': new_defense
            })

        print(f"Randomized terrain for {self.rom.TOTAL_CITIES} cities")

    def shuffle_city_importance(self):
        """Shuffle which cities are major vs minor"""
        print("Shuffling city importance levels...")

        # Create a distribution of city sizes
        sizes = []
        sizes.extend([5] * 5)   # 5 huge cities
        sizes.extend([4] * 10)  # 10 large cities
        sizes.extend([3] * 15)  # 15 medium cities
        sizes.extend([2] * 20)  # 20 small cities
        sizes.extend([1] * (self.rom.TOTAL_CITIES - 50))  # Rest are tiny

        random.shuffle(sizes)

        for city_id in range(self.rom.TOTAL_CITIES):
            if city_id < len(sizes):
                size = sizes[city_id]
            else:
                size = random.randint(1, 5)

            # Size affects population and production
            pop_multiplier = size
            production_multiplier = size * 0.6

            city = self.rom.read_city(city_id)
            base_gold_prod = city['gold_production']
            base_rice_prod = city['rice_production']

            self.rom.write_city(city_id, {
                'size': size,
                'population': min(255, int(50 * pop_multiplier)),
                'gold_production': min(99, int(base_gold_prod * production_multiplier)),
                'rice_production': min(99, int(base_rice_prod * production_multiplier)),
            })

    def create_chokepoints(self, num_fortress_cities: int = 8):
        """
        Create strategic chokepoint cities with high defense

        Args:
            num_fortress_cities: Number of fortress cities to create
        """
        print(f"Creating {num_fortress_cities} fortress chokepoints...")

        cities = list(range(self.rom.TOTAL_CITIES))
        random.shuffle(cities)

        for i in range(min(num_fortress_cities, len(cities))):
            city_id = cities[i]

            # Make it a heavily defended fortress
            self.rom.write_city(city_id, {
                'defense': random.randint(85, 99),
                'terrain': 2,  # Mountains
                'size': 4,     # Large city
                'soldiers': random.randint(5000, 9000),
                'weapons': random.randint(3000, 6000),
            })

    def randomize_connections(self):
        """
        Randomize city connections to change strategic map
        """
        print("Randomizing city connections...")

        for city_id in range(self.rom.TOTAL_CITIES):
            # Generate new random connections
            all_cities = list(range(self.rom.TOTAL_CITIES))
            all_cities.remove(city_id)  # Can't connect to self

            # Pick 3-6 random connections
            num_connections = random.randint(3, 6)
            random.shuffle(all_cities)
            connected = all_cities[:num_connections]

            # Pad with 0xFF (no connection) if less than 6
            while len(connected) < 6:
                connected.append(0xFF)

            self.rom.write_city(city_id, {
                'connected_cities': connected
            })

    def create_rich_poor_divide(self):
        """
        Create stark economic differences between cities
        """
        print("Creating economic inequality...")

        # Divide cities into rich and poor
        num_rich = self.rom.TOTAL_CITIES // 4  # 25% rich
        cities = list(range(self.rom.TOTAL_CITIES))
        random.shuffle(cities)

        rich_cities = cities[:num_rich]
        poor_cities = cities[num_rich:]

        # Make rich cities very wealthy
        for city_id in rich_cities:
            self.rom.write_city(city_id, {
                'gold': random.randint(8000, 15000),
                'rice': random.randint(6000, 12000),
                'gold_production': random.randint(70, 99),
                'rice_production': random.randint(60, 90),
                'population': random.randint(150, 255),
            })

        # Make poor cities struggling
        for city_id in poor_cities:
            self.rom.write_city(city_id, {
                'gold': random.randint(500, 2000),
                'rice': random.randint(400, 1500),
                'gold_production': random.randint(10, 30),
                'rice_production': random.randint(15, 35),
                'population': random.randint(20, 80),
            })

    def create_border_regions(self):
        """
        Create distinct border regions with unique characteristics
        """
        print("Creating border regions...")

        # Divide map into regions (approximate)
        num_regions = 8
        cities_per_region = self.rom.TOTAL_CITIES // num_regions

        for region in range(num_regions):
            start = region * cities_per_region
            end = start + cities_per_region
            if region == num_regions - 1:
                end = self.rom.TOTAL_CITIES

            # Each region gets a characteristic
            region_type = random.choice([
                'military',    # High soldiers/weapons
                'economic',    # High gold/production
                'agricultural',# High rice/food
                'fortress',    # High defense
                'populous',    # High population
                'wilderness',  # Low everything
            ])

            for city_id in range(start, end):
                mods = self._get_region_modifiers(region_type)
                self.rom.write_city(city_id, mods)

    def _get_region_modifiers(self, region_type: str) -> Dict:
        """Get city modifiers for a region type"""
        if region_type == 'military':
            return {
                'soldiers': random.randint(3000, 7000),
                'weapons': random.randint(2000, 5000),
                'defense': random.randint(60, 80),
            }
        elif region_type == 'economic':
            return {
                'gold': random.randint(5000, 12000),
                'gold_production': random.randint(60, 90),
            }
        elif region_type == 'agricultural':
            return {
                'rice': random.randint(5000, 10000),
                'rice_production': random.randint(60, 90),
            }
        elif region_type == 'fortress':
            return {
                'defense': random.randint(75, 95),
                'terrain': random.choice([2, 7]),  # Mountains or Highlands
            }
        elif region_type == 'populous':
            return {
                'population': random.randint(150, 255),
                'recruitment_rate': random.randint(70, 99),
            }
        else:  # wilderness
            return {
                'gold': random.randint(200, 1000),
                'rice': random.randint(300, 1200),
                'soldiers': random.randint(100, 800),
                'population': random.randint(10, 50),
            }

    def balance_map_resources(self):
        """
        Ensure total map resources are balanced
        """
        print("Balancing overall map resources...")

        # Calculate totals
        total_gold = 0
        total_rice = 0
        total_soldiers = 0

        for city_id in range(self.rom.TOTAL_CITIES):
            city = self.rom.read_city(city_id)
            total_gold += city['gold']
            total_rice += city['rice']
            total_soldiers += city['soldiers']

        # Target totals
        target_gold = 300000
        target_rice = 250000
        target_soldiers = 150000

        # Scale if needed
        gold_scale = target_gold / max(total_gold, 1)
        rice_scale = target_rice / max(total_rice, 1)
        soldier_scale = target_soldiers / max(total_soldiers, 1)

        for city_id in range(self.rom.TOTAL_CITIES):
            city = self.rom.read_city(city_id)

            self.rom.write_city(city_id, {
                'gold': min(65535, int(city['gold'] * gold_scale)),
                'rice': min(65535, int(city['rice'] * rice_scale)),
                'soldiers': min(9999, int(city['soldiers'] * soldier_scale)),
            })

        print(f"Scaled resources: Gold x{gold_scale:.2f}, Rice x{rice_scale:.2f}, Soldiers x{soldier_scale:.2f}")
