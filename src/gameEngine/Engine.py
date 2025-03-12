from Player import Player
from Deck import Deck

"""
This is what we will call in the GUI to update it.

It needs to return information that the GUI needs
    the GUI needs:
        all players stacks
        the human player's hole cards  
        community cards 
        each player's state (if they folded or not)
        pot 
"""

class Engine():
    def __init__(self, num_players, blind, initial_stack):
        self.num_players = num_players
        self.blind = blind
        self.initial_stack = initial_stack


    def starting_state(params):
        pass

    # takes player, and returns current state of player to ensure still in hand
    def current_state_of_player(player):
        pass

    
    def current_state_of_game(params):
        pass

    # takes pot, and adds money based on previous action, handles reduction of players stacks
    def calculate_pot(params):
        pass

    # to handle action of player can fold, call, or raise (of valid size), sends to other player who has same options
    def declare_action(params):
        pass

    # use hand_evaluator to evaluate hands from each plaer (pyPokerEngine)

    # function that returns winner of hand
    def winner(params):
        pass

    # function that returns the pot size
    def pot_size(params):
        pass
        
        

    
    

