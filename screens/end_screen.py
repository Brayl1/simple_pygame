"""Game over screen: final score, trainer rank, win/lose, play again."""

import tkinter as tk


def build(app):
    root = app.root
    game = app.game

    tk.Label(root, text="GAME OVER", font=("Arial", 30, "bold")).pack(pady=35)
    tk.Label(root, text="Trainer: " + game.trainer_name, font=("Arial", 15)).pack(pady=3)
    tk.Label(root, text="Final Score: " + str(game.score), font=("Arial", 18, "bold")).pack(pady=3)
    tk.Label(root, text="Rank: " + game.trainer_rank(), font=("Arial", 16, "bold")).pack(pady=3)
    tk.Label(root, text="Monsters Captured: " + str(len(game.captured_monsters)),
             font=("Arial", 15)).pack(pady=3)
    tk.Label(root, text="Capture Orbs Remaining: " + str(len(game.inventory)),
             font=("Arial", 15)).pack(pady=3)

    result_text = "YOU WIN!" if game.is_win() else "YOU LOSE!"
    tk.Label(root, text=result_text, font=("Arial", 28, "bold")).pack(pady=25)

    buttons = tk.Frame(root)
    buttons.pack(pady=15)

    tk.Button(buttons, text="PLAY AGAIN", font=("Arial", 13, "bold"), width=15,
              command=app.show_title).grid(row=0, column=0, padx=10)
    tk.Button(buttons, text="VIEW COLLECTION", font=("Arial", 13), width=18,
              command=app.open_collection).grid(row=0, column=1, padx=10)
    tk.Button(buttons, text="EXIT", font=("Arial", 13), width=15,
              command=app.root.destroy).grid(row=0, column=2, padx=10)
