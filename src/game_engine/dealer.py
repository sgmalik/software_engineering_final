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
import pygame


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

        self.game_over = False


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
        pygame.time.delay(1000)
        self.betting_manager.apply_player_action(
            self.table.current_player, Action.SMALL_BLIND)

        pygame.time.delay(1000)
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

        if cards_needed == 0:
            return
        
        self.table.deal_community_cards(cards_needed)

    def is_round_over(self) -> bool:
        """
        ignoring not 1v1 for now. 
        """
        # a player folded
        if len(self.table.players_in_hand()) == 1:
            return True
        
        #showdown conditions met
        if self.is_showdown():
            return True

        return False
        
    
    def is_showdown(self) -> bool:
        """
        showdown happens when betting round is over, and its end of river
        or a player is all in and river is over
        """

        # If any player has folded, don't do showdown (pot already distributed in _fold)
        if any(player.state == PlayerState.FOLDED for player in self.table.players):
            return False

        #check if betting is over
        if not self.betting_manager.is_betting_over():
            return False

        #if river is over showdown 
        if self.current_street == Street.RIVER:
            return True
            
        #if a player is all in + betting over showdown
        if len(self.table.players_in_hand()) == 2:
            if any(player.state == PlayerState.ALLIN for player in self.table.players_in_hand()):
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
        #draw more cards if needed
        self._start_showdown()

        winners = GameEvaluator.determine_winners(self.table)
        GameEvaluator.add_money_to_winners(self.table, winners)

        #think blinds are getting through first so negative stack happens
        for player in self.table.players:
            if player.stack <= 0:
                self.game_over = True
    
