"""
Main battle screen:
shows the current monster and the
CAPTURE / SKIP / USE RARE CANDY actions.
"""

import tkinter as tk
from PIL import Image, ImageTk

import sprites

from constants import RARITY_COLORS, SPRITE_PIXEL_SIZE


SPRITE_CANVAS_SIZE = 9 * SPRITE_PIXEL_SIZE


def build(app):

    root = app.root
    w = app.widgets

    # =====================================================
    # WINDOW
    # =====================================================

    root.geometry("1000x700")
    root.minsize(800, 600)
    root.resizable(True, True)

    # =====================================================
    # COLORS
    # =====================================================

    PIXEL_FONT = "Press Start 2P"

    DARK_GREEN = "#163B2A"
    DEEP_GREEN = "#0B241A"

    GOLD = "#F2C14E"
    LIGHT_GOLD = "#FFD966"

    CREAM = "#FFF4C2"
    WHITE = "#FFFFFF"

    BROWN = "#2B1B0E"

    CAPTURE_COLOR = "#E8B84A"
    CAPTURE_HOVER = "#FFD75A"

    SKIP_COLOR = "#C96B4B"
    SKIP_HOVER = "#E98562"

    CANDY_COLOR = "#C97AD6"
    CANDY_HOVER = "#E39AEF"

    NAV_COLOR = "#4E8B68"
    NAV_HOVER = "#68AA82"

    # =====================================================
    # BACKGROUND IMAGE
    # =====================================================

    original_bg = Image.open(
        "assets/bg2.png"
    ).convert("RGB")

    # =====================================================
    # MAIN CANVAS
    # =====================================================

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

    # =====================================================
    # BACKGROUND FUNCTION
    # =====================================================

    def draw_background(width, height):

        if width <= 0 or height <= 0:
            return

        image_width, image_height = original_bg.size

        # -----------------------------------------------
        # COVER IMAGE
        # Keeps aspect ratio and fills the whole window.
        # -----------------------------------------------

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

        # -----------------------------------------------
        # CENTER CROP
        # -----------------------------------------------

        left = max(
            0,
            (new_width - width) // 2
        )

        top = max(
            0,
            (new_height - height) // 2
        )

        right = left + width
        bottom = top + height

        resized = resized.crop(
            (left, top, right, bottom)
        )

        bg_photo = ImageTk.PhotoImage(resized)

        canvas.delete("background")

        canvas.create_image(
            0,
            0,
            image=bg_photo,
            anchor="nw",
            tags="background"
        )

        canvas.bg_photo = bg_photo

        canvas.tag_lower("background")

    # =====================================================
    # TOP INFORMATION
    # =====================================================

    w["trainer_label"] = tk.Label(
        root,
        text="Trainer: " + app.game.trainer_name,
        font=(PIXEL_FONT, 9),
        fg=CREAM,
        bg=DARK_GREEN,
        padx=12,
        pady=8
    )

    w["score_label"] = tk.Label(
        root,
        text="Score: 0",
        font=(PIXEL_FONT, 9),
        fg=CREAM,
        bg=DARK_GREEN,
        padx=12,
        pady=8
    )

    w["status_label"] = tk.Label(
        root,
        text="Orbs: 0   Candy: 0",
        font=(PIXEL_FONT, 7),
        fg=WHITE,
        bg=DARK_GREEN,
        padx=10,
        pady=8
    )

    # =====================================================
    # ROUND LABEL
    # =====================================================

    w["round_label"] = tk.Label(
        root,
        text="Round: 1",
        font=(PIXEL_FONT, 10),
        fg=CREAM,
        bg=DEEP_GREEN,
        padx=14,
        pady=8
    )

    # =====================================================
    # MONSTER PANEL
    # =====================================================

    frame = tk.LabelFrame(
        root,
        text=" WILD MONSTER ",
        font=(PIXEL_FONT, 10),
        fg=GOLD,
        bg=DARK_GREEN,
        bd=5,
        relief="ridge",
        labelanchor="n"
    )

    w["monster_frame"] = frame

    # =====================================================
    # SPRITE CANVAS
    # =====================================================

    sprite_canvas = tk.Canvas(
        frame,
        width=SPRITE_CANVAS_SIZE,
        height=SPRITE_CANVAS_SIZE,
        highlightthickness=0,
        bd=0,
        bg=DARK_GREEN
    )

    w["sprite_canvas"] = sprite_canvas

    # =====================================================
    # MONSTER INFORMATION
    # =====================================================

    info_frame = tk.Frame(
        frame,
        bg=DARK_GREEN
    )

    w["monster_name_label"] = tk.Label(
        info_frame,
        text="",
        font=(PIXEL_FONT, 14),
        fg=CREAM,
        bg=DARK_GREEN
    )

    w["monster_name_label"].pack(
        anchor="w",
        pady=(5, 12)
    )

    w["rarity_label"] = tk.Label(
        info_frame,
        text="",
        font=(PIXEL_FONT, 8),
        fg=GOLD,
        bg=DARK_GREEN
    )

    w["rarity_label"].pack(
        anchor="w",
        pady=4
    )

    w["ability_label"] = tk.Label(
        info_frame,
        text="",
        font=(PIXEL_FONT, 8),
        fg=WHITE,
        bg=DARK_GREEN
    )

    w["ability_label"].pack(
        anchor="w",
        pady=4
    )

    w["difficulty_label"] = tk.Label(
        info_frame,
        text="",
        font=(PIXEL_FONT, 8),
        fg=WHITE,
        bg=DARK_GREEN
    )

    w["difficulty_label"].pack(
        anchor="w",
        pady=4
    )

    # =====================================================
    # RESULT / STATUS MESSAGE
    # =====================================================

    w["result_label"] = tk.Label(
        root,
        text="What will you do?",
        font=(PIXEL_FONT, 9),
        fg=CREAM,
        bg=DEEP_GREEN,
        padx=15,
        pady=8
    )

    # =====================================================
    # ACTION BUTTON FRAME
    # =====================================================

    action_frame = tk.Frame(
        root,
        bg=""
    )

    # =====================================================
    # CAPTURE
    # =====================================================

    w["capture_button"] = tk.Button(
        action_frame,
        text="CAPTURE",
        font=(PIXEL_FONT, 8),
        fg=BROWN,
        bg=CAPTURE_COLOR,
        activebackground=CAPTURE_HOVER,
        activeforeground=BROWN,
        relief="raised",
        bd=5,
        cursor="hand2",
        command=lambda: _attempt_capture(app)
    )

    # =====================================================
    # SKIP
    # =====================================================

    w["skip_button"] = tk.Button(
        action_frame,
        text="SKIP",
        font=(PIXEL_FONT, 8),
        fg=WHITE,
        bg=SKIP_COLOR,
        activebackground=SKIP_HOVER,
        activeforeground=WHITE,
        relief="raised",
        bd=5,
        cursor="hand2",
        command=lambda: _skip(app)
    )

    # =====================================================
    # RARE CANDY
    # =====================================================

    w["candy_button"] = tk.Button(
        action_frame,
        text="USE RARE CANDY",
        font=(PIXEL_FONT, 7),
        fg=WHITE,
        bg=CANDY_COLOR,
        activebackground=CANDY_HOVER,
        activeforeground=WHITE,
        relief="raised",
        bd=5,
        cursor="hand2",
        command=lambda: _use_candy(app)
    )

    # =====================================================
    # NAVIGATION
    # =====================================================

    nav_frame = tk.Frame(
        root,
        bg=""
    )

    collection_button = tk.Button(
        nav_frame,
        text="COLLECTION",
        font=(PIXEL_FONT, 7),
        fg=WHITE,
        bg=NAV_COLOR,
        activebackground=NAV_HOVER,
        activeforeground=WHITE,
        relief="raised",
        bd=4,
        cursor="hand2",
        command=app.open_collection
    )

    history_button = tk.Button(
        nav_frame,
        text="HISTORY",
        font=(PIXEL_FONT, 7),
        fg=WHITE,
        bg=NAV_COLOR,
        activebackground=NAV_HOVER,
        activeforeground=WHITE,
        relief="raised",
        bd=4,
        cursor="hand2",
        command=app.open_history
    )

    # =====================================================
    # HOVER EFFECT
    # =====================================================

    def hover(button, color):
        button.config(bg=color)

    def leave(button, color):
        button.config(bg=color)

    w["capture_button"].bind(
        "<Enter>",
        lambda e: hover(w["capture_button"], CAPTURE_HOVER)
    )

    w["capture_button"].bind(
        "<Leave>",
        lambda e: leave(w["capture_button"], CAPTURE_COLOR)
    )

    w["skip_button"].bind(
        "<Enter>",
        lambda e: hover(w["skip_button"], SKIP_HOVER)
    )

    w["skip_button"].bind(
        "<Leave>",
        lambda e: leave(w["skip_button"], SKIP_COLOR)
    )

    w["candy_button"].bind(
        "<Enter>",
        lambda e: hover(w["candy_button"], CANDY_HOVER)
    )

    w["candy_button"].bind(
        "<Leave>",
        lambda e: leave(w["candy_button"], CANDY_COLOR)
    )

    collection_button.bind(
        "<Enter>",
        lambda e: hover(collection_button, NAV_HOVER)
    )

    collection_button.bind(
        "<Leave>",
        lambda e: leave(collection_button, NAV_COLOR)
    )

    history_button.bind(
        "<Enter>",
        lambda e: hover(history_button, NAV_HOVER)
    )

    history_button.bind(
        "<Leave>",
        lambda e: leave(history_button, NAV_COLOR)
    )

    # =====================================================
    # RESPONSIVE LAYOUT
    # =====================================================

    def update_layout(event=None):

        width = root.winfo_width()
        height = root.winfo_height()

        if width < 100 or height < 100:
            return

        # -----------------------------------------------
        # BACKGROUND
        # -----------------------------------------------

        draw_background(width, height)

        # -----------------------------------------------
        # RESPONSIVE SCALE
        # -----------------------------------------------

        scale_x = width / 1000
        scale_y = height / 700

        scale = min(
            scale_x,
            scale_y
        )

        scale = max(
            0.75,
            min(scale, 1.6)
        )

        # =================================================
        # TOP BAR
        # =================================================

        top_font = max(
            7,
            int(9 * scale)
        )

        w["trainer_label"].config(
            font=(PIXEL_FONT, top_font)
        )

        w["score_label"].config(
            font=(PIXEL_FONT, top_font)
        )

        w["status_label"].config(
            font=(
                PIXEL_FONT,
                max(6, int(7 * scale))
            )
        )

        w["trainer_label"].place(
            x=20 * scale,
            y=15 * scale
        )

        w["score_label"].place(
            relx=0.5,
            y=15 * scale,
            anchor="n"
        )

        w["status_label"].place(
            relx=1.0,
            x=-20 * scale,
            y=15 * scale,
            anchor="ne"
        )

        # =================================================
        # ROUND
        # =================================================

        w["round_label"].config(
            font=(
                PIXEL_FONT,
                max(8, int(10 * scale))
            )
        )

        w["round_label"].place(
            relx=0.5,
            y=65 * scale,
            anchor="n"
        )

        # =================================================
        # MONSTER FRAME
        # =================================================

        panel_width = int(
            min(
                width * 0.78,
                760 * scale
            )
        )

        panel_height = int(
            min(
                height * 0.34,
                245 * scale
            )
        )

        panel_width = max(
            500,
            panel_width
        )

        panel_height = max(
            190,
            panel_height
        )

        frame.place(
            relx=0.5,
            y=105 * scale,
            anchor="n",
            width=panel_width,
            height=panel_height
        )

        # =================================================
        # SPRITE
        # =================================================

        sprite_canvas.config(
            width=SPRITE_CANVAS_SIZE,
            height=SPRITE_CANVAS_SIZE
        )

        sprite_canvas.place(
            x=35 * scale,
            rely=0.5,
            anchor="w"
        )

        # =================================================
        # INFO FRAME
        # =================================================

        info_frame.place(
            relx=0.42,
            rely=0.5,
            anchor="w"
        )

        w["monster_name_label"].config(
            font=(
                PIXEL_FONT,
                max(10, int(14 * scale))
            )
        )

        w["rarity_label"].config(
            font=(
                PIXEL_FONT,
                max(6, int(8 * scale))
            )
        )

        w["ability_label"].config(
            font=(
                PIXEL_FONT,
                max(6, int(8 * scale))
            )
        )

        w["difficulty_label"].config(
            font=(
                PIXEL_FONT,
                max(6, int(8 * scale))
            )
        )

        # =================================================
        # RESULT MESSAGE
        # =================================================

        w["result_label"].config(
            font=(
                PIXEL_FONT,
                max(7, int(9 * scale))
            )
        )

        w["result_label"].place(
            relx=0.5,
            y=365 * scale,
            anchor="n"
        )

        # =================================================
        # ACTION BUTTONS
        # =================================================

        button_font = max(
            6,
            int(8 * scale)
        )

        w["capture_button"].config(
            font=(PIXEL_FONT, button_font)
        )

        w["skip_button"].config(
            font=(PIXEL_FONT, button_font)
        )

        w["candy_button"].config(
            font=(
                PIXEL_FONT,
                max(6, int(7 * scale))
            )
        )

        action_frame.place(
            relx=0.5,
            y=420 * scale,
            anchor="n"
        )

        button_width = max(
            130,
            int(170 * scale)
        )

        button_height = max(
            45,
            int(55 * scale)
        )

        w["capture_button"].grid(
            row=0,
            column=0,
            padx=int(6 * scale),
            ipadx=5,
            ipady=5
        )

        w["skip_button"].grid(
            row=0,
            column=1,
            padx=int(6 * scale),
            ipadx=5,
            ipady=5
        )

        w["candy_button"].grid(
            row=0,
            column=2,
            padx=int(6 * scale),
            ipadx=5,
            ipady=5
        )

        # =================================================
        # NAVIGATION
        # =================================================

        nav_frame.place(
            relx=0.5,
            y=510 * scale,
            anchor="n"
        )

        collection_button.config(
            font=(
                PIXEL_FONT,
                max(6, int(7 * scale))
            )
        )

        history_button.config(
            font=(
                PIXEL_FONT,
                max(6, int(7 * scale))
            )
        )

        collection_button.grid(
            row=0,
            column=0,
            padx=int(6 * scale),
            ipadx=int(8 * scale),
            ipady=int(5 * scale)
        )

        history_button.grid(
            row=0,
            column=1,
            padx=int(6 * scale),
            ipadx=int(8 * scale),
            ipady=int(5 * scale)
        )

    # =====================================================
    # RESIZE EVENT
    # =====================================================

    def on_resize(event):

        if event.widget == root:
            update_layout(event)

    root.bind(
        "<Configure>",
        on_resize
    )

    # =====================================================
    # INITIAL LAYOUT
    # =====================================================

    root.after(
        100,
        update_layout
    )


# =========================================================
# GAME FUNCTIONS
# =========================================================


def advance_round(app):

    game = app.game

    if game.is_game_over():
        app.show_end()
        return

    monster = game.start_next_encounter()

    app.widgets["round_label"].config(
        text="Round: " + str(game.round_number)
    )

    _render_monster(
        app,
        monster
    )

    app.widgets["result_label"].config(
        text="What will you do?"
    )

    app.widgets["capture_button"].config(
        state="normal"
    )

    app.widgets["skip_button"].config(
        state="normal"
    )

    app.widgets["candy_button"].config(
        state=("normal" if game.candies else "disabled")
    )

    _update_status(app)


def _render_monster(app, monster):

    name, difficulty, rarity, ability = monster

    w = app.widgets

    w["monster_name_label"].config(
        text=name
    )

    w["rarity_label"].config(
        text="Rarity: " + rarity
    )

    w["ability_label"].config(
        text="Ability: " + ability
    )

    w["difficulty_label"].config(
        text="Capture Difficulty: " + str(difficulty)
    )

    canvas = w["sprite_canvas"]

    canvas.delete("all")

    color = RARITY_COLORS.get(
        rarity,
        "#777777"
    )

    template_index = sprites.get_template_index(
        name
    )

    sprites.draw_monster(
        canvas,
        0,
        0,
        color,
        template_index
    )


def _update_status(app):

    game = app.game

    app.widgets["score_label"].config(
        text="Score: " + str(game.score)
    )

    app.widgets["status_label"].config(
        text=(
            "Orbs: "
            + str(len(game.inventory))
            + "   Candy: "
            + str(len(game.candies))
        )
    )


def _use_candy(app):

    if app.game.use_candy():

        _render_monster(
            app,
            app.game.current_monster
        )

        app.widgets["result_label"].config(
            text="Rare Candy used! Difficulty lowered."
        )

        app.widgets["candy_button"].config(
            state="disabled"
        )

        _update_status(app)


def _attempt_capture(app):

    game = app.game

    name = game.current_monster[0]

    success, roll = game.attempt_capture()

    if success:

        app.widgets["result_label"].config(
            text=(
                "SUCCESS! "
                + name
                + " captured! Roll: "
                + str(roll)
            )
        )

    else:

        app.widgets["result_label"].config(
            text=(
                name
                + " escaped! Roll: "
                + str(roll)
            )
        )

    _update_status(app)

    _lock_buttons(app)

    app.root.after(
        1500,
        lambda: advance_round(app)
    )


def _skip(app):

    game = app.game

    name = game.current_monster[0]

    game.skip_current()

    app.widgets["result_label"].config(
        text=name + " was skipped."
    )

    _lock_buttons(app)

    app.root.after(
        1200,
        lambda: advance_round(app)
    )


def _lock_buttons(app):

    app.widgets["capture_button"].config(
        state="disabled"
    )

    app.widgets["skip_button"].config(
        state="disabled"
    )

    app.widgets["candy_button"].config(
        state="disabled"
    )