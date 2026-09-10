"""
Game-wide constants: window settings, rarity colors/scores, and tunables.
Keeping these in one place means every other file imports the same values
instead of repeating "magic numbers" or hex codes.
"""

WINDOW_TITLE = "Monster Catcher"
WINDOW_SIZE = "900x700"

# Pixel-sprite color for each rarity tier (as requested: color by rarity)
RARITY_COLORS = {
    "Common": "#4CAF50",      # green
    "Uncommon": "#2196F3",    # blue
    "Rare": "#9C27B0",        # purple
    "Legendary": "#FFB300",   # gold
    "Epic": "#E53935",        # red
}

RARITY_ORDER = ["Common", "Uncommon", "Rare", "Legendary", "Epic"]

RARITY_SCORES = {
    "Common": 10,
    "Uncommon": 20,
    "Rare": 30,
    "Legendary": 50,
    "Epic": 70,
}

WIN_THRESHOLD = 4                  # monsters captured needed to win
STARTING_ORBS = 5
STARTING_CANDY = 3
CANDY_DIFFICULTY_REDUCTION = 3

SPRITE_PIXEL_SIZE = 16             # on-screen size (px) of one sprite "pixel"
