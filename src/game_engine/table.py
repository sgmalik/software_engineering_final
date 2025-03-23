"""
table class
"""
from .player import Player
from .deck import Deck
from .constants import Street
from .constants import Action


class Table:
    """
    represents the table of the game
        players: list of players
        deck: deck of cards
        current_player: player whose turn it is
        current_street: current street of the game
        current_bet: current bet amount
        blind_pos: position of the blind

    """

    def __init__(self, num_players, blind, initial_stack):
        self.blind_pos = None
        self.community_cards = []
        self.pot = 0

        # Going to play 1v1 for now
        self.num_players = 2

        self.deck: Deck = Deck()
        self.players: list[Player] = [
            Player(initial_stack) for _ in range(num_players)]
        self.current_player: Player = self.players[0]
        self.current_street: Street = Street.PREFLOP
        self.current_bet = 2

    def deal_hole_cards(self):
        """
        deal 2 cards to each player
        """
        for player in self.players:
            player.hole_cards = self.deck.draw_cards(2)

    def deal_community_cards(self, num_cards):
        """
        deal num_cards to the community cards
        """
        self.community_cards += self.deck.draw_cards(num_cards)

    def next_street(self):
        """
        changes the current street to the next street
        """

    # use current player to do an action ["bet", "raise", "fold"]
    def declare_action(self, action: Action):
        """
        declare action for the current player
        """
        if action == Action.CALL:
            self.current_player.bet(self.current_bet)
        elif action == Action.RAISE:
            pass
        elif action == Action.FOLD:
            pass
        elif action == Action.BIG_BLIND:
            pass
        elif action == Action.SMALL_BLIND:
            pass

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
        self.deal_community_cards(3)
        self.next_street()

    # function that calls declare action on turn
    def turn(self):
        """
        do turn actions
        """
        self.deal_community_cards(1)
        self.next_street()

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

    def reset_table(self):
        """
        set up table for next round
        """

    # set this to whos turn it is
    def set_current_player(self):
        """
        set current player to the next player
        """

   
    def raise_bet(self, amount):
        """
        raise the bet by the amount
        """
        self.current_player.bet(amount)
        self.current_bet += amount
