"""
dealer.py is adapted from pypokerengine's RoundManager class  
"""
from typing import Optional
from .deck import Deck
from .constants import Street
from .table import Table
from .constants import Action
from .constants import PlayerState
from .player import Player
from .betting_manager import BettingManager
from .game_evaluator import GameEvaluator


class Dealer:
    """
    dealer provides manages street state, and provides functions to 
    """

    def __init__(self, initial_stack, small_blind):

        self.current_street = Street.PREFLOP
        self.blind = small_blind
        self.initial_stack = initial_stack

        self.table = Table()
        self.table.init_players(initial_stack=initial_stack, num_players=2)

        self.betting_manager = BettingManager(self.table, self.blind)

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

    def start_street(self):
        """
        start the round by calling street functions
        """

        # reset betting round information
        self.betting_manager.reset_betting_round()

        if self.current_street == Street.PREFLOP:
            self._start_preflop()
        elif self.current_street == Street.FLOP:
            self._start_flop()
        elif self.current_street == Street.TURN:
            self._start_turn()
        elif self.current_street == Street.RIVER:
            self._start_river()

    # these street functions will do what needs to be done at the start of a street to set up the betting round
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

    def _start_showdown(self):
        """
        draw the remaining cards (if any)
        """
        cards_needed = 5 - len(self.table.community_cards)
        self.table.deal_community_cards(cards_needed)


    def is_round_over(self) -> bool:
        """
        the round is over when betting is over on the
        river street 

        or

        all but one players have folded 
        """
        if self.is_showdown():
            return True
        if len(self.table.active_players()) == 1:
            return True
        return False

    def is_showdown(self):
        """
        check if the round is over and we need to do showdown logic
        """
        
        if self.betting_manager.is_betting_over() is not True:
            return False
        
        players_all_in = 0
        for player in self.table.players:
            if player.is_allin():
                players_all_in += 1
        
        #if there's only 1 player that's not all_in at end of betting round, showdown
        if players_all_in >= len(self.table.players) - 1:
            return True

        #if river betting is over showdown
        if self.current_street == Street.RIVER:
            return True
        
        return False
        

    def apply_action(self, action: Action, raise_amount: Optional[int] = None):
        """
            wrapper for betting manager 
        """
        current_player = self.table.current_player
        self.betting_manager.apply_player_action(
            current_player, action, raise_amount)

    def set_up_next_round(self):
        """
        reset table and betting manager for the next round
        """
        self.current_street = Street.PREFLOP
        self.table.reset_table()
        self.betting_manager.reset_betting_round()

    def showdown(self):
        """
        this will be called when the round is over and we need to determine the winner/winners
        """

        winners = GameEvaluator.determine_winners(self.table)
        print("THIS IS WINNERS", winners)
        GameEvaluator.add_money_to_winners(self.table, winners)
    

