"""Collection window: captured monsters (each with its pixel icon),
a rarity breakdown, search, and sort.

A plain Listbox can't draw a Canvas sprite next to its text, so this screen
uses the standard Tkinter "scrollable frame" pattern instead: a Canvas +
inner Frame + Scrollbar, with one small row (icon + label) per monster.
"""

import tkinter as tk
from tkinter import messagebox

import sprites
from constants import RARITY_ORDER, RARITY_COLORS

ROW_PIXEL_SIZE = 6                 # smaller sprite scale for list rows
ROW_ICON_SIZE = 9 * ROW_PIXEL_SIZE  # templates are 9x9 pixels


def open_window(app):
    game = app.game
    win = tk.Toplevel(app.root)
    win.title("Monster Collection")
    win.geometry("640x580")

    tk.Label(win, text="YOUR MONSTER COLLECTION", font=("Arial", 18, "bold")).pack(pady=15)
    total_label = tk.Label(win, text="Total Captured: " + str(len(game.captured_monsters)),
                            font=("Arial", 12))
    total_label.pack()

    list_area = _build_scrollable_list(win)

    def refresh():
        _refresh_rows(list_area, game)
        total_label.config(text="Total Captured: " + str(len(game.captured_monsters)))
        breakdown_label.config(text=_format_breakdown(game))

    breakdown_label = tk.Label(win, text=_format_breakdown(game), font=("Arial", 11), justify="left")
    breakdown_label.pack(pady=8)

    refresh()

    search_frame = tk.Frame(win)
    search_frame.pack(pady=5)
    search_entry = tk.Entry(search_frame, font=("Arial", 12))
    search_entry.grid(row=0, column=0, padx=5)

    def on_search():
        found = game.find_captured(search_entry.get())
        if found:
            messagebox.showinfo(
                "Monster Found",
                "Name: " + found[0] + "\nRarity: " + found[2] + "\nAbility: " + found[3]
            )
        else:
            messagebox.showinfo("Search Result", "Monster not found.")

    tk.Button(search_frame, text="Search", command=on_search).grid(row=0, column=1)

    def on_sort():
        if not game.captured_monsters:
            messagebox.showinfo("Sort", "No monsters to sort.")
            return
        game.sort_captured_alphabetically()
        refresh()
        messagebox.showinfo("Sort", "Collection sorted alphabetically.")

    tk.Button(win, text="Sort Alphabetically", font=("Arial", 11), command=on_sort).pack(pady=10)


def _build_scrollable_list(parent):
    """Standard Tkinter scrollable-frame pattern: Canvas + inner Frame + Scrollbar."""
    outer = tk.Frame(parent)
    outer.pack(pady=10, fill="both", expand=False)

    canvas = tk.Canvas(outer, width=600, height=260, highlightthickness=1,
                        highlightbackground="#cccccc")
    scrollbar = tk.Scrollbar(outer, orient="vertical", command=canvas.yview)
    inner_frame = tk.Frame(canvas)

    inner_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=inner_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    return inner_frame


def _refresh_rows(inner_frame, game):
    for widget in inner_frame.winfo_children():
        widget.destroy()

    if not game.captured_monsters:
        tk.Label(inner_frame, text="No monsters captured yet.",
                 font=("Arial", 12)).pack(pady=10)
        return

    # >>> Rubric requirement 5: traverse a list with a for loop
    for monster in game.captured_monsters:
        _build_row(inner_frame, monster)


def _build_row(inner_frame, monster):
    name, difficulty, rarity, ability = monster

    row = tk.Frame(inner_frame, pady=4)
    row.pack(fill="x", anchor="w")

    icon = tk.Canvas(row, width=ROW_ICON_SIZE, height=ROW_ICON_SIZE,
                      highlightthickness=0, bg=row.cget("bg"))
    icon.pack(side="left", padx=8)

    color = RARITY_COLORS.get(rarity, "#777777")
    template_index = sprites.get_template_index(name)
    sprites.draw_monster(icon, 0, 0, color, template_index, pixel_size=ROW_PIXEL_SIZE)

    text = name + "  |  " + rarity + "  |  Ability: " + ability
    tk.Label(row, text=text, font=("Arial", 12)).pack(side="left", padx=8)


def _format_breakdown(game):
    counts = game.rarity_breakdown()
    lines = ["Collection breakdown:"]
    for tier in RARITY_ORDER:
        lines.append("  " + tier + ": " + str(counts[tier]))
    return "\n".join(lines)
