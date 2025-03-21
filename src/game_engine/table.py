"""
table class
"""
from .player import Player
from .deck import Deck
from .constants import Street
from .constants import Action


class Table:
    """
    Table will be responsible for keeping track of players and
    dealing community cards 
    """

    def __init__(self, num_players):
        self.blind_pos = None
        self.community_cards = []

        self.deck: Deck = Deck()

        # Going to play 1v1 for now
        self.num_players = num_players

        self.players: list[Player] = []
        self.current_player: Player = self.players[0]

    def init_players(self, initial_stack):
        """
        initialize players with initial stack
        """
        self.players = [Player(initial_stack) for _ in range(self.num_players)]

    # use current player to do an action ["bet", "raise", "fold"]
    # def declare_action(self, action: Action):
        """
        declare action for the current player
        """
        # if action == Action.CALL:
        # self.current_player.bet(self.current_bet)
       # elif action == Action.RAISE:
        # pass
       # elif action == Action.FOLD:
        # pass
       # elif action == Action.BIG_BLIND:
        # pass
        # elif action == Action.SMALL_BLIND:
        # pass

    def reset_table(self):
        """
        set up table for next round
        """

    # set this to whos turn it is
    # def set_current_player(self):
        """
        set current player to the next player
        """

    # def raise_bet(self, amount):
        """
        raise the bet by the amount
        """
       # self.current_player.bet(amount)
       # self.current_bet += amount

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
