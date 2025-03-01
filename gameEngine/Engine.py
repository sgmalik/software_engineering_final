from pypokerengine.players import BasePokerPlayer
from pypokerengine.api.game import setup_config, start_poker
from FishPlayer import FishPlayer 
from GUIPlayer import GUIPlayer

from Player import Player
from Deck import Deck

class Engine():
    def __init__(self, num_players, blind, initial_stack):
        self.num_players = num_players
        self.blind = blind
        self.initial_stack = initial_stack

        self.deck: Deck = Deck()
        self.players: list[Player] = [Player(initial_stack) for _ in range(num_players)]

    
    def start_game(self):
        config = setup_config(max_round=10, initial_stack= self.initial_stack, small_blind_amount=self.blind)
        config.register_player(name="fish_player", algorithm=FishPlayer())
        config.register_player(name="human_player", algorithm=GUIPlayer())
        game_result = start_poker(config, verbose=0)  # verbose=0 because game progress is visualized by ConsolePlayer

    def get_hole_cards(self):
        pass

    #In gui wait for player action, and then call this func when player does something    
    def player_action(button_action):
        return button_action
        
        

    
    

