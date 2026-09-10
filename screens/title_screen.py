"""Title screen: name entry + start / instructions."""

import tkinter as tk
from tkinter import messagebox

from constants import WIN_THRESHOLD


def build(app):
    root = app.root

    tk.Label(root, text="MONSTER CATCHER", font=("Arial", 30, "bold")).pack(pady=40)
    tk.Label(root, text="Capture monsters and build your collection!",
             font=("Arial", 14)).pack(pady=5)
    tk.Label(root, text="Enter Trainer Name:", font=("Arial", 13)).pack(pady=10)

    name_entry = tk.Entry(root, font=("Arial", 14), width=25)
    name_entry.pack(pady=10)

    def on_start():
        app.start_game(_clean_name(name_entry.get()))

    tk.Button(root, text="START GAME", font=("Arial", 14, "bold"), width=20,
              command=on_start).pack(pady=20)
    tk.Button(root, text="HOW TO PLAY", font=("Arial", 12), width=20,
              command=_show_instructions).pack(pady=5)


def _clean_name(raw_name):
    """Prevents blank/garbage input from crashing or breaking labels."""
    cleaned = "".join(ch for ch in raw_name.strip() if ch.isalnum() or ch == " ").strip()
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
