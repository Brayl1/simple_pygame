"""Main battle screen: shows the current monster (as a pixel sprite) and
the CAPTURE / SKIP / USE RARE CANDY actions."""

import tkinter as tk

import sprites
from constants import RARITY_COLORS, SPRITE_PIXEL_SIZE

SPRITE_CANVAS_SIZE = 9 * SPRITE_PIXEL_SIZE  # templates are 9x9 pixels


def build(app):
    root = app.root
    w = app.widgets

    w["trainer_label"] = tk.Label(root, text="Trainer: " + app.game.trainer_name,
                                   font=("Arial", 14, "bold"))
    w["trainer_label"].place(x=20, y=20)

    w["score_label"] = tk.Label(root, text="Score: 0", font=("Arial", 14, "bold"))
    w["score_label"].place(x=380, y=20)

    w["status_label"] = tk.Label(root, text="", font=("Arial", 12))
    w["status_label"].place(x=620, y=20)

    w["round_label"] = tk.Label(root, text="Round: 1", font=("Arial", 13))
    w["round_label"].pack(pady=60)

    frame = tk.LabelFrame(root, text="Wild Monster", font=("Arial", 15, "bold"),
                           width=680, height=230)
    frame.pack(pady=5)
    frame.pack_propagate(False)

    sprite_canvas = tk.Canvas(frame, width=SPRITE_CANVAS_SIZE, height=SPRITE_CANVAS_SIZE,
                               highlightthickness=0, bg=frame.cget("bg"))
    sprite_canvas.pack(side="left", padx=25, pady=15)
    w["sprite_canvas"] = sprite_canvas

    info_frame = tk.Frame(frame)
    info_frame.pack(side="left", padx=15, pady=15)

    w["monster_name_label"] = tk.Label(info_frame, text="", font=("Arial", 22, "bold"))
    w["monster_name_label"].pack(anchor="w", pady=5)
    w["rarity_label"] = tk.Label(info_frame, text="", font=("Arial", 13))
    w["rarity_label"].pack(anchor="w")
    w["ability_label"] = tk.Label(info_frame, text="", font=("Arial", 13))
    w["ability_label"].pack(anchor="w")
    w["difficulty_label"] = tk.Label(info_frame, text="", font=("Arial", 13))
    w["difficulty_label"].pack(anchor="w")

    w["result_label"] = tk.Label(root, text="", font=("Arial", 14, "bold"))
    w["result_label"].pack(pady=12)

    action_frame = tk.Frame(root)
    action_frame.pack(pady=8)

    w["capture_button"] = tk.Button(action_frame, text="CAPTURE", font=("Arial", 13, "bold"),
                                     width=14, command=lambda: _attempt_capture(app))
    w["capture_button"].grid(row=0, column=0, padx=5)

    w["skip_button"] = tk.Button(action_frame, text="SKIP", font=("Arial", 13, "bold"),
                                  width=14, command=lambda: _skip(app))
    w["skip_button"].grid(row=0, column=1, padx=5)

    w["candy_button"] = tk.Button(action_frame, text="USE RARE CANDY", font=("Arial", 12),
                                   width=16, command=lambda: _use_candy(app))
    w["candy_button"].grid(row=0, column=2, padx=5)

    nav_frame = tk.Frame(root)
    nav_frame.pack(pady=15)

    tk.Button(nav_frame, text="COLLECTION", font=("Arial", 13), width=15,
              command=app.open_collection).grid(row=0, column=0, padx=5)
    tk.Button(nav_frame, text="HISTORY", font=("Arial", 13), width=15,
              command=app.open_history).grid(row=0, column=1, padx=5)


def advance_round(app):
    game = app.game

    if game.is_game_over():
        app.show_end()
        return

    monster = game.start_next_encounter()
    app.widgets["round_label"].config(text="Round: " + str(game.round_number))
    _render_monster(app, monster)
    app.widgets["result_label"].config(text="What will you do?")
    app.widgets["capture_button"].config(state="normal")
    app.widgets["skip_button"].config(state="normal")
    app.widgets["candy_button"].config(state=("normal" if game.candies else "disabled"))
    _update_status(app)


def _render_monster(app, monster):
    name, difficulty, rarity, ability = monster
    w = app.widgets

    w["monster_name_label"].config(text=name)
    w["rarity_label"].config(text="Rarity: " + rarity)
    w["ability_label"].config(text="Ability: " + ability)
    w["difficulty_label"].config(text="Capture Difficulty: " + str(difficulty))

    canvas = w["sprite_canvas"]
    canvas.delete("all")
    color = RARITY_COLORS.get(rarity, "#777777")
    template_index = sprites.get_template_index(name)
    sprites.draw_monster(canvas, 0, 0, color, template_index)


def _update_status(app):
    game = app.game
    app.widgets["score_label"].config(text="Score: " + str(game.score))
    app.widgets["status_label"].config(
        text="Orbs: " + str(len(game.inventory)) + "   Candy: " + str(len(game.candies))
    )


def _use_candy(app):
    if app.game.use_candy():
        _render_monster(app, app.game.current_monster)
        app.widgets["result_label"].config(text="Rare Candy used! Difficulty lowered.")
        app.widgets["candy_button"].config(state="disabled")
        _update_status(app)


def _attempt_capture(app):
    game = app.game
    name = game.current_monster[0]
    success, roll = game.attempt_capture()

    if success:
        app.widgets["result_label"].config(
            text="SUCCESS! " + name + " captured! Roll: " + str(roll)
        )
    else:
        app.widgets["result_label"].config(text=name + " escaped! Roll: " + str(roll))

    _update_status(app)
    _lock_buttons(app)
    app.root.after(1500, lambda: advance_round(app))


def _skip(app):
    game = app.game
    name = game.current_monster[0]
    game.skip_current()
    app.widgets["result_label"].config(text=name + " was skipped.")
    _lock_buttons(app)
    app.root.after(1200, lambda: advance_round(app))


def _lock_buttons(app):
    app.widgets["capture_button"].config(state="disabled")
    app.widgets["skip_button"].config(state="disabled")
    app.widgets["candy_button"].config(state="disabled")
