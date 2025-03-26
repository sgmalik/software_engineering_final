"""
This module contains the Player class
"""
from .constants import PlayerState


class Player:
    """
    represents a player in the game
    """

    def __init__(self, initial_stack, name):
        self.hole_cards = []
        self.stack = initial_stack
        self.state = PlayerState.ACTIVE
        self.contribuition = 0
        self.name = name

    #eq's for removing from pending_betters, assuming names are unique
    def __eq__(self, other_player):
        if isinstance(other_player, Player):
            return self.name == other_player.name
        return False

    def clear_hole_cards(self):
        """
        clears the hole cards of the player
        """
        self.hole_cards = []

    def fold(self):
        """
        changes playerState to folded
        """
        self.state = PlayerState.FOLDED

    def add_to_stack(self, amount):
        """
        add amount to player's stack
        """
        self.stack += amount

    def bet(self, amount):
        """
        bet amount from player's stack
        """
        self.stack -= amount
        self.contribuition += amount
