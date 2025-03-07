from enum import Enum

class Action(Enum):
    FOLD  = 0
    CALL  = 1
    RAISE = 2
    SMALL_BLIND = 3
    BIG_BLIND = 4
    ANTE = 5

class Street(Enum):
    PREFLOP = 0
    FLOP = 1
    TURN = 2
    RIVER = 3
    SHOWDOWN = 4
    FINISHED = 5

class PlayerState(Enum): 
    ACTIVE = 0
    FOLDED = 1
    ALLIN = 2
    WAITING = 3
    WINNER = 4
