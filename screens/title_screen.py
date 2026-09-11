"""Title screen: name entry + start / instructions."""

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageSequence

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
    # BACKGROUND GIF
    # -------------------------

    gif = Image.open("assets/mscreen.gif")

    # Store every GIF frame
    gif_frames = []

    for frame in ImageSequence.Iterator(gif):
        gif_frames.append(
            frame.convert("RGB").copy()
        )

    # Get GIF speed
    gif_delay = gif.info.get("duration", 100)

    # Prevent extremely fast GIF playback
    if gif_delay < 30:
        gif_delay = 30

    current_frame = 0

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

    # Create background once
    background_id = canvas.create_image(
        0,
        0,
        anchor="nw",
        tags="background"
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
        event.widget.config(
            bg=BUTTON_HOVER
        )

    def button_leave(event):
        event.widget.config(
            bg=BUTTON_BG
        )

    start_button.bind(
        "<Enter>",
        button_enter
    )

    start_button.bind(
        "<Leave>",
        button_leave
    )

    instructions_button.bind(
        "<Enter>",
        button_enter
    )

    instructions_button.bind(
        "<Leave>",
        button_leave
    )

    # -------------------------
    # BACKGROUND UPDATE
    # -------------------------

    def update_background():

        width = root.winfo_width()
        height = root.winfo_height()

        if width < 100 or height < 100:
            return

        frame = gif_frames[current_frame]

        # NEAREST keeps pixel art sharp
        resized_bg = frame.resize(
            (width, height),
            Image.Resampling.NEAREST
        )

        bg_photo = ImageTk.PhotoImage(
            resized_bg
        )

        canvas.itemconfig(
            background_id,
            image=bg_photo
        )

        # Keep reference so image does not disappear
        canvas.bg_photo = bg_photo

        canvas.tag_lower(
            "background"
        )

    # -------------------------
    # GIF LOOP
    # -------------------------

    def animate_background():

        nonlocal current_frame

        # Stop animation automatically
        # if this screen/canvas is destroyed
        if not canvas.winfo_exists():
            return

        update_background()

        current_frame += 1

        if current_frame >= len(gif_frames):
            current_frame = 0

        root.after(
            gif_delay,
            animate_background
        )

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

        update_background()

        # -------------------------
        # SCALE
        # -------------------------

        scale_x = width / BASE_WIDTH
        scale_y = height / BASE_HEIGHT

        scale = min(
            scale_x,
            scale_y
        )

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

        # Shadow
        canvas.create_text(
            width / 2 + 3 * scale,
            height * 0.20 + 3 * scale,
            text="MONSTER CATCHER",
            font=(
                PIXEL_FONT,
                title_size
            ),
            fill=OUTLINE_COLOR,
            tags="title"
        )

        # Main title
        canvas.create_text(
            width / 2,
            height * 0.20,
            text="MONSTER CATCHER",
            font=(
                PIXEL_FONT,
                title_size
            ),
            fill=TITLE_COLOR,
            tags="title"
        )

        # -------------------------
        # SUBTITLE
        # -------------------------

        canvas.delete("subtitle")

        # Shadow
        canvas.create_text(
            width / 2 + 2 * scale,
            height * 0.32 + 2 * scale,
            text="Capture monsters and build your collection!",
            font=(
                PIXEL_FONT,
                subtitle_size
            ),
            fill=OUTLINE_COLOR,
            tags="subtitle"
        )

        # Main subtitle
        canvas.create_text(
            width / 2,
            height * 0.32,
            text="Capture monsters and build your collection!",
            font=(
                PIXEL_FONT,
                subtitle_size
            ),
            fill=TEXT_COLOR,
            tags="subtitle"
        )

        # -------------------------
        # TRAINER LABEL
        # -------------------------

        canvas.delete(
            "trainer_label"
        )

        # Shadow
        canvas.create_text(
            width / 2 + 2 * scale,
            height * 0.43 + 2 * scale,
            text="ENTER TRAINER NAME",
            font=(
                PIXEL_FONT,
                label_size
            ),
            fill=OUTLINE_COLOR,
            tags="trainer_label"
        )

        # Main text
        canvas.create_text(
            width / 2,
            height * 0.43,
            text="ENTER TRAINER NAME",
            font=(
                PIXEL_FONT,
                label_size
            ),
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
                max(
                    7,
                    int(9 * scale)
                )
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
                max(
                    7,
                    int(9 * scale)
                )
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
                max(
                    6,
                    int(7 * scale)
                )
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

        # Only respond to the main window
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

    root.after(
        100,
        update_ui
    )

    # Start GIF animation
    root.after(
        120,
        animate_background
    )

    name_entry.focus_set()


def _clean_name(raw_name):

    """Prevents blank/garbage input from crashing or breaking labels."""

    cleaned = "".join(
        ch
        for ch in raw_name.strip()
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
        "6. Capture "
        + str(WIN_THRESHOLD)
        + "+ monsters to win.\n"
        "7. View, search, and sort your collection anytime.\n"
        "8. The game ends when encounters, or Capture Orbs, run out."
    )