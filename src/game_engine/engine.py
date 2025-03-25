
"""
Poker Engine
"""

from .dealer import Dealer
from .constants import Action

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
        takes player, and returns current state of player to ensure still in hand.
        This will be useful in the GUI to gray out player buttons when
            1. player has folded
            2. player is all in
            3. player has already bet
            4. its not the players turn
        """

    def current_state_of_game(self):
        """
        create a data structure so that the GUI can display the current state of the game
        """
        #get the players stacks and cards
        street = self.dealer.current_street
        community_cards = self.dealer.table.community_cards
        players = [
        {
                "name": player.name,
                "stack": player.stack,
                "hole_cards": player.hole_cards,
                "state": player.state
        } for player in self.dealer.table.players]

        return {
            street: street,
            community_cards: community_cards,
            players: players
        }
            

    def start_next_street(self):
        """
        function that will be called when the street is over
        """
        self.dealer.start_street()
        

    def start_next_round(self):
        """
        function that will be called when the round is over
        """
        
        self.dealer.table.reset_table()
        self.dealer.start_street()


    
    def player_action(self, action: str):
        """
        function that will be called when its the players turn
        and they are active in the hand

        this receives the btn string from the GUI 
        """

        #convert string to Action enum
        action = Action(action)

        self.dealer.apply_player_action(action)
        

    def winners(self):
        """
        use game_eval to determine winners
        """

    def pot_size(self):
        """
        gets the pot size to display in GUI
        """
