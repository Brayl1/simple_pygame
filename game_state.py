"""
GameState holds every gameplay list and the rules that change them.

This is deliberately UI-free: no tkinter import here at all. Screens call
these methods and read these lists to know what to display. That
separation is what makes the "normal game" structure -- engine vs. view.
"""

import random

from constants import (
    RARITY_SCORES,
    RARITY_ORDER,
    WIN_THRESHOLD,
    STARTING_ORBS,
    STARTING_CANDY,
    CANDY_DIFFICULTY_REDUCTION,
)
from monsters_data import MONSTER_TEMPLATES


class GameState:
    def __init__(self):
        self.trainer_name = "Trainer"
        self.reset()

    # ------------------------------------------------------------------
    # SETUP / RESET
    # ------------------------------------------------------------------

    def reset(self):
        # >>> Rubric requirement 1: at least four meaningful lists
        self.inventory = ["Capture Orb"] * STARTING_ORBS              # list 1
        self.candies = ["Rare Candy"] * STARTING_CANDY                # list 2
        self.captured_monsters = []                                    # list 3
        self.encounter_history = []                                    # list 4 (nested)

        # Deep-copy every row so mutating a monster in play (Rare Candy)
        # never touches the master MONSTER_TEMPLATES data.
        self.encounters = [row.copy() for row in MONSTER_TEMPLATES]    # list 5 (nested)

        self.score = 0
        self.round_number = 0
        self.current_monster = None
        self.candy_used_this_round = False

    # ------------------------------------------------------------------
    # ENCOUNTER FLOW
    # ------------------------------------------------------------------

    def is_game_over(self):
        return len(self.encounters) == 0 or len(self.inventory) == 0

    def start_next_encounter(self):
        self.round_number += 1
        self.candy_used_this_round = False

        index = random.randint(0, len(self.encounters) - 1)  # list indexing
        self.current_monster = self.encounters[index]
        return self.current_monster

    def use_candy(self):
        if not self.candies or self.current_monster is None or self.candy_used_this_round:
            return False

        self.candies.pop()                     # pop() during gameplay
        self.candy_used_this_round = True

        # >>> Rubric requirement 6: UPDATE an element via list indexing
        self.current_monster[1] = max(1, self.current_monster[1] - CANDY_DIFFICULTY_REDUCTION)
        return True

    def attempt_capture(self):
        self.inventory.pop()  # consume a Capture Orb

        name, difficulty, rarity, ability = self.current_monster
        roll = random.randint(1, 10)
        success = roll >= difficulty

        if success:
            self.captured_monsters.append(self.current_monster)  # append()
            self.score += RARITY_SCORES.get(rarity, 0)
            result = "CAPTURED"
        else:
            result = "ESCAPED"

        self.encounter_history.append([self.round_number, name, result, roll])  # append()
        self.encounters.remove(self.current_monster)  # remove()
        return success, roll

    def skip_current(self):
        name = self.current_monster[0]
        self.encounter_history.append([self.round_number, name, "SKIPPED", "-"])
        self.encounters.remove(self.current_monster)

    # ------------------------------------------------------------------
    # INFO / DISPLAY HELPERS
    # ------------------------------------------------------------------

    def rarity_breakdown(self):
        rarities = [monster[2] for monster in self.captured_monsters]
        return {tier: rarities.count(tier) for tier in RARITY_ORDER}  # count()

    def sort_captured_alphabetically(self):
        self.captured_monsters.sort(key=lambda monster: monster[0])  # sort()

    def find_captured(self, name):
        target = name.strip().lower()
        for monster in self.captured_monsters:  # traversal + search
            if monster[0].lower() == target:
                return monster
        return None

    def is_win(self):
        return len(self.captured_monsters) >= WIN_THRESHOLD

    def trainer_rank(self):
        if self.score >= 150:
            return "Platinum Trainer"
        elif self.score >= 100:
            return "Gold Trainer"
        elif self.score >= 50:
            return "Silver Trainer"
        return "Bronze Trainer"
