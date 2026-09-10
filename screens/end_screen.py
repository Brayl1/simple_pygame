"""
Game over screen:
final score, trainer rank, win/lose,
play again, collection, and exit.

Pixel fantasy design matching the rest of the game.
"""

import tkinter as tk

from PIL import Image, ImageTk


# =========================================================
# PIXEL GAME STYLE
# =========================================================

PIXEL_FONT = "Press Start 2P"

# Main colors
DEEP_GREEN = "#10291E"
DARK_GREEN = "#1D4931"
PANEL_GREEN = "#163725"

# Text colors
GOLD = "#F2C14E"
LIGHT_GOLD = "#FFD966"

CREAM = "#FFF4C2"
WHITE = "#FFFFFF"

BROWN = "#2B1B0E"

# Buttons
GREEN_BUTTON = "#4E8B68"
GREEN_HOVER = "#68AA82"

GOLD_BUTTON = "#E8B84A"
GOLD_HOVER = "#FFD75A"

RED_BUTTON = "#B95E47"
RED_HOVER = "#D9775D"

# Result colors
WIN_COLOR = "#FFD966"
LOSE_COLOR = "#E9876E"


# =========================================================
# GAME OVER SCREEN
# =========================================================

def build(app):

    root = app.root
    game = app.game

    # =====================================================
    # MAIN SCREEN
    # =====================================================

    screen = tk.Frame(
        root,
        bg=DEEP_GREEN
    )

    screen.pack(
        fill="both",
        expand=True
    )

    # =====================================================
    # BACKGROUND IMAGE
    # =====================================================

    original_bg = Image.open(
        "assets/bg5.png"
    ).convert("RGB")

    background_canvas = tk.Canvas(
        screen,
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
    # RESPONSIVE BACKGROUND
    # =====================================================

    def update_background(width, height):

        if width <= 0 or height <= 0:
            return

        image_width, image_height = original_bg.size

        # Scale image until it completely covers the window
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

        background_canvas.delete(
            "background"
        )

        background_canvas.create_image(
            0,
            0,
            image=photo,
            anchor="nw",
            tags="background"
        )

        # Keep image reference
        background_canvas.image = photo

        background_canvas.tag_lower(
            "background"
        )

    # =====================================================
    # MAIN GAME OVER PANEL
    # =====================================================

    main_panel = tk.Frame(
        screen,
        bg=DEEP_GREEN,
        bd=5,
        relief="ridge"
    )

    main_panel.place(
        relx=0.5,
        rely=0.5,
        anchor="center",
        relwidth=0.72,
        relheight=0.78
    )

    # =====================================================
    # GAME OVER TITLE
    # =====================================================

    title_label = tk.Label(
        main_panel,
        text="GAME OVER",
        font=(PIXEL_FONT, 22),
        fg=CREAM,
        bg=DEEP_GREEN
    )

    title_label.pack(
        pady=(28, 8)
    )

    # =====================================================
    # RESULT
    # =====================================================

    result_text = (
        "YOU WIN!"
        if game.is_win()
        else "YOU LOSE!"
    )

    result_color = (
        WIN_COLOR
        if game.is_win()
        else LOSE_COLOR
    )

    result_label = tk.Label(
        main_panel,
        text=result_text,
        font=(PIXEL_FONT, 16),
        fg=result_color,
        bg=DEEP_GREEN
    )

    result_label.pack(
        pady=(2, 18)
    )

    # =====================================================
    # TRAINER INFORMATION PANEL
    # =====================================================

    stats_panel = tk.Frame(
        main_panel,
        bg=DARK_GREEN,
        bd=4,
        relief="ridge"
    )

    stats_panel.pack(
        fill="x",
        padx=45,
        pady=8
    )

    # =====================================================
    # TRAINER
    # =====================================================

    trainer_label = tk.Label(
        stats_panel,
        text=(
            "TRAINER: "
            + game.trainer_name
        ),
        font=(PIXEL_FONT, 8),
        fg=CREAM,
        bg=DARK_GREEN
    )

    trainer_label.pack(
        pady=(18, 7)
    )

    # =====================================================
    # FINAL SCORE
    # =====================================================

    score_label = tk.Label(
        stats_panel,
        text=(
            "FINAL SCORE: "
            + str(game.score)
        ),
        font=(PIXEL_FONT, 10),
        fg=GOLD,
        bg=DARK_GREEN
    )

    score_label.pack(
        pady=7
    )

    # =====================================================
    # TRAINER RANK
    # =====================================================

    rank_label = tk.Label(
        stats_panel,
        text=(
            "RANK: "
            + game.trainer_rank()
        ),
        font=(PIXEL_FONT, 8),
        fg=LIGHT_GOLD,
        bg=DARK_GREEN
    )

    rank_label.pack(
        pady=7
    )

    # =====================================================
    # MONSTERS CAPTURED
    # =====================================================

    captured_label = tk.Label(
        stats_panel,
        text=(
            "MONSTERS CAPTURED: "
            + str(
                len(
                    game.captured_monsters
                )
            )
        ),
        font=(PIXEL_FONT, 7),
        fg=CREAM,
        bg=DARK_GREEN
    )

    captured_label.pack(
        pady=7
    )

    # =====================================================
    # ORBS REMAINING
    # =====================================================

    orbs_label = tk.Label(
        stats_panel,
        text=(
            "CAPTURE ORBS REMAINING: "
            + str(
                len(
                    game.inventory
                )
            )
        ),
        font=(PIXEL_FONT, 7),
        fg=CREAM,
        bg=DARK_GREEN
    )

    orbs_label.pack(
        pady=(7, 18)
    )

    # =====================================================
    # BUTTON AREA
    # =====================================================

    buttons = tk.Frame(
        main_panel,
        bg=DEEP_GREEN
    )

    buttons.pack(
        pady=(18, 20)
    )

    # =====================================================
    # PLAY AGAIN BUTTON
    # =====================================================

    play_button = tk.Button(
        buttons,
        text="PLAY AGAIN",
        font=(PIXEL_FONT, 7),
        fg=WHITE,
        bg=GREEN_BUTTON,

        activebackground=GREEN_HOVER,
        activeforeground=WHITE,

        relief="raised",
        bd=4,

        cursor="hand2",

        command=app.show_title
    )

    play_button.grid(
        row=0,
        column=0,
        padx=8,
        ipadx=14,
        ipady=8
    )

    # =====================================================
    # COLLECTION BUTTON
    # =====================================================

    collection_button = tk.Button(
        buttons,
        text="VIEW COLLECTION",
        font=(PIXEL_FONT, 7),
        fg=BROWN,
        bg=GOLD_BUTTON,

        activebackground=GOLD_HOVER,
        activeforeground=BROWN,

        relief="raised",
        bd=4,

        cursor="hand2",

        command=app.open_collection
    )

    collection_button.grid(
        row=0,
        column=1,
        padx=8,
        ipadx=14,
        ipady=8
    )

    # =====================================================
    # EXIT BUTTON
    # =====================================================

    exit_button = tk.Button(
        buttons,
        text="EXIT",
        font=(PIXEL_FONT, 7),
        fg=WHITE,
        bg=RED_BUTTON,

        activebackground=RED_HOVER,
        activeforeground=WHITE,

        relief="raised",
        bd=4,

        cursor="hand2",

        command=app.root.destroy
    )

    exit_button.grid(
        row=0,
        column=2,
        padx=8,
        ipadx=20,
        ipady=8
    )

    # =====================================================
    # BUTTON HOVER EFFECTS
    # =====================================================

    play_button.bind(
        "<Enter>",
        lambda e: play_button.config(
            bg=GREEN_HOVER
        )
    )

    play_button.bind(
        "<Leave>",
        lambda e: play_button.config(
            bg=GREEN_BUTTON
        )
    )

    collection_button.bind(
        "<Enter>",
        lambda e: collection_button.config(
            bg=GOLD_HOVER
        )
    )

    collection_button.bind(
        "<Leave>",
        lambda e: collection_button.config(
            bg=GOLD_BUTTON
        )
    )

    exit_button.bind(
        "<Enter>",
        lambda e: exit_button.config(
            bg=RED_HOVER
        )
    )

    exit_button.bind(
        "<Leave>",
        lambda e: exit_button.config(
            bg=RED_BUTTON
        )
    )

    # =====================================================
    # RESPONSIVE LAYOUT
    # =====================================================

    def update_layout(event=None):

        width = screen.winfo_width()
        height = screen.winfo_height()

        if width < 100 or height < 100:
            return

        # Background
        update_background(
            width,
            height
        )

        # Base design size
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

        # =================================================
        # TITLE
        # =================================================

        title_label.config(
            font=(
                PIXEL_FONT,
                max(
                    14,
                    int(22 * scale)
                )
            )
        )

        # =================================================
        # RESULT
        # =================================================

        result_label.config(
            font=(
                PIXEL_FONT,
                max(
                    11,
                    int(16 * scale)
                )
            )
        )

        # =================================================
        # TRAINER
        # =================================================

        trainer_label.config(
            font=(
                PIXEL_FONT,
                max(
                    6,
                    int(8 * scale)
                )
            )
        )

        # =================================================
        # SCORE
        # =================================================

        score_label.config(
            font=(
                PIXEL_FONT,
                max(
                    7,
                    int(10 * scale)
                )
            )
        )

        # =================================================
        # RANK
        # =================================================

        rank_label.config(
            font=(
                PIXEL_FONT,
                max(
                    6,
                    int(8 * scale)
                )
            )
        )

        # =================================================
        # CAPTURED
        # =================================================

        captured_label.config(
            font=(
                PIXEL_FONT,
                max(
                    5,
                    int(7 * scale)
                )
            )
        )

        # =================================================
        # ORBS
        # =================================================

        orbs_label.config(
            font=(
                PIXEL_FONT,
                max(
                    5,
                    int(7 * scale)
                )
            )
        )

        # =================================================
        # BUTTONS
        # =================================================

        button_font_size = max(
            5,
            int(7 * scale)
        )

        play_button.config(
            font=(
                PIXEL_FONT,
                button_font_size
            )
        )

        collection_button.config(
            font=(
                PIXEL_FONT,
                button_font_size
            )
        )

        exit_button.config(
            font=(
                PIXEL_FONT,
                button_font_size
            )
        )

    # =====================================================
    # RESIZE EVENT
    # =====================================================

    screen.bind(
        "<Configure>",
        update_layout
    )

    screen.after(
        100,
        update_layout
    )