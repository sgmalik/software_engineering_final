from Deck import Deck
from enum import Enum
from Constants import Action
from Constants import PlayerState


class Player:
    def __init__(self, initial_stack):
        self.hole_cards = []
        self.stack = initial_stack
        self.state = PlayerState.ACTIVE
        self.contribuition = 0

    def clear_hole_cards(self):
        self.hole_cards = []

    def fold(self):
        self.state = PlayerState.FOLDED

    def add_to_stack(self, amount):
        self.stack += amount

    def bet(self, amount):
        self.stack -= amount
        self.contribuition += amount
