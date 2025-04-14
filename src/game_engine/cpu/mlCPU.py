from pypokerengine.players import BasePokerPlayer
from game_engine.deck import Card
from game_engine.constants import Action, PlayerState, Street
from typing import List, Union, Dict, Any, Optional, cast
import numpy as np
import pickle
import os
import random
from collections import defaultdict

def parse_card_str(card_str: str) -> Card:
    """
    Helper function to parse card strings into Card objects.
    Card strings are in format like '2H', 'AD', 'KC', etc.
    where first char is rank and second char is suit.
    Also handles '10H' format for ten.
    """
    # Get suit and rank from the string
    if len(card_str) == 3:  # Handle '10H' format
        suit = card_str[2].upper()  # 'H'
        rank = card_str[0:2]  # '10'
    else:  # Handle '2H' format
        suit = card_str[1].upper()
        rank = card_str[0]
    
    return Card(suit=suit, card_val=rank)

class MLCPU(BasePokerPlayer):
    """
    CPU that uses reinforcement learning to improve its poker strategy over time.
    Implements Q-learning to learn optimal actions in different game states.
    """
    def __init__(self, initial_stack, model_path=None, learning_rate=0.1, discount_factor=0.95, epsilon=0.1):
        self.hole_cards: List[Card] = []
        self.stack = initial_stack
        self.state = PlayerState.ACTIVE
        self.round_action_histories: List[Optional[List[Dict[str, Any]]]] = [None] * 4
        self.contribuition = 0
        self.action_histories: List[Dict[str, Any]] = []
        
        # Game state tracking
        self.game_info: Optional[Dict[str, Any]] = None
        self.name = "ml_cpu"
        self.round_count = 0
        self.seats: List[Dict[str, Any]] = []
        self.street: Optional[str] = None
        self.community_cards: List[Card] = []
        self.opponent_actions: List[Dict[str, Any]] = []
        
        # ML parameters
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon  # Exploration rate
        self.model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "models", "ml_cpu_model.pkl")
        
        # Q-table: maps state-action pairs to Q-values
        self.q_table = defaultdict(lambda: defaultdict(float))
        
        # Load pre-trained model if available
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
        
        # Track current state and action for updating Q-values
        self.current_state = None
        self.current_action = None
        
        # Track game history for training
        self.game_history = []
        self.current_round_history = []
    
    def add_hole_card(self, cards: List[Card]):
        if len(self.hole_cards) != 0:
            raise ValueError("Player already has hold cards")
        if len(cards) != 2:
            raise ValueError("Player can osnly have 2 hole cards")
        if not all(isinstance(card, Card) for card in cards):
            raise ValueError("Player can only have cards as hole cards")
        self.hole_cards = cards

    def clear_hole_cards(self):
        self.hole_cards = []

    def add_to_stack(self, amount):
        self.stack += amount
    
    def collect_bet(self, amount: float | int):
        if self.stack < amount:
            raise ValueError("Player cannot afford this bet")
        self.stack -= amount
        self.contribuition += amount

    def reset_contribuition(self):
        self.contribuition = 0

    def is_active(self):
        return self.state == PlayerState.ACTIVE

    def is_folded(self):
        return self.state == PlayerState.FOLDED

    def is_allin(self):
        return self.state == PlayerState.ALLIN

    def is_waiting(self):
        return self.state == PlayerState.WAITING

    def is_winner(self):
        return self.state == PlayerState.WINNER
    
    def add_action_history(
        self,
        action: Action,
        chip_amount: Union[int, float] = 0,
        add_amount: Union[int, float] = 0,
        sb_amount: Union[int, float] = 0,
        bb_amount: Union[int, float] = 0,
    ):
        """
        add action to player's action history
        """
        history = None
        if action == Action.FOLD:
            history = {"action": action, "name": self.name, "stack": self.stack}
        elif action == Action.CALL:
            pay_history = [
                h
                for h in self.action_histories
                if h["action"] != Action.FOLD and h["action"] != Action.ANTE
            ]
            last_pay = pay_history[-1] if len(pay_history) != 0 else None
            last_pay_amount = last_pay.get("paid", 0) if last_pay else 0
            history = {
                "name": self.name,
                "action": action,
                "amount": chip_amount,
                "paid": chip_amount - last_pay_amount,
                "stack": self.stack
            }
        elif action == Action.RAISE:
            pay_history = [
                h
                for h in self.action_histories
                if h["action"] != Action.FOLD and h["action"] != Action.ANTE
            ]
            last_pay = pay_history[-1] if len(pay_history) != 0 else None
            last_pay_amount = last_pay.get("paid", 0) if last_pay else 0
            history = {
                "name": self.name,
                "action": action,
                "amount": chip_amount,
                "paid": chip_amount - last_pay_amount,
                "add_amount": add_amount,
                "stack": self.stack
            }
        elif action == Action.SMALL_BLIND:
            assert sb_amount is not None
            add_amount = sb_amount
            history = {
                "action": action,
                "amount": sb_amount,
                "add_amount": add_amount,
                "name": self.name,
                "paid": sb_amount,
                "stack": self.stack
            }
        elif action == Action.BIG_BLIND:
            assert bb_amount is not None
            add_amount = bb_amount
            history = {
                "action": action,
                "amount": bb_amount,
                "add_amount": add_amount,
                "name": self.name,
                "paid": bb_amount,
                "stack": self.stack
            }
        elif action == Action.CHECK:
            history = {
                "action": action,
                "name": self.name,
                "stack": self.stack
            }

        if history is not None:
            self.action_histories.append(history)
            # Add to current round history for training
            self.current_round_history.append({
                "state": self.current_state,
                "action": self.current_action,
                "reward": 0  # Will be updated at the end of the round
            })

    def save_round_action_histories(self, street: Street):
        """
        Save the current action histories to the round action histories for the given street.
        If there are already histories for this street, append to them instead of overwriting.
        """
        if self.round_action_histories[street.value] is None:
            self.round_action_histories[street.value] = []
        
        histories = cast(List[dict], self.round_action_histories[street.value])
        histories.extend(self.action_histories)
        self.action_histories = []

    def clear_action_histories(self):
        self.round_action_histories = [None for _ in range(4)]
        self.action_histories = []

    @staticmethod
    def count_outs(hole_cards, community_cards):
        """
        Count the number of outs for the current hand.
        """
        # Initialize counters for suits and ranks
        suits = {'H': 0, 'D': 0, 'C': 0, 'S': 0}
        ranks = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0}
        
        # Count occurrences of each suit and rank
        for card in hole_cards:
            suits[card.suit] += 1
            rank = int(card.card_val) if card.card_val.isdigit() else {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}[card.card_val]
            ranks[rank] += 1
            
        for card in community_cards:
            suits[card.suit] += 1
            rank = int(card.card_val) if card.card_val.isdigit() else {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}[card.card_val]
            ranks[rank] += 1
            
        # Check for flush draw
        flush_outs = 0
        for suit, count in suits.items():
            if count == 4:
                flush_outs = 9  # 9 cards of the same suit remaining
                
        # Check for straight draw
        straight_outs = 0
        for i in range(2, 11):
            if ranks[i] > 0 and ranks[i+1] > 0 and ranks[i+2] > 0 and ranks[i+3] > 0:
                straight_outs = 8  # 8 cards to complete the straight
                
        # Check for overcards
        overcard_outs = 0
        if len(hole_cards) == 2:
            hole_ranks = [int(card.card_val) if card.card_val.isdigit() else {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}[card.card_val] for card in hole_cards]
            max_hole_rank = max(hole_ranks)
            for rank in range(max_hole_rank + 1, 15):
                if ranks[rank] == 0:
                    overcard_outs += 1
                    
        # Return total outs
        return flush_outs + straight_outs + overcard_outs
    
    def extract_features(self, hole_cards, community_cards, pot, call_amount, round_state):
        """
        Extract numerical features from the current game state.
        Returns a tuple that can be used as a key in the Q-table.
        """
        # Count outs as a measure of hand strength
        outs = self.count_outs(hole_cards, community_cards)
        
        # Calculate pot odds
        # Handle case where call_amount is a dictionary with min and max values
        if isinstance(call_amount, dict) and 'min' in call_amount:
            call_amount = call_amount['min']  # Use minimum call amount for pot odds calculation
        
        pot_odds = call_amount / (pot + call_amount) if pot + call_amount > 0 else 0
        
        # Calculate position (0 = small blind, 1 = big blind)
        position = 0
        if round_state.get('small_blind_pos') == 1:  # We're small blind
            position = 0
        elif round_state.get('big_blind_pos') == 1:  # We're big blind
            position = 1
            
        # Calculate street (0 = preflop, 1 = flop, 2 = turn, 3 = river)
        street_map = {'preflop': 0, 'flop': 1, 'turn': 2, 'river': 3}
        street = street_map.get(round_state.get('street', 'preflop'), 0)
        
        # Calculate stack to pot ratio
        stack_to_pot = self.stack / (pot + 1)  # Add 1 to avoid division by zero
        
        # Calculate opponent aggression (ratio of raises to calls)
        opponent_aggression = 0
        if self.opponent_actions:
            raises = sum(1 for action in self.opponent_actions if action.get('action') == 'raise')
            calls = sum(1 for action in self.opponent_actions if action.get('action') == 'call')
            opponent_aggression = raises / (calls + 1)  # Add 1 to avoid division by zero
            
        # Discretize continuous values to reduce state space
        outs_bucket = min(outs // 2, 10)  # 0-20 outs, bucketed into 11 categories
        pot_odds_bucket = int(pot_odds * 10)  # 0-1 pot odds, bucketed into 10 categories
        stack_to_pot_bucket = min(int(stack_to_pot), 10)  # 0-10+ stack to pot ratio
        aggression_bucket = min(int(opponent_aggression * 2), 5)  # 0-2.5+ aggression, bucketed into 6 categories
        
        # Return a tuple of discretized features
        return (outs_bucket, pot_odds_bucket, position, street, stack_to_pot_bucket, aggression_bucket)
    
    def get_action_from_q_table(self, state, valid_actions):
        """
        Get the best action from the Q-table based on the current state.
        Uses epsilon-greedy strategy for exploration.
        """
        # Epsilon-greedy strategy
        if random.random() < self.epsilon:
            # Explore: choose a random action
            action_idx = random.randint(0, len(valid_actions) - 1)
            action = valid_actions[action_idx]['action']
            amount = valid_actions[action_idx].get('amount', 0)
            if isinstance(amount, dict):  # For raise actions
                amount = amount.get('min', 0)
            return action, amount
        
        # Exploit: choose the action with the highest Q-value
        best_action_idx = 0
        best_q_value = float('-inf')
        
        for i, action_dict in enumerate(valid_actions):
            action = action_dict['action']
            amount = action_dict.get('amount', 0)
            if isinstance(amount, dict):  # For raise actions
                amount = amount.get('min', 0)
                
            q_value = self.q_table[state][(action, amount)]
            if q_value > best_q_value:
                best_q_value = q_value
                best_action_idx = i
                
        action = valid_actions[best_action_idx]['action']
        amount = valid_actions[best_action_idx].get('amount', 0)
        if isinstance(amount, dict):  # For raise actions
            amount = amount.get('min', 0)
            
        return action, amount
    
    def update_q_value(self, state, action, reward, next_state):
        """
        Update the Q-value for the state-action pair using the Q-learning update rule.
        """
        # Get the maximum Q-value for the next state
        next_max_q = max(self.q_table[next_state].values()) if self.q_table[next_state] else 0
        
        # Q-learning update rule
        current_q = self.q_table[state][action]
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * next_max_q - current_q)
        self.q_table[state][action] = new_q
    
    def calculate_reward(self, round_result, hand_info):
        """
        Calculate the reward for the current round based on the outcome.
        """
        # Check if we won
        won = False
        for winner in round_result:
            if isinstance(winner, dict) and winner.get('name') == self.name:
                won = True
                break
                
        # Calculate reward based on stack change
        initial_stack = self.stack - self.contribuition
        stack_change = self.stack - initial_stack
        
        # Base reward is the stack change
        reward = stack_change
        
        # Add bonus for winning
        if won:
            reward += 10
            
        # Add penalty for folding with a strong hand
        if self.state == PlayerState.FOLDED and self.count_outs(self.hole_cards, self.community_cards) > 10:
            reward -= 5
            
        return reward
    
    def declare_action(self, valid_actions: List[Dict[str, Any]], hole_card: List[str], round_state: Dict[str, Any]) -> tuple[str, Union[int, float]]:
        """
        Declare action based on Q-learning.
        """
        # Convert hole cards from strings
        hole_cards = [parse_card_str(card_str) for card_str in hole_card]
            
        # Convert community cards from strings
        community_cards = [parse_card_str(card_str) for card_str in round_state['community_card']]
        
        # Get the current pot and call amount
        pot = round_state['pot']['main']
        call_amount = valid_actions[1]['amount']  # Index 1 is always call
        
        # Extract features from the current state
        state = self.extract_features(hole_cards, community_cards, pot, call_amount, round_state)
        self.current_state = state
        
        # Get the best action from the Q-table
        action, amount = self.get_action_from_q_table(state, valid_actions)
        self.current_action = (action, amount)
        
        return action, amount

    def receive_game_start_message(self, game_info: Dict[str, Any]) -> None:
        """
        Called when a new game begins. Store initial game settings.
        """
        self.game_info = game_info
        self.stack = game_info['rule']['initial_stack']
        
        # Find our seat
        for seat in game_info['seats']:
            if seat['name'] == self.name:
                break
                
        # Reset game history
        self.game_history = []

    def receive_round_start_message(self, round_count: int, hole_card: List[str], seats: List[Dict[str, Any]]) -> None:
        """
        Called at the beginning of each round.
        """
        self.round_count = round_count
        self.hole_cards = [parse_card_str(card_str) for card_str in hole_card]
        self.seats = seats
        self.community_cards = []
        self.opponent_actions = []
        
        # Reset action histories for new round
        self.round_action_histories = [None] * 4
        self.action_histories = []
        
        # Reset current round history
        self.current_round_history = []

    def receive_street_start_message(self, street: str, round_state: Dict[str, Any]) -> None:
        """
        Called at the start of each street.
        """
        self.street = street
        self.community_cards = [parse_card_str(card_str) for card_str in round_state['community_card']]
        
        # Save action histories for the previous street if any
        if street == 'preflop':
            street_index = 0
        elif street == 'flop':
            street_index = 1
        elif street == 'turn':
            street_index = 2
        elif street == 'river':
            street_index = 3
        else:
            return
            
        if self.action_histories:
            self.round_action_histories[street_index-1] = self.action_histories
            self.action_histories = []

    def receive_game_update_message(self, new_action: Dict[str, Any], round_state: Dict[str, Any]) -> None:
        """
        Called after any player takes an action.
        """
        # Track opponent actions
        if new_action.get('player_name') != self.name:
            self.opponent_actions.append(new_action)
        
        # Update community cards
        self.community_cards = [parse_card_str(card_str) for card_str in round_state['community_card']]
        
        # Update Q-values for the previous state-action pair if we have one
        if self.current_state and self.current_action:
            # Extract features for the new state
            hole_cards = self.hole_cards
            community_cards = self.community_cards
            pot = round_state['pot']['main']
            call_amount = 0  # We don't know the call amount yet
            
            next_state = self.extract_features(hole_cards, community_cards, pot, call_amount, round_state)
            
            # Calculate immediate reward (0 for intermediate actions)
            reward = 0
            
            # Update Q-value
            self.update_q_value(self.current_state, self.current_action, reward, next_state)

    def receive_round_result_message(self, winners: List[Dict[str, Any]], hand_info: Dict[str, Any], round_state: Dict[str, Any]) -> None:
        """
        Called when the round is over and winners are determined.
        """
        # Check if we won
        for winner in winners:
            if isinstance(winner, dict) and winner.get('name') == self.name:
                self.state = PlayerState.WINNER
                break

        # Update stack sizes
        for seat in round_state['seats']:
            if seat.get('name') == self.name:
                self.stack = seat['stack']
                break
                
        # Calculate reward for the round
        reward = self.calculate_reward(winners, hand_info)
        
        # Update Q-values for all state-action pairs in the round
        for i, history in enumerate(self.current_round_history):
            state = history['state']
            action = history['action']
            
            # For the last action, use the final reward
            # For earlier actions, use a discounted reward
            if i == len(self.current_round_history) - 1:
                final_reward = reward
            else:
                # Use a small negative reward for intermediate actions to encourage efficiency
                final_reward = -0.1
                
            # Extract features for the next state (use the next state in history or a dummy state)
            if i < len(self.current_round_history) - 1:
                next_state = self.current_round_history[i + 1]['state']
            else:
                # For the last action, use a dummy terminal state
                next_state = (-1, -1, -1, -1, -1, -1)
                
            # Update Q-value
            self.update_q_value(state, action, final_reward, next_state)
            
        # Add the round history to the game history
        self.game_history.append(self.current_round_history)
        
        # Save the model periodically
        if self.model_path and len(self.game_history) % 10 == 0:
            self.save_model(self.model_path)
    
    def save_model(self, path):
        """
        Save the Q-table to a file.
        """
        # Ensure the directory exists
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, 'wb') as f:
            pickle.dump(dict(self.q_table), f)
            
    def load_model(self, path):
        """
        Load the Q-table from a file.
        """
        with open(path, 'rb') as f:
            q_table_dict = pickle.load(f)
            self.q_table = defaultdict(lambda: defaultdict(float), q_table_dict) 
            
    def train_model(self, num_rounds=100, opponent_strategy="random"):
        """
        Train the model by simulating multiple rounds of poker.
        
        Args:
            num_rounds: Number of rounds to simulate for training
            opponent_strategy: Strategy for the opponent ("random", "aggressive", "passive")
            
        Returns:
            The trained model
        """
        print(f"Training MLCPU model for {num_rounds} rounds...")
        
        # Save original state
        original_stack = self.stack
        original_epsilon = self.epsilon
        
        # Increase exploration during training
        self.epsilon = 0.3
        
        # Create a simulated opponent
        from game_engine.cpu.baselineCPU import baselineCPU
        opponent = baselineCPU(original_stack)
        
        # Simulate rounds
        completed_rounds = 0
        for round_num in range(num_rounds):
            # Reset for new round
            self.stack = original_stack
            opponent.stack = original_stack
            self.hole_cards = []
            opponent.hole_cards = []
            self.community_cards = []
            self.opponent_actions = []
            self.current_round_history = []
            
            # Deal hole cards
            from game_engine.deck import Deck
            deck = Deck()
            self.hole_cards = deck.draw_cards(2)
            opponent.hole_cards = deck.draw_cards(2)
            
            # Simulate each street
            streets = ["preflop", "flop", "turn", "river"]
            pot = 0
            
            for street in streets:
                # Create round state
                round_state = {
                    "street": street,
                    "small_blind_pos": 0,
                    "big_blind_pos": 1,
                    "community_card": [str(card) for card in self.community_cards],
                    "pot": {"main": pot},
                    "seats": [
                        {"name": "player", "stack": 1000, "state": "participating"},
                        {"name": self.name, "stack": self.stack, "state": "participating"}
                    ]
                }
                
                # Deal community cards based on street
                if street == "flop":
                    self.community_cards.extend(deck.draw_cards(3))
                elif street in ["turn", "river"]:
                    self.community_cards.extend(deck.draw_cards(1))
                
                # Update round state with new community cards
                round_state["community_card"] = [str(card) for card in self.community_cards]
                
                # Simulate betting rounds
                valid_actions = [
                    {"action": "fold", "amount": 0},
                    {"action": "call", "amount": 10},
                    {"action": "raise", "amount": {"min": 20, "max": self.stack}},
                    {"action": "check", "amount": 0}
                ]
                
                # CPU acts
                action, amount = self.declare_action(valid_actions, [str(card) for card in self.hole_cards], round_state)
                
                # Record action in history
                self.current_round_history.append({
                    "state": self.current_state,
                    "action": self.current_action,
                    "reward": 0  # Will be updated at the end of the round
                })
                
                # Opponent acts based on strategy
                opponent_action = "call"
                opponent_amount = 10
                
                if opponent_strategy == "random":
                    opponent_action = random.choice(["fold", "call", "raise"])
                    if opponent_action == "raise":
                        opponent_amount = random.randint(20, min(100, opponent.stack))
                elif opponent_strategy == "aggressive":
                    if random.random() < 0.7:  # 70% chance to raise
                        opponent_action = "raise"
                        opponent_amount = random.randint(20, min(100, opponent.stack))
                elif opponent_strategy == "passive":
                    if random.random() < 0.7:  # 70% chance to call
                        opponent_action = "call"
                    else:
                        opponent_action = "fold"
                
                # Update pot and stacks based on actions
                if action == "fold":
                    self.state = PlayerState.FOLDED
                elif action == "call":
                    self.collect_bet(amount)
                    pot += amount
                elif action == "raise":
                    self.collect_bet(amount)
                    pot += amount
                
                if opponent_action == "fold":
                    opponent.state = PlayerState.FOLDED
                elif opponent_action == "call":
                    opponent.collect_bet(opponent_amount)
                    pot += opponent_amount
                elif opponent_action == "raise":
                    opponent.collect_bet(opponent_amount)
                    pot += opponent_amount
                
                # Record opponent action
                self.opponent_actions.append({
                    "player_name": "player",
                    "action": opponent_action,
                    "amount": opponent_amount
                })
                
                # Check if round is over (someone folded)
                if self.state == PlayerState.FOLDED or opponent.state == PlayerState.FOLDED:
                    break
            
            # Determine winner and update Q-values
            if self.state == PlayerState.FOLDED:
                # Opponent won
                opponent.add_to_stack(pot)
                self.state = PlayerState.ACTIVE  # Reset state
                reward = -pot
            elif opponent.state == PlayerState.FOLDED:
                # CPU won
                self.add_to_stack(pot)
                self.state = PlayerState.ACTIVE  # Reset state
                reward = pot
            else:
                # Showdown - evaluate hands
                from game_engine.hand_evaluator import HandEvaluator
                cpu_hand = HandEvaluator.hand_eval(self.hole_cards, self.community_cards)
                opponent_hand = HandEvaluator.hand_eval(opponent.hole_cards, self.community_cards)
                
                if cpu_hand["hand_rank"] > opponent_hand["hand_rank"]:
                    # CPU won
                    self.add_to_stack(pot)
                    reward = pot
                elif cpu_hand["hand_rank"] < opponent_hand["hand_rank"]:
                    # Opponent won
                    opponent.add_to_stack(pot)
                    reward = -pot
                else:
                    # Split pot
                    self.add_to_stack(pot // 2)
                    opponent.add_to_stack(pot // 2)
                    reward = 0
            
            # Update Q-values for all state-action pairs in the round
            for i, history in enumerate(self.current_round_history):
                state = history['state']
                action = history['action']
                
                # For the last action, use the final reward
                # For earlier actions, use a discounted reward
                if i == len(self.current_round_history) - 1:
                    final_reward = reward
                else:
                    # Use a small negative reward for intermediate actions to encourage efficiency
                    final_reward = -0.1
                    
                # Extract features for the next state (use the next state in history or a dummy state)
                if i < len(self.current_round_history) - 1:
                    next_state = self.current_round_history[i + 1]['state']
                else:
                    # For the last action, use a dummy terminal state
                    next_state = (-1, -1, -1, -1, -1, -1)
                    
                # Update Q-value
                self.update_q_value(state, action, final_reward, next_state)
            
            # Add the round history to the game history
            self.game_history.append(self.current_round_history)
            
            # Increment completed rounds counter
            completed_rounds += 1
            
            # Save the model periodically
            if self.model_path and completed_rounds % 10 == 0:
                self.save_model(self.model_path)
                
            # Print progress
            if completed_rounds % 10 == 0 or completed_rounds == num_rounds:
                print(f"Completed {completed_rounds} training rounds")
        
        # Restore original epsilon
        self.epsilon = original_epsilon
        
        # Save the final model
        if self.model_path:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(os.path.abspath(self.model_path)), exist_ok=True)
            print(f"Saving model to {self.model_path}")
            self.save_model(self.model_path)
            print(f"Model saved to {self.model_path}")
            
        print(f"Training complete. Completed {completed_rounds} rounds.")
        return self 
