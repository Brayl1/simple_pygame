"""Title screen: name entry + start / instructions."""

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

from constants import WIN_THRESHOLD


def build(app):

    root = app.root

    # -------------------------
    # WINDOW SETTINGS
    # -------------------------

    root.geometry("800x450")

    # Allow resizing and maximizing
    root.resizable(True, True)

    # Minimum size
    root.minsize(600, 350)

    # -------------------------
    # COLORS
    # -------------------------

    TITLE_COLOR = "#FFF4C2"
    TEXT_COLOR = "#FFFFFF"
    OUTLINE_COLOR = "#2B1B0E"

    BUTTON_BG = "#F2C14E"
    BUTTON_HOVER = "#FFD966"
    BUTTON_TEXT = "#2B1B0E"

    ENTRY_BG = "#FFF8DC"
    ENTRY_TEXT = "#2B1B0E"

    PIXEL_FONT = "Press Start 2P"

    # Original design size
    BASE_WIDTH = 800
    BASE_HEIGHT = 450

    # -------------------------
    # BACKGROUND IMAGE
    # -------------------------

    original_bg = Image.open(
        "assets/bg.png"
    ).convert("RGB")

    # -------------------------
    # CANVAS
    # -------------------------

    canvas = tk.Canvas(
        root,
        highlightthickness=0,
        bd=0
    )

    canvas.place(
        x=0,
        y=0,
        relwidth=1,
        relheight=1
    )

    # -------------------------
    # NAME ENTRY
    # -------------------------

    name_entry = tk.Entry(
        root,
        font=(PIXEL_FONT, 9),
        justify="center",
        bg=ENTRY_BG,
        fg=ENTRY_TEXT,
        insertbackground=ENTRY_TEXT,
        relief="flat",
        bd=0,
        highlightthickness=3,
        highlightbackground=OUTLINE_COLOR,
        highlightcolor=BUTTON_BG
    )

    # -------------------------
    # START GAME
    # -------------------------

    def on_start():
        app.start_game(
            _clean_name(name_entry.get())
        )

    start_button = tk.Button(
        root,
        text="START GAME",
        font=(PIXEL_FONT, 9),
        command=on_start,
        bg=BUTTON_BG,
        fg=BUTTON_TEXT,
        activebackground=BUTTON_HOVER,
        activeforeground=BUTTON_TEXT,
        relief="raised",
        bd=4,
        cursor="hand2"
    )

    # -------------------------
    # HOW TO PLAY
    # -------------------------

    instructions_button = tk.Button(
        root,
        text="HOW TO PLAY",
        font=(PIXEL_FONT, 7),
        command=_show_instructions,
        bg=BUTTON_BG,
        fg=BUTTON_TEXT,
        activebackground=BUTTON_HOVER,
        activeforeground=BUTTON_TEXT,
        relief="raised",
        bd=4,
        cursor="hand2"
    )

    # -------------------------
    # BUTTON HOVER
    # -------------------------

    def button_enter(event):
        event.widget.config(bg=BUTTON_HOVER)

    def button_leave(event):
        event.widget.config(bg=BUTTON_BG)

    start_button.bind("<Enter>", button_enter)
    start_button.bind("<Leave>", button_leave)

    instructions_button.bind("<Enter>", button_enter)
    instructions_button.bind("<Leave>", button_leave)

    # -------------------------
    # RESPONSIVE UPDATE
    # -------------------------

    def update_ui(width=None, height=None):

        # Get the ACTUAL current window size
        if width is None:
            width = root.winfo_width()

        if height is None:
            height = root.winfo_height()

        # Ignore invalid initial sizes
        if width < 100 or height < 100:
            return

        # -------------------------
        # BACKGROUND
        # -------------------------

        resized_bg = original_bg.resize(
            (width, height),
            Image.Resampling.LANCZOS
        )

        bg_photo = ImageTk.PhotoImage(resized_bg)

        canvas.delete("background")

        canvas.create_image(
            0,
            0,
            image=bg_photo,
            anchor="nw",
            tags="background"
        )

        canvas.bg_photo = bg_photo

        # Make sure background is behind everything
        canvas.tag_lower("background")

        # -------------------------
        # SCALE
        # -------------------------

        scale_x = width / BASE_WIDTH
        scale_y = height / BASE_HEIGHT

        scale = min(scale_x, scale_y)

        # -------------------------
        # FONT SIZES
        # -------------------------

        title_size = max(
            14,
            int(20 * scale)
        )

        subtitle_size = max(
            6,
            int(7 * scale)
        )

        label_size = max(
            6,
            int(8 * scale)
        )

        # -------------------------
        # TITLE
        # -------------------------

        canvas.delete("title")

        canvas.create_text(
            width / 2 + 3 * scale,
            height * 0.20 + 3 * scale,
            text="MONSTER CATCHER",
            font=(PIXEL_FONT, title_size),
            fill=OUTLINE_COLOR,
            tags="title"
        )

        canvas.create_text(
            width / 2,
            height * 0.20,
            text="MONSTER CATCHER",
            font=(PIXEL_FONT, title_size),
            fill=TITLE_COLOR,
            tags="title"
        )

        # -------------------------
        # SUBTITLE
        # -------------------------

        canvas.delete("subtitle")

        canvas.create_text(
            width / 2 + 2 * scale,
            height * 0.32 + 2 * scale,
            text="Capture monsters and build your collection!",
            font=(PIXEL_FONT, subtitle_size),
            fill=OUTLINE_COLOR,
            tags="subtitle"
        )

        canvas.create_text(
            width / 2,
            height * 0.32,
            text="Capture monsters and build your collection!",
            font=(PIXEL_FONT, subtitle_size),
            fill=TEXT_COLOR,
            tags="subtitle"
        )

        # -------------------------
        # TRAINER LABEL
        # -------------------------

        canvas.delete("trainer_label")

        canvas.create_text(
            width / 2 + 2 * scale,
            height * 0.43 + 2 * scale,
            text="ENTER TRAINER NAME",
            font=(PIXEL_FONT, label_size),
            fill=OUTLINE_COLOR,
            tags="trainer_label"
        )

        canvas.create_text(
            width / 2,
            height * 0.43,
            text="ENTER TRAINER NAME",
            font=(PIXEL_FONT, label_size),
            fill=TITLE_COLOR,
            tags="trainer_label"
        )

        # -------------------------
        # NAME ENTRY
        # -------------------------

        entry_width = max(
            200,
            int(260 * scale)
        )

        entry_height = max(
            28,
            int(30 * scale)
        )

        name_entry.config(
            font=(
                PIXEL_FONT,
                max(7, int(9 * scale))
            )
        )

        name_entry.place(
            x=(width - entry_width) / 2,
            y=height * 0.50,
            width=entry_width,
            height=entry_height
        )

        # -------------------------
        # START BUTTON
        # -------------------------

        start_width = max(
            190,
            int(240 * scale)
        )

        start_height = max(
            45,
            int(55 * scale)
        )

        start_button.config(
            font=(
                PIXEL_FONT,
                max(7, int(9 * scale))
            )
        )

        start_button.place(
            x=(width - start_width) / 2,
            y=height * 0.61,
            width=start_width,
            height=start_height
        )

        # -------------------------
        # HOW TO PLAY
        # -------------------------

        how_width = max(
            170,
            int(200 * scale)
        )

        how_height = max(
            40,
            int(45 * scale)
        )

        instructions_button.config(
            font=(
                PIXEL_FONT,
                max(6, int(7 * scale))
            )
        )

        instructions_button.place(
            x=(width - how_width) / 2,
            y=height * 0.77,
            width=how_width,
            height=how_height
        )

    # -------------------------
    # WINDOW RESIZE
    # -------------------------

    def on_resize(event):

        # Only respond to the MAIN WINDOW
        if event.widget == root:
            update_ui(
                event.width,
                event.height
            )

    root.bind(
        "<Configure>",
        on_resize
    )

    # -------------------------
    # INITIAL DISPLAY
    # -------------------------
    # Wait until Tkinter has
    # finished creating the window.

    root.after(
        100,
        update_ui
    )

    name_entry.focus_set()


def _clean_name(raw_name):

    """Prevents blank/garbage input from crashing or breaking labels."""

    cleaned = "".join(
        ch for ch in raw_name.strip()
        if ch.isalnum() or ch == " "
    ).strip()

    return cleaned[:20] if cleaned else "Trainer"


def _show_instructions():

    messagebox.showinfo(
        "How to Play",
        "1. Enter your trainer name.\n"
        "2. A random monster appears each round.\n"
        "3. Choose CAPTURE or SKIP.\n"
        "4. Capturing uses one Capture Orb.\n"
        "5. Use a Rare Candy to weaken a monster before capturing it.\n"
        "6. Capture " + str(WIN_THRESHOLD) + "+ monsters to win.\n"
        "7. View, search, and sort your collection anytime.\n"
        "8. The game ends when encounters, or Capture Orbs, run out."
    )