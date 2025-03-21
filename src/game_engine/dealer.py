from .deck import Deck
from .constants import Street
from .table import Table
from .constants import Action


class Dealer:
    def __init__(self, blind, initial_stack):

        self.current_street = Street.PREFLOP
        self.current_bet = 2
        self.blind = blind
        self.initial_stack = initial_stack
        self.pot = 0
        # setting num_players to 2 for now
        self.table = Table(num_players=2)

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
        elif self.current_street == Street.SHOWDOWN:
            self._showdown()
        elif self.current_street == Street.FINISHED:
            self._finished()

    # define helper functions as needed, function that calls declare action preflop,
    # flop, turn, river

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

    # call game_evaluator here
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
        raise the bet by the amount
        """
        self.table.current_player.bet(amount)
        self.current_bet += amount

    def apply_player_action(self, action: Action):
        """
        declare action for the current player
        """
        #TODO: check if player has folded
        #TODO: check if player has enough stack to call or raise
        if action == Action.CALL:
            self.table.current_player.bet(self.current_bet)
        elif action == Action.RAISE:
            pass
        elif action == Action.FOLD:
            pass
        elif action == Action.BIG_BLIND:
            self.table.current_player.bet(self.blind*2)
        elif action == Action.SMALL_BLIND:
            self.table.current_player.bet(self.blind)
