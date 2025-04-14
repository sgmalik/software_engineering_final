"""
engine.py is written by us, and loosely based on how pypoker 
keeps track of state. As well as how the game is initialzied. 
"""

from .dealer import Dealer
from .constants import Action, PlayerState
from typing import Optional, Dict, Any
from .cpu.baselineCPU import baselineCPU
from .cpu.equityCPU import equityCPU
from .cpu.potOddsCPU import potOddsCPU
from .cpu.expectedValueCPU import expectedValueCPU
from .cpu.mlCPU import MLCPU
import os

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
        self.cpu_player = None  # Single CPU player
        # Initialize game_info
        self.game_info = {
            'player_num': self.num_players,
            'rule': {
                'initial_stack': self.initial_stack,
                'small_blind': self.blind,
                'max_round': None,  # No limit by default
                'ante': 0  # No ante by default
            },
            'seats': []
        }
        
        # Initialize seats information
        for i, player in enumerate(self.dealer.table.players):
            seat_info = {
                'name': player.name,
                'uuid': f"{player.name}-uuid",  # Simple UUID generation
                'initial_stack': self.initial_stack
            }
            self.game_info['seats'].append(seat_info)
            
        # Create directory for ML model if it doesn't exist
        self.ml_model_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'models')
        if not os.path.exists(self.ml_model_dir):
            os.makedirs(self.ml_model_dir)
            
        # Define the path for the ML model file
        self.ml_model_path = os.path.join(self.ml_model_dir, 'ml_cpu_model.pkl')

    def set_cpu_player(self, cpu_player):
        """
        Set the CPU player for the game.
        
        Args:
            cpu_player: An instance of a CPU player class
        """
        self.cpu_player = cpu_player
        
        # Initialize the CPU player with the initial stack
        cpu_player.stack = self.initial_stack
        
        # Set the name of the CPU player in the table
        self.dealer.table.players[1].name = cpu_player.__class__.__name__
        
        # Update the game_info seats with the CPU player's name
        self.game_info['seats'][1]['name'] = cpu_player.__class__.__name__
        
        # Send game start message to CPU
        self.cpu_player.receive_game_start_message(self.game_info)
    
    def set_cpu_difficulty(self, difficulty):
        """
        Set the difficulty of the CPU player.
        
        Args:
            difficulty: String representing the difficulty level ("easy", "medium", "hard", "ml")
        """
        if difficulty == "easy":
            self.cpu_player = baselineCPU(self.initial_stack)
        elif difficulty == "medium":
            self.cpu_player = equityCPU(self.initial_stack)
        elif difficulty == "hard":
            # Initialize MLCPU with the model path
            self.cpu_player = MLCPU(self.initial_stack, model_path=self.ml_model_path)
            
            # Try to load existing model
            if os.path.exists(self.ml_model_path):
                print(f"Loading model from {self.ml_model_path}")
                self.cpu_player.load_model(self.ml_model_path)
            else:
                print(f"No model found at {self.ml_model_path}, training a new model...")
                # Train the model - it will automatically save to self.ml_model_path
                self.cpu_player.train_model(num_rounds=100, opponent_strategy="random")
                print(f"Model trained and saved to {self.ml_model_path}")
        else:
            # Default to baseline CPU
            self.cpu_player = baselineCPU(self.initial_stack)
            
        # Set the CPU player in the game
        self.set_cpu_player(self.cpu_player)

    def current_state_of_game(self):
        """
        create a data structure so that the GUI can display the current state of the game
        """
        #get the players stacks and cards
        community_cards = self.dealer.table.community_cards
        pc = self.dealer.table.players[0]

        players = []
        for player in self.dealer.table.players:
            max_bet = self.dealer.betting_manager.get_max_raise(player)
            players.append({
                "name": player.name,
                "stack": player.stack,
                "hole_cards": [str(card) for card in player.hole_cards],
                "state": player.state.value,
                "max_bet": max_bet
            })
   
        # Create action histories structure
        action_histories = {
            "preflop": [],
            "flop": [],
            "turn": [],
            "river": []
        }
        
        # Populate action histories from each player
        for player in self.dealer.table.players:
            for i, history in enumerate(player.round_action_histories):
                if history is not None:
                    street_name = list(action_histories.keys())[i]
                    for action in history:
                        action_entry = {
                            "name": action["name"],
                            "action": action["action"].value,
                            "amount": action.get("amount", 0),
                            "add_amount": action.get("add_amount", 0),
                            "paid": action.get("paid", 0),
                            "stack": action.get("stack", player.stack)  # Include stack value from action history
                        }
                        action_histories[street_name].append(action_entry)
   
        state = {
            "player_max_raise": self.dealer.betting_manager.get_max_raise(pc),
            "showdown": self.dealer.is_showdown(),
            "pot": self.dealer.table.pot.value,
            "game_over": self.dealer.game_over,
            "players_turn": self.dealer.table.is_players_turn(),
            "betting_over": self.dealer.betting_manager.is_betting_over(),
            "round_over": self.dealer.is_round_over(),
            "community_cards": [str(card) for card in community_cards],
            "players": players,
            "action_histories": action_histories
        }
        
        return state
    
    def build_round_state(self):
        """
        Create a round_state dictionary that matches the format expected by CPU players.
        This is used to provide information to CPU players for decision making.
        """
        # Get the current street name
        street_name = self.dealer.current_street.name.lower()
        
        # Get the index of the next player to act
        next_player_index = 0
        for i, player in enumerate(self.dealer.table.players):
            if player == self.dealer.table.current_player:
                next_player_index = i
                break
        
        # Get the blind position
        blind_pos = self.dealer.table.blind_pos

        # Format community cards
        community_cards = [str(card) for card in self.dealer.table.community_cards]
        
        # Create pot structure
        pot = {
            "main": self.dealer.table.pot.value,
            "side": []  # Side pots not implemented yet
        }
        
        # Create seats information
        seats = []
        for player in self.dealer.table.players:
            # Map PlayerState to string representation
            state_str = "active"
            if player.state == PlayerState.FOLDED:
                state_str = "folded"
            elif player.state == PlayerState.ALLIN:
                state_str = "allin"
            
            seat = {
                "name": player.name,
                "stack": player.stack,
                "state": state_str
            }
            seats.append(seat)
        
        # Create action histories
        action_histories = {
            "preflop": [],
            "flop": [],
            "turn": [],
            "river": []
        }
        
        # Populate action histories from each player
        for player in self.dealer.table.players:
            for i, history in enumerate(player.round_action_histories):
                if history is not None:
                    street_name = list(action_histories.keys())[i]
                    for action in history:
                        action_entry = {
                            "name": action["name"],
                            "action": action["action"],
                            "amount": action.get("amount", 0),
                            "add_amount": action.get("add_amount", 0),
                            "paid": action.get("paid", 0),
                            "stack": action.get("stack", 0)
                        }
                        action_histories[street_name].append(action_entry)
        
        # Build the complete round_state dictionary
        round_state = {
            "street": street_name,
            "next_player": next_player_index,
            "blind_pos": blind_pos,
            "community_card": community_cards,
            "pot": pot,
            "seats": seats,
            "action_histories": action_histories
        }
        return round_state
            
    def start_next_street(self):
        """
        function that will be called when the street is over.
        """
        if self.dealer.is_round_over():
            print("round over")
            self.start_next_round()
        else:
            # Save action histories for all players before moving to next street
            for player in self.dealer.table.players:
                player.save_round_action_histories(self.dealer.current_street)
            
            self.dealer.next_street()
            self.dealer.start_street()
        
        # Send street start message to CPU if one is set
        if self.cpu_player is not None:
            round_state = self.build_round_state()
            self.cpu_player.receive_street_start_message(
                street=self.dealer.current_street.name.lower(),
                round_state=round_state
            )

    def start_next_round(self):
        """
        function that will be called when the round is over
        (so call this when river is done)
        """
        print("starting next round")
        # Send round start message to CPU if one is set
        if self.cpu_player is not None:
            # Get hole cards for CPU player
            cpu_hole_cards = [str(card) for card in self.dealer.table.players[1].hole_cards]
            
            # Get current seats information
            seats = []
            for player in self.dealer.table.players:
                seat_info = {
                    'name': player.name,
                    'uuid': f"{player.name}-uuid",
                    'stack': player.stack,
                    'state': player.state.value
                }
                seats.append(seat_info)
            
            # Send the message
            self.cpu_player.receive_round_start_message(
                round_count=1,  # You might want to track this
                hole_card=cpu_hole_cards,
                seats=seats
            )
        
        # Update CPU player with the results of the previous round
        self.update_cpu_player_with_round_result()
        self.dealer.set_up_next_round()
        self.dealer.start_street()
    
    def player_action(self, action: str, raise_amount: Optional[int] = None):
        """
        function that will be called when its the players turn
        and they are active in the hand

        this receives the btn string from the GUI 
        """
        
        #convert string to Action enum
        action_enum = Action(action)
        self.dealer.apply_action(action_enum, raise_amount)

        # Save action histories for all players after the action
        for player in self.dealer.table.players:
            player.save_round_action_histories(self.dealer.current_street)

        # Send game update message to CPU if one is set
        if self.cpu_player is not None:
            new_action = {
                'player_name': "pc",  # Name for human player
                'action': action,
                'amount': raise_amount if raise_amount is not None else 0
            }
            round_state = self.build_round_state()
            self.cpu_player.receive_game_update_message(new_action, round_state)

        #after we apply the action need to check if the round is over so can do showdown logic
        #calling showdown will change player stack values
        if self.dealer.is_showdown():
            self.dealer.showdown()

        
    def cpu_action(self):
        """
        function that will be called when its the cpu's turn
        """
        # Build the round_state dictionary for the CPU
        round_state = self.build_round_state()
        
        # Get the current CPU player
        cpu_player = self.dealer.table.current_player
        
        # Check if there is a current player
        if cpu_player is None:
            return
        
        # Get the CPU's hole cards
        hole_cards = [str(card) for card in cpu_player.hole_cards]
        
        # Define valid actions (simplified for now)
        valid_actions = [
            {"action": "fold", "amount": 0},
            {"action": "call", "amount": self.dealer.betting_manager.current_bet - cpu_player.contribuition},
            {"action": "raise", "amount": {"min": self.dealer.betting_manager.current_bet * 2, "max": cpu_player.stack}}, 
            {"action": "check", "amount": 0}
        ]
        
        # Check if we have a CPU player set
        if self.cpu_player is not None:
            # Use the CPU player's declare_action method
            action, amount = self.cpu_player.declare_action(valid_actions, hole_cards, round_state)
        else:
            # Default behavior if no CPU player is set
            action = "call"
            amount = valid_actions[1]["amount"]
        
        # Convert string action to Action enum
        action_enum = Action(action)
        
        # Apply the action
        self.dealer.apply_action(action_enum, int(amount) if action == "raise" else None)
        
        # Save action histories for all players after the action
        for player in self.dealer.table.players:
            player.save_round_action_histories(self.dealer.current_street)
        
        # Send game update message to CPU if one is set
        if self.cpu_player is not None:
            new_action = {
                'player_name': cpu_player.name,  # Name for CPU player
                'action': action,
                'amount': amount if action == "raise" else 0
            }
            round_state = self.build_round_state()
            self.cpu_player.receive_game_update_message(new_action, round_state)
            
            # If the CPU folded, update its stack immediately
            if action == "fold":
                self.cpu_player.stack = self.dealer.table.players[1].stack
        
        #after we apply the action need to check if the round is over so can do showdown logic
        #calling showdown will change player stack values
        if self.dealer.is_showdown():
            self.dealer.showdown()

    def _is_game_over(self) -> bool:
        """
        check if the game is over (one of the players stack is 0)
        """
        #check if any of the players stack is 0 
        for player in self.dealer.table.players:
            if player.stack == 0:
                return True
        return False

    def update_cpu_player_with_round_result(self):
        """
        Update the CPU player with the results of a round.
        This should be called after a round is over and the pot has been distributed.
        """
        if self.cpu_player is None:
            return
            
        # Build the round_state dictionary
        round_state = self.build_round_state()
        
        # Get the winners
        winners = []
        for player in self.dealer.table.players:
            if player.state == PlayerState.WINNER:
                winners.append(player)
        
        # Create hand_info dictionary
        hand_info = {}
        for player in self.dealer.table.players:
            if player.state != PlayerState.FOLDED:
                hand_info[player.name] = {
                    "hand": [str(card) for card in player.hole_cards],
                    "hand_rank": "high_card"  # This would be determined by HandEvaluator in a real implementation
                }
        
        # Call the CPU's receive_round_result_message method
        self.cpu_player.receive_round_result_message(winners, hand_info, round_state)
        
        # Update the CPU's stack to match the player's stack
        self.cpu_player.stack = self.dealer.table.players[1].stack
