"""
History screen: chronological list of every encounter this run.

This version uses the SAME main window instead of creating
a separate Toplevel popup.
"""

import tkinter as tk

from PIL import Image, ImageTk


# =========================================================
# PIXEL GAME STYLE
# =========================================================

PIXEL_FONT = "Press Start 2P"

DEEP_GREEN = "#10291E"
DARK_GREEN = "#1D4931"
LIST_GREEN = "#163725"

GOLD = "#F2C14E"
LIGHT_GOLD = "#FFD966"

CREAM = "#FFF4C2"
BROWN = "#2B1B0E"

GREEN_BUTTON = "#4E8B68"
GREEN_HOVER = "#68AA82"


# =========================================================
# HISTORY SCREEN
# =========================================================

def open_window(app):

    game = app.game
    root = app.root

    # =====================================================
    # HISTORY SCREEN FRAME
    # =====================================================

    # IMPORTANT:
    # Do NOT destroy the current game screen.
    # History will appear on top of it.
    screen = tk.Frame(
        root,
        bg=DEEP_GREEN
    )

    screen.place(
        x=0,
        y=0,
        relwidth=1,
        relheight=1
    )

    # Make sure History appears above current game screen
    screen.lift()

    # =====================================================
    # BACKGROUND IMAGE
    # =====================================================

    original_bg = Image.open(
        "assets/bg4.png"
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

        # Make image large enough to completely cover screen
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

    # =====================================================
    # MAIN PANEL
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
        relwidth=0.86,
        relheight=0.86
    )

    # =====================================================
    # TITLE
    # =====================================================

    title_label = tk.Label(
        main_panel,
        text="ENCOUNTER HISTORY",
        font=(PIXEL_FONT, 16),
        fg=CREAM,
        bg=DEEP_GREEN
    )

    title_label.pack(
        pady=(20, 10)
    )

    # =====================================================
    # SUBTITLE
    # =====================================================

    subtitle = tk.Label(
        main_panel,
        text="CHRONOLOGICAL RECORD OF ENCOUNTERS",
        font=(PIXEL_FONT, 7),
        fg=GOLD,
        bg=DEEP_GREEN
    )

    subtitle.pack(
        pady=(0, 12)
    )

    # =====================================================
    # HISTORY PANEL
    # =====================================================

    history_panel = tk.Frame(
        main_panel,
        bg=DARK_GREEN,
        bd=4,
        relief="ridge"
    )

    history_panel.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=5
    )

    # =====================================================
    # LISTBOX
    # =====================================================

    listbox = tk.Listbox(
        history_panel,

        font=(PIXEL_FONT, 8),

        bg=LIST_GREEN,
        fg=CREAM,

        selectbackground=GOLD,
        selectforeground=BROWN,

        highlightthickness=0,

        relief="flat",
        bd=0,

        activestyle="none"
    )

    listbox.pack(
        side="left",
        fill="both",
        expand=True,

        padx=(8, 0),
        pady=8
    )

    # =====================================================
    # SCROLLBAR
    # =====================================================

    scrollbar = tk.Scrollbar(
        history_panel,

        orient="vertical",

        command=listbox.yview,

        troughcolor=DEEP_GREEN,

        bg=GOLD,
        activebackground=LIGHT_GOLD,

        relief="flat",
        bd=0
    )

    scrollbar.pack(
        side="right",
        fill="y",

        padx=8,
        pady=8
    )

    listbox.config(
        yscrollcommand=scrollbar.set
    )

    # =====================================================
    # INSERT HISTORY
    # =====================================================

    if not game.encounter_history:

        listbox.insert(
            tk.END,
            "NO ENCOUNTERS YET."
        )

    else:

        for round_no, name, result, roll in game.encounter_history:

            line = (
                "R"
                + str(round_no)
                + "   "
                + name
                + "   -   "
                + result
            )

            if roll != "-":

                line += (
                    "   (ROLL "
                    + str(roll)
                    + ")"
                )

            listbox.insert(
                tk.END,
                line
            )

    # =====================================================
    # BACK TO GAME BUTTON
    # =====================================================

    def go_back():

        # ONLY close the History overlay.
        # The current game screen underneath stays unchanged.
        screen.destroy()

    back_button = tk.Button(
        main_panel,

        text="BACK TO GAME",

        font=(PIXEL_FONT, 8),

        fg=BROWN,
        bg=GREEN_BUTTON,

        activebackground=GREEN_HOVER,
        activeforeground=BROWN,

        relief="raised",
        bd=4,

        cursor="hand2",

        command=go_back
    )

    back_button.pack(
        pady=(12, 18),

        ipadx=25,
        ipady=7
    )

    # =====================================================
    # BUTTON HOVER
    # =====================================================

    back_button.bind(
        "<Enter>",
        lambda e: back_button.config(
            bg=GREEN_HOVER
        )
    )

    back_button.bind(
        "<Leave>",
        lambda e: back_button.config(
            bg=GREEN_BUTTON
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

        # -------------------------------------------------
        # BACKGROUND
        # -------------------------------------------------

        update_background(
            width,
            height
        )

        # -------------------------------------------------
        # SCALE FONT
        # -------------------------------------------------

        scale_x = width / 800
        scale_y = height / 600

        scale = min(
            scale_x,
            scale_y
        )

        # Prevent fonts from becoming too tiny or huge
        scale = max(
            0.70,
            min(scale, 1.5)
        )

        # -------------------------------------------------
        # TITLE
        # -------------------------------------------------

        title_label.config(
            font=(
                PIXEL_FONT,
                max(
                    11,
                    int(16 * scale)
                )
            )
        )

        # -------------------------------------------------
        # SUBTITLE
        # -------------------------------------------------

        subtitle.config(
            font=(
                PIXEL_FONT,
                max(
                    5,
                    int(7 * scale)
                )
            )
        )

        # -------------------------------------------------
        # HISTORY TEXT
        # -------------------------------------------------

        listbox.config(
            font=(
                PIXEL_FONT,
                max(
                    6,
                    int(8 * scale)
                )
            )
        )

        # -------------------------------------------------
        # BACK BUTTON
        # -------------------------------------------------

        back_button.config(
            font=(
                PIXEL_FONT,
                max(
                    6,
                    int(8 * scale)
                )
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