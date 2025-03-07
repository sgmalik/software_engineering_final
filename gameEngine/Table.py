from Player import Player
from Deck import Deck
from Constants import Street
class Table: 
    def __init__(self, num_players, blind, initial_stack):
        self.blind_pos = None
        self.community_cards = []
        self.pot = 0

        #Going to play 1v1 for now
        self.num_players = 2

        self.deck: Deck = Deck()
        self.players: list[Player] = [Player(initial_stack) for _ in range(num_players)]
        self.current_player: Player = self.players[0]
        self.current_street: Street = Street.PREFLOP

    def deal_hole_cards(self):
        for player in self.players:
            player.hole_cards = self.deck.draw_cards(2)
    
    def deal_community_cards(self, num_cards):
        self.community_cards += self.deck.draw_cards(num_cards)
    
    def start_next_round(self):
        pass
    
    #round = preflop, flop, turn, river (use enum)
    def round(self):
        pass

    # define helper functions as needed, function that calls declare action preflop, flop, turn, river
    def preflop(params):
        pass
    
    # function that calls declare action on flop
    def flop(params):
        pass
    
    # function that calls declare action on turn
    def turn(params):
        pass

    # function that calls declare action on river
    def river(params):
        pass

    def reset_table(self):
        pass

    def set_current_player(self):
        pass
    