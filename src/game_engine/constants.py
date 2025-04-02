"""
enums to be used in the game engine 
"""
from enum import Enum

class Action(Enum):
    """
    represents the actions a player can take
    """
    FOLD  = "fold"
    CALL  = "call"
    RAISE = "raise"
    SMALL_BLIND = "sb"
    BIG_BLIND = "bb"
    ANTE = "ante"

class Street(Enum):
    """
    current poker street
    """
    PREFLOP = 0
    FLOP = 1
    TURN = 2
    RIVER = 3
    SHOWDOWN = 4
    FINISHED = 5

class PlayerState(Enum): 
    """
    whether the player is active, folded, allin, waiting, or winner
    """
    ACTIVE = 0
    FOLDED = 1
    ALLIN = 2
    WAITING = 3
    WINNER = 4
