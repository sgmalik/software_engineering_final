from Player import Player
from Deck import Deck

class Engine:
    def __init__(self, num_players, blind, initial_stack):
        self.num_players = num_players
        self.blind = blind
        self.starting_stack = initial_stack
        
        self.deck: Deck = Deck()
        self.players: list[Player] = [Player(initial_stack) for _ in range(num_players)]

    
    

