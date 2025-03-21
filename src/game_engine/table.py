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

    def __init__(self):
        self.blind_pos = None
        self.community_cards = []
        
        self.deck: Deck = Deck()

        # Going to play 1v1 for now

        self.players: list[Player] = []
        self.current_player: Player = self.players[0]

    def init_players(self, initial_stack, num_players):
        """
        initialize players with initial stack
        """
        self.players = [Player(initial_stack) for _ in range(num_players)]

    # use current player to do an action ["bet", "raise", "fold"]
    

    def reset_table(self):
        """
        set up table for next round
        """

    # set this to whos turn it is
    def next_player(self):
        """
        set current player to the next player
        """
        #if end of players list, go back to first player
        if self.current_player == self.players[-1]:
            self.current_player = self.players[0]
        else:
            self.current_player  = self.players[self.current_player + 1]

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
