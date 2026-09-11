"""
App: the controller. Owns the Tk root window and the GameState, and swaps
screens in and out. Screens (in screens/) never talk to each other directly
-- they only call back through this App and read app.game.
"""

from constants import WINDOW_TITLE, WINDOW_SIZE
from game_state import GameState
from screens import (
    title_screen,
    game_screen,
    collection_screen,
    history_screen,
    end_screen,
)


class App:
    def __init__(self, root):
        self.root = root

        # Window settings
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)
        self.root.resizable(True, True)

        # Game state
        self.game = GameState()

        # Widget references for the active screen
        self.widgets = {}

        # Start with title screen
        self.show_title()

    # ------------------------------------------------------------
    # CLEAR CURRENT SCREEN
    # ------------------------------------------------------------

    def clear_window(self):
        """Remove everything from the main window."""

        # Remove resize bindings owned by the current screen before its
        # widgets are destroyed. The next screen can safely bind its own
        # <Configure> handler.
        self.root.unbind("<Configure>")

        for widget in self.root.winfo_children():
            widget.destroy()

        self.widgets = {}

    # ------------------------------------------------------------
    # SCREEN SWITCHES
    # ------------------------------------------------------------

    def show_title(self):
        """Show the title screen."""
        self.clear_window()
        title_screen.build(self)

    def show_game(self):
        """Show the main battle/game screen."""
        self.clear_window()
        game_screen.build(self)
        game_screen.advance_round(self)

    def show_end(self):
        """Show the game-over/end screen."""
        self.clear_window()
        end_screen.build(self)

    def open_collection(self):
        """Open the Collection screen over the current game screen."""
        # Do NOT clear the game screen because Collection is a Toplevel window.
        collection_screen.open_window(self)

    def open_history(self):
        """Open the History screen over the current game screen."""
        # Do NOT clear the game screen because History is a Toplevel window.
        history_screen.open_window(self)

    # ------------------------------------------------------------
    # GAME FLOW
    # ------------------------------------------------------------

    def start_game(self, trainer_name):
        """Start a new game using the given trainer name."""
        self.game.trainer_name = trainer_name
        self.game.reset()
        self.show_game()
