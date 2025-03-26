from typing import Optional
from .deck import Deck
from .constants import Street
from .table import Table
from .constants import Action
from .constants import PlayerState
from .player import Player

#TODO: need to track contribuitions for raises to be correct
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
        # players who haven't responded to a raise yet
        self.pending_betters = []

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

        # add all active players to pending_betters, at start of street
        # all active players are pending betters
        self.pending_betters = self.table.active_players()

    # these street functions will do what needs to be done at the start of a street to set up the betting round
        # dealer cards, blinds, etc

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

        

    # function that calls declare action on flop
    def _flop(self):
        """
        do flop actions
        """
        self.table.deal_community_cards(3)
        self._reset_current_bet()

    # function that calls declare action on turn
    def _turn(self):
        """
        do turn actions
        """
        self.table.deal_community_cards(1)
        self._reset_current_bet()

    # function that calls declare action on river
    def _river(self):
        """
        do river actions
        """
        self.table.deal_community_cards(1)
        self._reset_current_bet()

    def _next_street(self):
        """
        changes the current street to the next street,
        this should be called when street is over/ betting 
        has concluded .
        """
        if self.current_street == Street.PREFLOP:
            self.current_street = Street.FLOP
        elif self.current_street == Street.FLOP:
            self.current_street = Street.TURN
        elif self.current_street == Street.TURN:
            self.current_street = Street.RIVER

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
        current_player = self.table.current_player

        if action == Action.CALL:
            current_player.bet(self.current_bet)
            self._add_to_pot(self.current_bet)
            self._remove_better(current_player)
        elif action == Action.RAISE:
            #we need to pay the current bet before we can raise
            current_player.bet(self.current_bet)
            self._add_to_pot(self.current_bet)

            #do the raise action
            self._raise_bet(raise_amount)
            current_player.bet(raise_amount)
            self._add_to_pot(raise_amount)
            self._add_betters(current_player)
        elif action == Action.FOLD:
            # TODO: replace this with player fold function
            current_player.state = PlayerState.FOLDED
            self._remove_better(current_player)
        elif action == Action.SMALL_BLIND:
            current_player.bet(self.blind)
            self._add_to_pot(self.blind)
        elif action == Action.BIG_BLIND:
            amount = self.blind*2
            current_player.bet(amount)
            self._add_to_pot(amount)
            self._raise_bet(amount)
           

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
        # if betting is over need to set current bet to 0 (in game_engine )
        return len(self.pending_betters) == 0

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

    