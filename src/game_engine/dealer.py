from typing import Optional
from .deck import Deck
from .constants import Street
from .table import Table
from .constants import Action
from .constants import PlayerState
from .player import Player
from .round_manager import RoundManager
from .player_action import PlayerAction

# TODO: need to track contribuitions for raises to be correct


class Dealer:
    def __init__(self, small_blind, initial_stack):

        self.current_street = Street.PREFLOP
        self.current_bet = 0
        self.blind = small_blind
        self.initial_stack = initial_stack
        # setting num_players to 2 for now
        self.table = Table()
        self.round_manager = RoundManager(self, self.table)
        self.player_action = PlayerAction(self, self.table, self.round_manager)

        # this array represents active
        # players who haven't responded to a bet yet
        self.pending_betters = []

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
        if self.current_street == Street.PREFLOP:
            self.round_manager.start_preflop()
        elif self.current_street == Street.FLOP:
            self.round_manager.start_flop()
        elif self.current_street == Street.TURN:
            self.round_manager.start_turn()
        elif self.current_street == Street.RIVER:
            self.round_manager.start_river()

        # add all active players to pending_betters, at start of street
        # all active players are pending betters
        self.pending_betters = self.table.active_players()

        # reset player contributions at start of street
        self.table.reset_contribuition()

    # these street functions will do what needs to be done at the start of a street to set up the betting round
        # dealer cards, blinds, etc



    def is_betting_over(self) -> bool:
        """
        check if betting is over (to be used in game_engine),
        if betting is over than the street is over 
        """
        # so going to have pending actions array. players that are still active will go in the array
        # so if they check they aren't in the array anymore
        # if they raise all the other players are in the array as well
        # if betting is over need to set current bet to 0 (in game_engine)

        # should this check if every other player is folded.

        # when checking if betting is over and thats true, you should check if the round is over
        return len(self.pending_betters) == 0 or len(self.table.active_players()) == 1

    
    def is_round_over(self) -> bool:
        """
        the round is over when betting is over on the
        river street 

        or

        all but one players have folded 
        """
        if self.current_street == Street.RIVER and self.is_betting_over():
            return True
        if len(self.table.active_players()) == 1:
            return True
        return False
    
    def apply_player_action(self, action: Action, raise_amount: Optional[int] = None):
        """
        declare action for the current player
        """
        # TODO: check if player has folded
        # TODO: check if player has enough stack to call or raise

        if action == Action.CALL:
            self.player_action.call()
        elif action == Action.RAISE:
            self.player_action.raise_by_amount(raise_amount)
        elif action == Action.FOLD:
            # TODO: replace this with player fold function
            self.player_action.fold()
        elif action == Action.SMALL_BLIND:
            self.player_action.blind(self.blind)
        elif action == Action.BIG_BLIND:
            self.player_action(self.blind*2)
            self.current_bet = self.blind*2
        self.table.next_player()

    
    def raise_bet(self, amount):
        """
        raise the current bet by the amount (this is so we can keep track of the current bet)
        """
        self.current_bet += amount
    
    
    
    
