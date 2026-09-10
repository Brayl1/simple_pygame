"""
App: the controller. Owns the Tk root window and the GameState, and swaps
screens in and out. Screens (in screens/) never talk to each other directly
-- they only call back through this App and read app.game.
"""

from constants import WINDOW_TITLE, WINDOW_SIZE
from game_state import GameState
from screens import title_screen, game_screen, collection_screen, history_screen, end_screen


class App:
    def __init__(self, root):
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)
        self.root.resizable(False, False)

        self.game = GameState()

        # Widget references the active screen needs to update live.
        # Screens store into this dict instead of using globals.
        self.widgets = {}

        self.show_title()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.widgets = {}

    # ---- screen switches ------------------------------------------------

    def show_title(self):
        self.clear_window()
        title_screen.build(self)

    def show_game(self):
        self.clear_window()
        game_screen.build(self)
        game_screen.advance_round(self)

    def show_end(self):
        self.clear_window()
        end_screen.build(self)

    def open_collection(self):
        collection_screen.open_window(self)

    def open_history(self):
        history_screen.open_window(self)

    # ---- flow control -----------------------------------------------

    def start_game(self, trainer_name):
        self.game.trainer_name = trainer_name
        self.game.reset()
        self.show_game()
