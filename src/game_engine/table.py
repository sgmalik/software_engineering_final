"""
table class adapted from table.py in pypokerengine 
https://github.com/ishikota/PyPokerEngine/blob/master/pypokerengine/engine/table.py
"""
from .player import Player
from .deck import Deck
from .constants import Street
from .constants import Action
from .constants import PlayerState
from .pot import Pot


class Table:
    """
    Table will be responsible for keeping track of players and
    dealing cards 
    """

    def __init__(self):

        self.blind_pos = 1
        self.community_cards = []

        self.deck: Deck = Deck()
        self.pot = Pot()
        self.players: list[Player] = []
        self.current_player = None

    def init_players(self, initial_stack, num_players):
        """
        initialize players with initial stack
        """
        # if not pc, cpu1, cpu2, etc
        for i in range(num_players):
            self.players.append(Player(initial_stack, f"cpu{i}"))

        # name gui player pc
        self.players[0].name = "pc"

        # init current player to first player
        self.current_player = self.players[0]

    def reset_table(self):
        """
        set up table for next round
        """
        # clear dealer community cards
        # clear player's hole_cards
        self.deck = Deck()
        self.community_cards = []
        self.pot.value = 0

        for player in self.players:
            player.clear_hole_cards()
            player.contribuition = 0
            player.state = PlayerState.ACTIVE
        
        self.set_blind_pos()
        #change to the player paying the small blind
        self.current_player = self.players[self.blind_pos]

    # set this to whos turn it is
    def next_player(self):
        """
        set current player to the next player
        """
        # For heads up, don't need to change this because when a player folds the round is over
        # more players needs to be based on active players
        if self.current_player == self.players[1]:
            self.current_player = self.players[0]
        else:
            self.current_player = self.players[1]

    def deal_hole_cards(self):
        """
        deal 2 cards to each player
        """
        for player in self.players:
            player.hole_cards = self.deck.draw_cards(2)

    def set_blind_pos(self):
        """
        start of the round set the small blind pos,
        since we are playing heads up, for now just swapping between
        2 players
        """
        if self.blind_pos == 0:
            self.blind_pos = 1
        else:
            self.blind_pos = 0

    def deal_community_cards(self, num_cards):
        """
        deal num_cards to the community cards
        """
        self.community_cards += self.deck.draw_cards(num_cards)

    def active_players(self):
        """
        return list of active players
        """
        return [player for player in self.players if player.is_active()]
    
    def not_all_in_players(self):
        return [player for player in self.players if player.state != player.is_allin()]
    
    def players_in_hand(self):
        return [player for player in self.players if player.is_active() or player.is_allin()]

    def reset_contribution(self):
        """
        after every street we need to reset the contribuition of every player
        """
        for player in self.players:
            player.contribuition = 0

    def is_players_turn(self) -> bool:
        """
        check if it is the players turn, this is a helper function so we don't have to do this in GUI code
        """

        # TODO: replace with is active player func
        return self.current_player is not None and self.current_player.name == "pc" and self.current_player.state == PlayerState.ACTIVE
    
    
