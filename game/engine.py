## psuedo code for the engine if we decide to implement our own

class Engine: 
    # use baseModel from pypokerengine??
    def __init__(self, players):
        self.players = players

    # params is the configs for game setup
    def starting_state(params):
        pass

    # takes player, and returns current state of player to ensure still in hand
    def current_state_of_player(player):
        pass

    # function that returns the current state of the game
    def current_state_of_game(params):
        pass

    # takes pot, and adds money based on previous action, handles reduction of players stacks
    def calculate_pot(params):
        pass

    # to handle action of player can fold, call, or raise (of valid size), sends to other player who has same options
    def declare_action(params):
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

    # use hand_evaluator to evaluate hands from each plaer (pyPokerEngine)

    # function that returns winner of hand
    def winner(params):
        pass

    # function that returns the pot size
    def pot_size(params):
        pass
    

    # keep in mind, every fuinction will need to have some sort of call to the relevant graphics or vice versa to make sure game is displayed correctly
    # rip code from pypokerengine to get the basic functionality down, adjust as needed, already made a lot of adjustments just to make sure it's compatible with current version of python
    # moreover, will utilize emulator from pypokerengine to improve player types, thinking can allow difficulty for cpu player and then expand to multi player tables of varying skill levels with leftover time
