"""History window: chronological list of every encounter this run."""

import tkinter as tk


def open_window(app):
    game = app.game
    win = tk.Toplevel(app.root)
    win.title("Encounter History")
    win.geometry("560x460")

    tk.Label(win, text="ENCOUNTER HISTORY", font=("Arial", 18, "bold")).pack(pady=15)

    listbox = tk.Listbox(win, font=("Arial", 12), width=62, height=16)
    listbox.pack(pady=10)

    if not game.encounter_history:
        listbox.insert(tk.END, "No encounters yet.")
        return

    for round_no, name, result, roll in game.encounter_history:
        line = "R" + str(round_no) + "  " + name + "  -  " + result
        if roll != "-":
            line += "  (roll " + str(roll) + ")"
        listbox.insert(tk.END, line)
