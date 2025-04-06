
"""
Poker Engine
"""

from .dealer import Dealer
from .constants import Action
from typing import Optional

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
    def __init__(self, num_players, initial_stack, blind):
        self.num_players = num_players
        self.blind = blind
        self.initial_stack = initial_stack
        self.dealer = Dealer(self.initial_stack, self.blind)

    def current_state_of_game(self):
        """
        create a data structure so that the GUI can display the current state of the game
        """
        #get the players stacks and cards
        community_cards = self.dealer.table.community_cards


        #TODO: check if game is over (one of the players stack is 0)
        players = [
        {
                "name": player.name,
                "stack": player.stack,
                "hole_cards": [str(card) for card in player.hole_cards],
                "state": player.state.value
        } for player in self.dealer.table.players]

        state = {
            "pot": self.dealer.table.pot.value,
            "game_over": self.is_game_over(),
            "players_turn": self.dealer.table.is_players_turn(),
            "betting_over": self.dealer.betting_manager.is_betting_over(),
            "round_over": self.dealer.is_round_over(),
            "community_cards": [str(card) for card in community_cards],
            "players": players
        }
        
        return state
    
            
    def start_next_street(self):
        """
        function that will be called when the street is over.
        """
        self.dealer.next_street()
        self.dealer.start_street()
        #TODO: check if round is over, if so, call start_next_round
        

    def start_next_round(self):
        """
        function that will be called when the round is over
        (so call this when river is done)
        """
        #maybe just call this in _showdown 
        self.dealer.set_up_next_round()
        self.dealer.start_street()
    
    def player_action(self, action: str, raise_amount: Optional[int] = None):
        """
        function that will be called when its the players turn
        and they are active in the hand

        this receives the btn string from the GUI 
        """
        
        #convert string to Action enum
        #TODO: need to assert that raise is not greater than stack and is less than 
        
        action = Action(action)
        self.dealer.apply_action(action, raise_amount)
        #after we apply the action need to check if the round is over so can do showdown logic
        #calling showdown will change player stack values
        if self.dealer.is_showdown():
            self.dealer.showdown()

        
    def cpu_action(self):
        """
        function that will be called when its the cpu's turn
        """
        #here is where you would get the action from the cpu players
        #then you would call apply_action with that call 
        #CPU is just going to call for now 
        self.dealer.apply_action(Action.CALL)


    def is_game_over(self) -> bool:
        """
        check if the game is over (one of the players stack is 0)
        """
        #check if any of the players stack is 0 
        for player in self.dealer.table.players:
            if player.stack == 0:
                return True
        return False


        



   
