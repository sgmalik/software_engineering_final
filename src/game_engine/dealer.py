from typing import Optional
from .deck import Deck
from .constants import Street
from .table import Table
from .constants import Action
from .constants import PlayerState
from .player import Player

# TODO: need to track contribuitions for raises to be correct


class Dealer:
    def __init__(self, small_blind, initial_stack):

        self.current_street = Street.PREFLOP
        self.current_bet = 0
        self.blind = small_blind
        self.initial_stack = initial_stack
        self.pot = 0
        # setting num_players to 2 for now
        self.table = Table()

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
            self._start_preflop()
        elif self.current_street == Street.FLOP:
            self._start_flop()
        elif self.current_street == Street.TURN:
            self._start_turn()
        elif self.current_street == Street.RIVER:
            self._start_river()

        # add all active players to pending_betters, at start of street
        # all active players are pending betters
        self.pending_betters = self.table.active_players()

        # reset player contributions at start of street
        self.table.reset_contribuition()

    # these street functions will do what needs to be done at the start of a street to set up the betting round
        # dealer cards, blinds, etc

    def _start_preflop(self):
        """
        do preflop actions 
        """
        self.table.deal_hole_cards()

        # blinds
        self.apply_player_action(Action.SMALL_BLIND)
        self.apply_player_action(Action.BIG_BLIND)

   

    def _start_flop(self):
        """
        do start of flop actions
        """
        self.table.deal_community_cards(3)
        self._reset_current_bet()

   
    def _start_turn(self):
        """
        do start of turn actions
        """
        self.table.deal_community_cards(1)
        self._reset_current_bet()

    
    def _start_river(self):
        """
        do start of river actions
        """
        self.table.deal_community_cards(1)
        self._reset_current_bet()

    def _raise_bet(self, amount):
        """
        raise the current bet by the amount (this is so we can keep track of the current bet)
        """
        self.current_bet += amount

    def apply_player_action(self, action: Action, raise_amount: Optional[int] = None):
        """
        declare action for the current player
        """
        # TODO: check if player has folded
        # TODO: check if player has enough stack to call or raise

        if action == Action.CALL:
            self._call()
        elif action == Action.RAISE:
            # we need to pay the current bet before we can raise
            self._raise(raise_amount)
        elif action == Action.FOLD:
            # TODO: replace this with player fold function
            self._fold()
        elif action == Action.SMALL_BLIND:
            self._blind(self.blind)
        elif action == Action.BIG_BLIND:
            self._blind(self.blind*2)
            self.current_bet = self.blind*2
        self.table.next_player()

    def _blind(self, blind):
        self.table.current_player.bet(blind)
        self._add_to_pot(blind)

    def _fold(self):
        self.table.current_player.state = PlayerState.FOLDED
        self._remove_better(self.table.current_player)

    def _raise(self, raise_amount):
        # need to pay current bet first
        call_amount = self.current_bet - self.table.current_player.contribuition
        self.table.current_player.bet(call_amount)
        self._add_to_pot(call_amount)

        # do the raise action
        self._raise_bet(raise_amount)
        self.table.current_player.bet(raise_amount)
        self._add_to_pot(raise_amount)
        self._add_betters(self.table.current_player)

    def _call(self):
        call_amount = self.current_bet - self.table.current_player.contribuition
        self.table.current_player.bet(call_amount)

        self._add_to_pot(call_amount)
        self._remove_better(self.table.current_player)

    def is_players_turn(self) -> bool:
        """
        check if it is the players turn, this is a helper function so we don't have to do this in GUI code
        """
        player = self.table.current_player
        # TODO: replace with is active player func
        return player.name == "pc" and player.state == PlayerState.ACTIVE

    def _add_to_pot(self, amount):
        """
        add amount to pot
        """
        self.pot += amount

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

    def _remove_better(self, current_player):
        """
        remove current player from current_betters
        """
        self.pending_betters.remove(current_player)

    def _add_betters(self, current_player):
        """
        add all other active players to current betters
        this will be called when a player raises the bet
        """
        self.pending_betters = []
        for player in self.table.active_players():
            if player != current_player:
                self.pending_betters.append(player)

    def _reset_current_bet(self):
        """
        reset current bet to 0
        """
        self.current_bet = 0

    # TODO: should probably be table function
   

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
