"""
Collection window:
captured monsters with pixel icons,
rarity breakdown, search, and sort.
"""

import tkinter as tk
from tkinter import messagebox

from PIL import Image, ImageTk

import sprites

from constants import RARITY_ORDER, RARITY_COLORS


ROW_PIXEL_SIZE = 6
ROW_ICON_SIZE = 9 * ROW_PIXEL_SIZE


# =========================================================
# COLORS / STYLE
# =========================================================

PIXEL_FONT = "Press Start 2P"

DARK_GREEN = "#173D2B"
DEEP_GREEN = "#0C281C"

GOLD = "#F2C14E"
LIGHT_GOLD = "#FFD966"

CREAM = "#FFF4C2"
WHITE = "#FFFFFF"

BROWN = "#2B1B0E"

GREEN_BUTTON = "#4E8B68"
GREEN_HOVER = "#68AA82"

GOLD_BUTTON = "#E8B84A"
GOLD_HOVER = "#FFD75A"

RED_BUTTON = "#B95E47"
RED_HOVER = "#D9775D"

PURPLE_BUTTON = "#A96CBD"
PURPLE_HOVER = "#C988D6"


# =========================================================
# OPEN COLLECTION WINDOW
# =========================================================

def open_window(app):

    game = app.game

    # Collection screen overlays the current game screen
    # without destroying it.
    win = tk.Frame(
        app.root,
        bg=DEEP_GREEN
    )

    win.place(
        x=0,
        y=0,
        relwidth=1,
        relheight=1
    )

    win.lift()

    # =====================================================
    # BACKGROUND
    # =====================================================

    original_bg = Image.open(
        "assets/bg3.png"
    ).convert("RGB")

    background_canvas = tk.Canvas(
        win,
        highlightthickness=0,
        bd=0
    )

    background_canvas.place(
        x=0,
        y=0,
        relwidth=1,
        relheight=1
    )

    # =====================================================
    # BACKGROUND RESIZE
    # =====================================================

    def update_background(width, height):

        if width <= 0 or height <= 0:
            return

        image_width, image_height = original_bg.size

        # Scale image so it completely covers window
        scale = max(
            width / image_width,
            height / image_height
        )

        new_width = int(image_width * scale)
        new_height = int(image_height * scale)

        resized = original_bg.resize(
            (new_width, new_height),
            Image.Resampling.LANCZOS
        )

        # Center crop
        left = max(
            0,
            (new_width - width) // 2
        )

        top = max(
            0,
            (new_height - height) // 2
        )

        resized = resized.crop(
            (
                left,
                top,
                left + width,
                top + height
            )
        )

        photo = ImageTk.PhotoImage(resized)

        background_canvas.delete("background")

        background_canvas.create_image(
            0,
            0,
            image=photo,
            anchor="nw",
            tags="background"
        )

        background_canvas.image = photo

        background_canvas.tag_lower("background")

    # =====================================================
    # MAIN CONTENT
    # =====================================================

    content = tk.Frame(
        win,
        bg=DEEP_GREEN
    )

    content.place(
        relx=0.5,
        rely=0.5,
        anchor="center",
        relwidth=0.82,
        relheight=0.90
    )

    # =====================================================
    # BACK BUTTON
    # =====================================================

    def go_back():

        # ONLY remove the Collection overlay.
        # Do not rebuild or advance the game screen.
        win.destroy()

    back_button = tk.Button(
        content,
        text="< BACK",
        font=(PIXEL_FONT, 7),
        fg=WHITE,
        bg=RED_BUTTON,
        activebackground=RED_HOVER,
        activeforeground=WHITE,
        relief="raised",
        bd=4,
        cursor="hand2",
        command=go_back
    )

    back_button.place(
        x=15,
        y=15
    )

    # =====================================================
    # TITLE
    # =====================================================

    title_label = tk.Label(
        content,
        text="YOUR MONSTER COLLECTION",
        font=(PIXEL_FONT, 16),
        fg=CREAM,
        bg=DEEP_GREEN,
        pady=12
    )

    title_label.pack(
        pady=(18, 5)
    )

    # =====================================================
    # TOTAL CAPTURED
    # =====================================================

    total_label = tk.Label(
        content,
        text="Total Captured: "
        + str(len(game.captured_monsters)),
        font=(PIXEL_FONT, 8),
        fg=GOLD,
        bg=DEEP_GREEN
    )

    total_label.pack(
        pady=5
    )

    # =====================================================
    # BREAKDOWN PANEL
    # =====================================================

    breakdown_panel = tk.Frame(
        content,
        bg=DARK_GREEN,
        bd=4,
        relief="ridge"
    )

    breakdown_panel.pack(
        fill="x",
        padx=25,
        pady=8
    )

    breakdown_label = tk.Label(
        breakdown_panel,
        text=_format_breakdown(game),
        font=(PIXEL_FONT, 7),
        fg=CREAM,
        bg=DARK_GREEN,
        justify="left"
    )

    breakdown_label.pack(
        pady=10,
        padx=15
    )

    # =====================================================
    # SEARCH AREA
    # =====================================================

    search_frame = tk.Frame(
        content,
        bg=DEEP_GREEN
    )

    search_frame.pack(
        fill="x",
        padx=25,
        pady=8
    )

    search_entry = tk.Entry(
        search_frame,
        font=(PIXEL_FONT, 8),
        bg="#FFFBE6",
        fg=BROWN,
        insertbackground=BROWN,
        relief="solid",
        bd=3
    )

    search_entry.pack(
        side="left",
        fill="x",
        expand=True,
        ipady=7,
        padx=(0, 8)
    )

    # =====================================================
    # SEARCH FUNCTION
    # =====================================================

    def on_search():

        found = game.find_captured(
            search_entry.get()
        )

        if found:

            messagebox.showinfo(
                "Monster Found",
                "Name: "
                + found[0]
                + "\nRarity: "
                + found[2]
                + "\nAbility: "
                + found[3],
                parent=win
            )

        else:

            messagebox.showinfo(
                "Search Result",
                "Monster not found.",
                parent=win
            )

    search_button = tk.Button(
        search_frame,
        text="SEARCH",
        font=(PIXEL_FONT, 7),
        fg=BROWN,
        bg=GOLD_BUTTON,
        activebackground=GOLD_HOVER,
        activeforeground=BROWN,
        relief="raised",
        bd=4,
        cursor="hand2",
        command=on_search
    )

    search_button.pack(
        side="right",
        ipadx=12,
        ipady=5
    )

    # =====================================================
    # MONSTER LIST
    # =====================================================

    list_container = tk.Frame(
        content,
        bg=DARK_GREEN,
        bd=5,
        relief="ridge"
    )

    list_container.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=8
    )

    list_area = _build_scrollable_list(
        list_container
    )

    # =====================================================
    # SORT BUTTON
    # =====================================================

    def on_sort():

        if not game.captured_monsters:

            messagebox.showinfo(
                "Sort",
                "No monsters to sort.",
                parent=win
            )

            return

        game.sort_captured_alphabetically()

        refresh()

        messagebox.showinfo(
            "Sort",
            "Collection sorted alphabetically.",
            parent=win
        )

    sort_button = tk.Button(
        content,
        text="SORT ALPHABETICALLY",
        font=(PIXEL_FONT, 7),
        fg=WHITE,
        bg=GREEN_BUTTON,
        activebackground=GREEN_HOVER,
        activeforeground=WHITE,
        relief="raised",
        bd=4,
        cursor="hand2",
        command=on_sort
    )

    sort_button.pack(
        pady=(5, 15),
        ipadx=12,
        ipady=6
    )

    # =====================================================
    # HOVER EFFECTS
    # =====================================================

    search_button.bind(
        "<Enter>",
        lambda e: search_button.config(
            bg=GOLD_HOVER
        )
    )

    search_button.bind(
        "<Leave>",
        lambda e: search_button.config(
            bg=GOLD_BUTTON
        )
    )

    sort_button.bind(
        "<Enter>",
        lambda e: sort_button.config(
            bg=GREEN_HOVER
        )
    )

    sort_button.bind(
        "<Leave>",
        lambda e: sort_button.config(
            bg=GREEN_BUTTON
        )
    )

    back_button.bind(
        "<Enter>",
        lambda e: back_button.config(
            bg=RED_HOVER
        )
    )

    back_button.bind(
        "<Leave>",
        lambda e: back_button.config(
            bg=RED_BUTTON
        )
    )

    # =====================================================
    # REFRESH
    # =====================================================

    def refresh():

        _refresh_rows(
            list_area,
            game
        )

        total_label.config(
            text="Total Captured: "
            + str(len(game.captured_monsters))
        )

        breakdown_label.config(
            text=_format_breakdown(game)
        )

    refresh()

    # =====================================================
    # RESPONSIVE RESIZE
    # =====================================================

    def update_layout(event=None):

        width = win.winfo_width()
        height = win.winfo_height()

        if width < 100 or height < 100:
            return

        # Background
        update_background(
            width,
            height
        )

        # Responsive font scaling
        scale_x = width / 900
        scale_y = height / 700

        scale = min(
            scale_x,
            scale_y
        )

        scale = max(
            0.70,
            min(scale, 1.5)
        )

        # -----------------------------------------------
        # TITLE
        # -----------------------------------------------

        title_label.config(
            font=(
                PIXEL_FONT,
                max(
                    11,
                    int(16 * scale)
                )
            )
        )

        # -----------------------------------------------
        # TOTAL
        # -----------------------------------------------

        total_label.config(
            font=(
                PIXEL_FONT,
                max(
                    6,
                    int(8 * scale)
                )
            )
        )

        # -----------------------------------------------
        # BREAKDOWN
        # -----------------------------------------------

        breakdown_label.config(
            font=(
                PIXEL_FONT,
                max(
                    6,
                    int(7 * scale)
                )
            )
        )

        # -----------------------------------------------
        # SEARCH
        # -----------------------------------------------

        search_entry.config(
            font=(
                PIXEL_FONT,
                max(
                    6,
                    int(8 * scale)
                )
            )
        )

        search_button.config(
            font=(
                PIXEL_FONT,
                max(
                    6,
                    int(7 * scale)
                )
            )
        )

        # -----------------------------------------------
        # SORT
        # -----------------------------------------------

        sort_button.config(
            font=(
                PIXEL_FONT,
                max(
                    6,
                    int(7 * scale)
                )
            )
        )

        # -----------------------------------------------
        # BACK
        # -----------------------------------------------

        back_button.config(
            font=(
                PIXEL_FONT,
                max(
                    6,
                    int(7 * scale)
                )
            )
        )

    # =====================================================
    # WINDOW RESIZE EVENT
    # =====================================================

    win.bind(
        "<Configure>",
        update_layout
    )

    win.after(
        100,
        update_layout
    )


# =========================================================
# SCROLLABLE LIST
# =========================================================

def _build_scrollable_list(parent):

    outer = tk.Frame(
        parent,
        bg=DARK_GREEN
    )

    outer.pack(
        fill="both",
        expand=True
    )

    canvas = tk.Canvas(
        outer,
        highlightthickness=0,
        bd=0,
        bg=DARK_GREEN
    )

    scrollbar = tk.Scrollbar(
        outer,
        orient="vertical",
        command=canvas.yview,
        troughcolor=DEEP_GREEN,
        bg=GOLD,
        activebackground=LIGHT_GOLD
    )

    inner_frame = tk.Frame(
        canvas,
        bg=DARK_GREEN
    )

    inner_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    # Make inner frame width follow canvas width
    canvas.bind(
        "<Configure>",
        lambda e: canvas.itemconfig(
            canvas_window,
            width=e.width
        )
    )

    canvas_window = canvas.create_window(
        (0, 0),
        window=inner_frame,
        anchor="nw"
    )

    canvas.configure(
        yscrollcommand=scrollbar.set
    )

    canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    # Mouse wheel scrolling
    def mouse_wheel(event):

        canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    canvas.bind_all(
        "<MouseWheel>",
        mouse_wheel
    )

    return inner_frame


# =========================================================
# REFRESH MONSTER ROWS
# =========================================================

def _refresh_rows(inner_frame, game):

    for widget in inner_frame.winfo_children():
        widget.destroy()

    if not game.captured_monsters:

        empty_label = tk.Label(
            inner_frame,
            text="NO MONSTERS CAPTURED YET",
            font=(PIXEL_FONT, 8),
            fg=CREAM,
            bg=DARK_GREEN
        )

        empty_label.pack(
            pady=30
        )

        return

    # Required list traversal
    for monster in game.captured_monsters:

        _build_row(
            inner_frame,
            monster
        )


# =========================================================
# BUILD MONSTER ROW
# =========================================================

def _build_row(inner_frame, monster):

    name, difficulty, rarity, ability = monster

    # -----------------------------------------------
    # ROW
    # -----------------------------------------------

    row = tk.Frame(
        inner_frame,
        bg=DEEP_GREEN,
        bd=2,
        relief="groove"
    )

    row.pack(
        fill="x",
        padx=8,
        pady=4
    )

    # -----------------------------------------------
    # ICON
    # -----------------------------------------------

    icon = tk.Canvas(
        row,
        width=ROW_ICON_SIZE,
        height=ROW_ICON_SIZE,
        highlightthickness=0,
        bd=0,
        bg=DEEP_GREEN
    )

    icon.pack(
        side="left",
        padx=12,
        pady=7
    )

    color = RARITY_COLORS.get(
        rarity,
        "#777777"
    )

    template_index = sprites.get_template_index(
        name
    )

    sprites.draw_monster(
        icon,
        0,
        0,
        color,
        template_index,
        pixel_size=ROW_PIXEL_SIZE
    )

    # -----------------------------------------------
    # MONSTER INFORMATION
    # -----------------------------------------------

    info = tk.Frame(
        row,
        bg=DEEP_GREEN
    )

    info.pack(
        side="left",
        fill="x",
        expand=True,
        padx=8,
        pady=8
    )

    # Monster name
    name_label = tk.Label(
        info,
        text=name,
        font=(PIXEL_FONT, 9),
        fg=CREAM,
        bg=DEEP_GREEN,
        anchor="w"
    )

    name_label.pack(
        anchor="w",
        pady=(0, 6)
    )

    # Rarity
    rarity_label = tk.Label(
        info,
        text="RARITY: " + rarity,
        font=(PIXEL_FONT, 6),
        fg=color,
        bg=DEEP_GREEN,
        anchor="w"
    )

    rarity_label.pack(
        anchor="w",
        pady=2
    )

    # Ability
    ability_label = tk.Label(
        info,
        text="ABILITY: " + ability,
        font=(PIXEL_FONT, 6),
        fg=WHITE,
        bg=DEEP_GREEN,
        anchor="w"
    )

    ability_label.pack(
        anchor="w",
        pady=2
    )

    # Difficulty
    difficulty_label = tk.Label(
        info,
        text="DIFFICULTY: " + str(difficulty),
        font=(PIXEL_FONT, 6),
        fg=GOLD,
        bg=DEEP_GREEN,
        anchor="w"
    )

    difficulty_label.pack(
        anchor="w",
        pady=2
    )


# =========================================================
# RARITY BREAKDOWN
# =========================================================

def _format_breakdown(game):

    counts = game.rarity_breakdown()

    lines = [
        "COLLECTION BREAKDOWN"
    ]

    for tier in RARITY_ORDER:

        lines.append(
            tier
            + ": "
            + str(counts[tier])
        )

    return "\n".join(lines)