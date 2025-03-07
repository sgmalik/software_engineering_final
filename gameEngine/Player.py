from Deck import Deck
from enum import Enum
from Constants import Action
from Constants import PlayerState

class Player:
    def __init__(self, initial_stack):
        self.hole_cards = []
        self.stack = initial_stack
        self.state = PlayerState.ACTIVE
    
    

    