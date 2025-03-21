from dealer import Dealer
"""
Poker Engine
"""

class Engine():
    """
This is what we will call in the GUI to update it.

It needs to return information that the GUI needs
    the GUI needs:
        all players stacks
        all players hole cards
        community cards 
        each player's state (if they folded or not)
        pot 
"""

    #pass a settings config when creating class to set up game
    def __init__(self, num_players, blind, initial_stack):
        self.num_players = num_players
        self.blind = blind
        self.initial_stack = initial_stack
        self.dealer = Dealer(self.blind, self.initial_stack)
    
    
    def start_game(self):
        """
        function that will be called when starting up the GUI
        """

        #initialize players
        self.dealer.table.init_players(self.initial_stack, self.num_players)

        #start preflop street 
        self.dealer.start_street()

    def current_state_of_player(self):
        """
        takes player, and returns current state of player to ensure still in hand
        """

    def current_state_of_game(self):
        """
        create a data structure so that the GUI can display the current state of the game
        """

    def winners(self):
        """
        use game_eval to determine winners
        """

    def pot_size(self):
        """
        gets the pot size to display in GUI
        """
