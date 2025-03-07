from Deck import Deck
from enum import Enum
from Constants import Action
from Constants import PlayerState

class Player:
    def __init__(self, initial_stack):
        self.hole_cards = []
        self.stack = initial_stack
        self.state = PlayerState.ACTIVE

    def player_action(self, action, amount):
        if action == Action.FOLD:
            self.state = PlayerState.FOLDED
        elif action == Action.CALL:
            self.stack -= amount
        elif action == Action.RAISE:
            self.stack -= amount

    def clear_hole_cards(self):
        self.hole_cards = []
    