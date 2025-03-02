from Player import Player
from Deck import Deck

class Table: 
    def __init__(self):
        self.blind_pos = None
        self.community_cards = []
        self.pot = 0

        self.deck: Deck = Deck()
        self.players: list[Player] = [Player(initial_stack) for _ in range(num_players)]
       
    
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