from typing import Optional
from .deck import Deck
from .constants import Street
from .table import Table
from .constants import Action
from .constants import PlayerState
from .player import Player
from .betting_manager import BettingManager

# TODO: need to track contribuitions for raises to be correct


class Dealer:
    def __init__(self, initial_stack, small_blind):

        self.current_street = Street.PREFLOP
        self.blind = small_blind

        self.initial_stack = initial_stack
        # setting num_players to 2 for now
        self.table = Table()
        self.betting_manager = BettingManager(self.table, self.blind)

        # this array represents active
        # players who haven't responded to a bet yet

    def next_street(self):
        """
        changes the current street to the next street,
        this should be called when street is over/ betting 
        has concluded.

        call in engine.py
        """
        if self.current_street == Street.PREFLOP:
            self.current_street = Street.FLOP
        elif self.current_street == Street.FLOP:
            self.current_street = Street.TURN
        elif self.current_street == Street.TURN:
            self.current_street = Street.RIVER

     # street = preflop, flop, turn, river (use enum)
    def start_street(self):
        """
        start the round by calling street functions
        """

       
        self.betting_manager.reset_betting_round()
        
        if self.current_street == Street.PREFLOP:
            self._start_preflop()
        elif self.current_street == Street.FLOP:
            self._start_flop()
        elif self.current_street == Street.TURN:
            self._start_turn()
        elif self.current_street == Street.RIVER:
            self._start_river()

        # add all active players to pending_betters, at start of street
        # all active players are pending betters
        

    # these street functions will do what needs to be done at the start of a street to set up the betting round
        # dealer cards, blinds, etc

    def _start_preflop(self):
        """
        do preflop actions 
        """
        self.table.deal_hole_cards()

        # blinds
        self.betting_manager.apply_player_action(
            self.table.current_player, Action.SMALL_BLIND)
        self.betting_manager.apply_player_action(
            self.table.current_player, Action.BIG_BLIND)

    def _start_flop(self):
        """
        do start of flop actions
        """
        self.table.deal_community_cards(3)

    def _start_turn(self):
        """
        do start of turn actions
        """
        self.table.deal_community_cards(1)

    def _start_river(self):
        """
        do start of river actions
        """
        self.table.deal_community_cards(1)

    def is_players_turn(self) -> bool:
        """
        check if it is the players turn, this is a helper function so we don't have to do this in GUI code
        """
        player = self.table.current_player
        # TODO: replace with is active player func
        return player.name == "pc" and player.state == PlayerState.ACTIVE

    def is_round_over(self) -> bool:
        """
        the round is over when betting is over on the
        river street 

        or

        all but one players have folded 
        """
        if self.current_street == Street.RIVER and self.betting_manager.is_betting_over():
            return True
        if len(self.table.active_players()) == 1:
            return True
        return False
    
    def apply_action(self, action: Action, raise_amount: Optional[int] = None):
        """
            wrapper for betting manager 
        """
        current_player = self.table.current_player
        self.betting_manager.apply_player_action(current_player, action, raise_amount)
