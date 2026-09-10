"""
Simple pixel-art monster sprites.

No image files are needed -- each monster is drawn on a Tkinter Canvas as a
grid of colored squares, so the game runs anywhere Python + Tkinter runs.

Each template is a 9x9 grid of characters:
    '.'  -> empty / transparent
    'X'  -> body pixel (filled with the monster's rarity color)
    'O'  -> eye pixel (always white, for contrast)

Which template a monster uses is picked deterministically from its name
(same name always renders the same shape), so monsters that share a rarity
(and therefore a color) still look different from each other.
"""

PIXEL_TEMPLATES = [
    # 0: Round
    [
        "...XXX...",
        "..XXXXX..",
        ".XXXXXXX.",
        "XXXOXOXXX",
        "XXXXXXXXX",
        "XXXXXXXXX",
        ".XXXXXXX.",
        "..XXXXX..",
        "...X.X...",
    ],
    # 1: Horned
    [
        "..X...X..",
        ".XX...XX.",
        "..XXXXX..",
        ".XXXXXXX.",
        "XXXOXOXXX",
        "XXXXXXXXX",
        ".XXXXXXX.",
        "..XXXXX..",
        "...X.X...",
    ],
    # 2: Wide
    [
        "XXXXXXXXX",
        "XXXXXXXXX",
        "XXOXXXOXX",
        "XXXXXXXXX",
        "XXXXXXXXX",
        "XXXXXXXXX",
        ".XXXXXXX.",
        "..XXXXX..",
        "...X.X...",
    ],
    # 3: Tall / slender
    [
        "...XXX...",
        "...XXX...",
        "..XXXXX..",
        "..XOXOX..",
        "..XXXXX..",
        "..XXXXX..",
        "..XXXXX..",
        "...XXX...",
        "....X....",
    ],
]


def get_template_index(name):
    """Deterministic shape choice based on the monster's name."""
    return sum(ord(ch) for ch in name) % len(PIXEL_TEMPLATES)


def draw_monster(canvas, top_x, top_y, color, template_index, pixel_size=16):
    """Draw one pixel-monster onto `canvas` with its top-left at (top_x, top_y)."""
    grid = PIXEL_TEMPLATES[template_index % len(PIXEL_TEMPLATES)]

    for row_index, row in enumerate(grid):
        for col_index, char in enumerate(row):
            if char == ".":
                continue

            x1 = top_x + col_index * pixel_size
            y1 = top_y + row_index * pixel_size
            x2 = x1 + pixel_size
            y2 = y1 + pixel_size

            fill = "white" if char == "O" else color
            canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline=fill)
