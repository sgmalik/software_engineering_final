from .deck import Deck
from .constants import Street
from .table import Table
from .constants import Action
from .constants import PlayerState
from typing import Optional


class Dealer:
    def __init__(self, blind, initial_stack):

        self.current_street = Street.PREFLOP
        self.current_bet = 2
        self.blind = blind
        self.initial_stack = initial_stack
        self.pot = 0
        # setting num_players to 2 for now
        self.table = Table()

     # street = preflop, flop, turn, river (use enum)
    def start_street(self):
        """
        start the round by calling street functions
        """
        if self.current_street == Street.PREFLOP:
            self._preflop()
        elif self.current_street == Street.FLOP:
            self._flop()
        elif self.current_street == Street.TURN:
            self._turn()
        elif self.current_street == Street.RIVER:
            self._river()
    
    
    #these street functions will do what needs to be done at the start of a street to set up the betting round
        #dealer cards, blinds, etc
    def _preflop(self):
        """
        do preflop actions 
        """
        self.table.deal_hole_cards()

        # blinds
        self.apply_player_action(Action.SMALL_BLIND)
        self.table.next_player()
        self.apply_player_action(Action.BIG_BLIND)
        self.table.next_player()
        
        #deal hole cards
        self.table.deal_hole_cards()

    # function that calls declare action on flop
    def _flop(self):
        """
        do flop actions
        """
        self.table.deal_community_cards(3)

    # function that calls declare action on turn
    def _turn(self):
        """
        do turn actions
        """
        self.table.deal_community_cards(1)

    # function that calls declare action on river
    def _river(self):
        """
        do river actions
        """
        self.table.deal_community_cards(1)
    
    def _showdown(self):
        """
        use game_eval to determine winners
        """

    def _finished(self):
        """
        call when round is over to reset what we need to
        """

    def _next_street(self):
        """
        changes the current street to the next street
        """

    def _raise_bet(self, amount):
        """
        raise the current bet by the amount (this is so we can keep track of the current bet)
        """
        current_player = self.table.players[self.table.current_player_index]

        #take amount from player's stack
        current_player.bet(amount)
        self.current_bet += amount

    def apply_player_action(self, action: Action, raise_amount: Optional[int] = None):
        """
        declare action for the current player
        """
        #NOTE: 
        #TODO: check if player has folded
        #TODO: check if player has enough stack to call or raise
        current_player = self.table.players[self.table.current_player_index]

        if action == Action.CALL:
            current_player.bet(self.current_bet)
        elif action == Action.RAISE:
            self._raise_bet(raise_amount)
        elif action == Action.FOLD:
            #TODO: replace this with player fold function 
            current_player.state = PlayerState.FOLDED
        elif action == Action.BIG_BLIND:
            current_player.bet(self.blind*2)
        elif action == Action.SMALL_BLIND:
            current_player.bet(self.blind)

    def is_players_turn(self) -> bool:
        """
        check if it is the players turn, this is a helper function so we don't have to do this in GUI code
        """
        player = self.table.players[self.table.current_player_index]
        #TODO: replace with is active player func
        return player.name == "pc" and self.table.players[self.table.current_player_index].state == PlayerState.ACTIVE
