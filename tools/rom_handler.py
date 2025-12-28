"""
ROM Handler for Bandit Kings of Ancient China
Provides safe reading/writing of ROM data with structure awareness
"""

import struct
from typing import List, Dict, Tuple, Optional
import os


class ROMHandler:
    """Handles NES ROM file operations for Bandit Kings of Ancient China"""

    # Memory offsets (PRG ROM addresses)
    GENERAL_DATA_OFFSET = 0x1C010
    GENERAL_DATA_SIZE = 16
    TOTAL_GENERALS = 108

    CITY_DATA_OFFSET = 0x1E010
    CITY_DATA_SIZE = 32
    TOTAL_CITIES = 64

    MARKET_PRICES_OFFSET = 0x22010
    PRODUCTION_RATES_OFFSET = 0x22110
    AI_BEHAVIOR_OFFSET = 0x24010

    def __init__(self, rom_path: str):
        """Load ROM file into memory"""
        if not os.path.exists(rom_path):
            raise FileNotFoundError(f"ROM file not found: {rom_path}")

        with open(rom_path, 'rb') as f:
            self.rom_data = bytearray(f.read())

        self.original_size = len(self.rom_data)
        print(f"Loaded ROM: {len(self.rom_data)} bytes")

    def save(self, output_path: str):
        """Save modified ROM to file"""
        with open(output_path, 'wb') as f:
            f.write(self.rom_data)
        print(f"Saved modified ROM to: {output_path}")

    def read_byte(self, offset: int) -> int:
        """Read single byte from ROM"""
        return self.rom_data[offset]

    def write_byte(self, offset: int, value: int):
        """Write single byte to ROM"""
        self.rom_data[offset] = value & 0xFF

    def read_word(self, offset: int) -> int:
        """Read 2-byte word (little-endian) from ROM"""
        return struct.unpack_from('<H', self.rom_data, offset)[0]

    def write_word(self, offset: int, value: int):
        """Write 2-byte word (little-endian) to ROM"""
        struct.pack_into('<H', self.rom_data, offset, value & 0xFFFF)

    def get_general_offset(self, general_id: int) -> int:
        """Get ROM offset for a specific general's data"""
        if not 0 <= general_id < self.TOTAL_GENERALS:
            raise ValueError(f"Invalid general ID: {general_id}")
        return self.GENERAL_DATA_OFFSET + (general_id * self.GENERAL_DATA_SIZE)

    def get_city_offset(self, city_id: int) -> int:
        """Get ROM offset for a specific city's data"""
        if not 0 <= city_id < self.TOTAL_CITIES:
            raise ValueError(f"Invalid city ID: {city_id}")
        return self.CITY_DATA_OFFSET + (city_id * self.CITY_DATA_SIZE)

    def read_general(self, general_id: int) -> Dict:
        """Read all data for a general"""
        offset = self.get_general_offset(general_id)

        return {
            'id': self.read_byte(offset + 0x00),
            'leadership': self.read_byte(offset + 0x01),
            'intelligence': self.read_byte(offset + 0x02),
            'strength': self.read_byte(offset + 0x03),
            'luck': self.read_byte(offset + 0x04),
            'weapon_type': self.read_byte(offset + 0x05),
            'special_ability': self.read_byte(offset + 0x06),
            'starting_city': self.read_byte(offset + 0x07),
            'loyalty': self.read_byte(offset + 0x08),
            'affiliation': self.read_byte(offset + 0x09),
            'recruitment_difficulty': self.read_byte(offset + 0x0A),
            'character_class': self.read_byte(offset + 0x0B),
            'name_pointer': self.read_word(offset + 0x0C),
            'portrait_id': self.read_word(offset + 0x0E),
        }

    def write_general(self, general_id: int, data: Dict):
        """Write all data for a general"""
        offset = self.get_general_offset(general_id)

        if 'id' in data:
            self.write_byte(offset + 0x00, data['id'])
        if 'leadership' in data:
            self.write_byte(offset + 0x01, data['leadership'])
        if 'intelligence' in data:
            self.write_byte(offset + 0x02, data['intelligence'])
        if 'strength' in data:
            self.write_byte(offset + 0x03, data['strength'])
        if 'luck' in data:
            self.write_byte(offset + 0x04, data['luck'])
        if 'weapon_type' in data:
            self.write_byte(offset + 0x05, data['weapon_type'])
        if 'special_ability' in data:
            self.write_byte(offset + 0x06, data['special_ability'])
        if 'starting_city' in data:
            self.write_byte(offset + 0x07, data['starting_city'])
        if 'loyalty' in data:
            self.write_byte(offset + 0x08, data['loyalty'])
        if 'affiliation' in data:
            self.write_byte(offset + 0x09, data['affiliation'])
        if 'recruitment_difficulty' in data:
            self.write_byte(offset + 0x0A, data['recruitment_difficulty'])
        if 'character_class' in data:
            self.write_byte(offset + 0x0B, data['character_class'])

    def read_city(self, city_id: int) -> Dict:
        """Read all data for a city"""
        offset = self.get_city_offset(city_id)

        connected_cities = [
            self.read_byte(offset + 0x12 + i)
            for i in range(6)
        ]

        return {
            'id': self.read_byte(offset + 0x00),
            'size': self.read_byte(offset + 0x01),
            'gold': self.read_word(offset + 0x02),
            'rice': self.read_word(offset + 0x04),
            'soldiers': self.read_word(offset + 0x06),
            'weapons': self.read_word(offset + 0x08),
            'terrain': self.read_byte(offset + 0x0A),
            'defense': self.read_byte(offset + 0x0B),
            'population': self.read_byte(offset + 0x0C),
            'governor': self.read_byte(offset + 0x0D),
            'ruling_force': self.read_byte(offset + 0x0E),
            'gold_production': self.read_byte(offset + 0x0F),
            'rice_production': self.read_byte(offset + 0x10),
            'recruitment_rate': self.read_byte(offset + 0x11),
            'connected_cities': connected_cities,
            'map_x': self.read_word(offset + 0x18),
            'map_y': self.read_word(offset + 0x1A),
        }

    def write_city(self, city_id: int, data: Dict):
        """Write all data for a city"""
        offset = self.get_city_offset(city_id)

        if 'size' in data:
            self.write_byte(offset + 0x01, data['size'])
        if 'gold' in data:
            self.write_word(offset + 0x02, data['gold'])
        if 'rice' in data:
            self.write_word(offset + 0x04, data['rice'])
        if 'soldiers' in data:
            self.write_word(offset + 0x06, data['soldiers'])
        if 'weapons' in data:
            self.write_word(offset + 0x08, data['weapons'])
        if 'terrain' in data:
            self.write_byte(offset + 0x0A, data['terrain'])
        if 'defense' in data:
            self.write_byte(offset + 0x0B, data['defense'])
        if 'population' in data:
            self.write_byte(offset + 0x0C, data['population'])
        if 'governor' in data:
            self.write_byte(offset + 0x0D, data['governor'])
        if 'ruling_force' in data:
            self.write_byte(offset + 0x0E, data['ruling_force'])
        if 'gold_production' in data:
            self.write_byte(offset + 0x0F, data['gold_production'])
        if 'rice_production' in data:
            self.write_byte(offset + 0x10, data['rice_production'])
        if 'recruitment_rate' in data:
            self.write_byte(offset + 0x11, data['recruitment_rate'])
        if 'connected_cities' in data:
            for i, city in enumerate(data['connected_cities'][:6]):
                self.write_byte(offset + 0x12 + i, city)
