"""
Master monster data.

>>> Rubric requirement 2 (nested list): every row is a related record.
    [Name, Difficulty, Rarity, Ability]

This file has ONE job: hold the data. GameState (game_state.py) makes a
working copy of it every time a game starts.
"""

MONSTER_TEMPLATES = [
    ["Leafling", 3, "Common", "Vine Whip"],
    ["Flameling", 4, "Common", "Fire Blast"],
    ["Aquafin", 5, "Uncommon", "Water Splash"],
    ["Voltwing", 6, "Uncommon", "Thunder Strike"],
    ["Rockhorn", 7, "Rare", "Stone Crash"],
    ["Shadowfang", 9, "Legendary", "Dark Bite"],
    ["Sandcoil", 4, "Common", "Sand Toss"],
    ["Frostail", 6, "Uncommon", "Ice Shard"],
    ["Stormtail", 10, "Epic", "Thunder Storm"],
]
