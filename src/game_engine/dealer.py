from .deck import Deck
from .constants import Street
from .table import Table

class Dealer: 
    def __init__(self, blind, initial_stack):
        self.pot = 0
        self.current_street = Street.PREFLOP
        self.current_bet = 2
        self.blind = blind
        self.initial_stack = initial_stack
        #setting num_players to 2 for now 
        self.table = Table(2)

     # round = preflop, flop, turn, river (use enum)
    def start_round(self):
        """
        start the round by calling street functions
        """
        if self.current_street == Street.PREFLOP:
            self.preflop()
        elif self.current_street == Street.FLOP:
            self.flop()
        elif self.current_street == Street.TURN:
            self.turn()
        elif self.current_street == Street.RIVER:
            self.river()
        elif self.current_street == Street.SHOWDOWN:
            self.showdown()
        elif self.current_street == Street.FINISHED:
            self.finished()

    # define helper functions as needed, function that calls declare action preflop,
    # flop, turn, river

    def preflop(self):
        """
        do preflop actions
        """
       
    # function that calls declare action on flop
    def flop(self):
        """
        do flop actions
        """
        self.table.deal_community_cards(3)
        
    # function that calls declare action on turn
    def turn(self):
        """
        do turn actions
        """
        self.table.deal_community_cards(1)
        

    # function that calls declare action on river
    def river(self):
        """
        do river actions
        """

    # call game_evaluator here
    def showdown(self):
        """
        use game_eval to determine winners
        """

    def finished(self):
        """
        call when round is over to reset what we need to
        """
        
    def next_street(self):
        """
        changes the current street to the next street
        """
