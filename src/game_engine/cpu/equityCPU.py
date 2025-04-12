from game_engine.constants import Action, PlayerState, Street
from pypokerengine.players import BasePokerPlayer
from game_engine.deck import Card
from typing import List, Union, Dict, Any, Optional

# assuming that round_state is a dictionary with the following structure:

# {
#     'street': 'preflop',  # Current phase (preflop, flop, turn, river)
#     'next_player': 1,  # Index of the next player to act
#     'small_blind_pos': 0,  # Position of small blind player
#     'big_blind_pos': 1,  # Position of big blind player
#     'community_card': ['H1', 'D5', 'C9'],  # Cards on the table
#     'pot': {
#         'main': 300,  # Total chips in the pot
#         'side': []  # Side pots (if applicable)
#     },
#     'seats': [
#         {
#             'name': 'Player1',
#             'uuid': 'player1-uuid',
#             'stack': 800,  # Chips left
#             'state': 'participating',  # 'participating', 'folded', 'allin'
#         },
#         {
#             'name': 'AI',
#             'uuid': 'ai-uuid',
#             'stack': 1200,
#             'state': 'participating'
#         }
#     ],
#     'action_histories': {
#         'preflop': [
#             {'uuid': 'player1-uuid', 'action': 'small_blind', 'amount': 10},
#             {'uuid': 'ai-uuid', 'action': 'big_blind', 'amount': 20},
#             {'uuid': 'player1-uuid', 'action': 'call', 'amount': 10},
#             {'uuid': 'ai-uuid', 'action': 'check', 'amount': 0}
#         ],
#         'flop': [],
#         'turn': [],
#         'river': []
#     }
# }

def parse_card_str(card_str: str) -> Card:
    """
    Helper function to parse card strings into Card objects.
    Card strings are in format like 'H2', 'DA', 'CK', etc.
    where first char is suit and second char is rank.
    Also handles 'H10' format for ten.
    """
    # Get suit and rank from the string
    if len(card_str) == 3:  # Handle 'H10' format
        suit = card_str[0].upper()  # 'H'
        rank = card_str[1:]  # '10'
    else:  # Handle 'H2' format
        suit = card_str[0].upper()
        rank = card_str[1]
        # Convert face cards to proper values
        if rank == 'A':
            rank = '14'
        elif rank == 'K':
            rank = '13'
        elif rank == 'Q':
            rank = '12'
        elif rank == 'J':
            rank = '11'
        elif rank == 'T':
            rank = '10'
    return Card(suit=suit, card_val=rank)

class equityCPU(BasePokerPlayer):
    """
    CPU that makes decisions based on calculating equity from counting outs
    """
    def __init__(self, initial_stack):
        self.hole_cards: List[Card] = []
        self.stack = initial_stack
        self.state = PlayerState.ACTIVE
        self.round_action_histories: List[Optional[List[Dict[str, Any]]]] = [None] * 4
        self.contribuition = 0
        self.action_histories: List[Dict[str, Any]] = []
        
        # Game state tracking
        self.game_info: Optional[Dict[str, Any]] = None
        self.name = "ai"  # Set name to "ai" for testing
        self.round_count = 0
        self.seats: List[Dict[str, Any]] = []
        self.street: Optional[str] = None
        self.community_cards: List[Card] = []
        self.opponent_actions: List[Dict[str, Any]] = []
        self.games_played = 0
        self.games_won = 0
    
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
            history = {"action": action}
        elif action == Action.CALL:
            pay_history = [
                h
                for h in self.action_histories
                if h["action"].value != Action.FOLD or h["action"].value != Action.ANTE
            ]
            last_pay = pay_history[-1] if len(pay_history) != 0 else None
            last_pay_amount = last_pay["paid"] if last_pay else 0
            history = {
                "action": action,
                "amount": chip_amount,
                "paid": chip_amount - last_pay_amount,
            }
        elif action == Action.RAISE:
            pay_history = [
                h
                for h in self.action_histories
                if h["action"].value != Action.FOLD or h["action"].value != Action.ANTE
            ]
            last_pay = pay_history[-1] if len(pay_history) != 0 else None
            last_pay_amount = last_pay["paid"] if last_pay else 0
            history = {
                "action": action,
                "amount": chip_amount,
                "paid": chip_amount - last_pay_amount,
                "add_amount": add_amount,
            }
        elif action == Action.SMALL_BLIND:
            assert sb_amount is not None
            add_amount = sb_amount
            history = {"action": action, "amount": sb_amount, "add_amount": add_amount}
        elif action == Action.BIG_BLIND:
            assert bb_amount is not None
            add_amount = bb_amount
            history = {"action": action, "amount": bb_amount, "add_amount": add_amount}
        elif action == Action.ANTE:
            assert chip_amount > 0 if chip_amount is not None else True
            history = {"action": action, "amount": chip_amount}
        self.action_histories.append(history)

    def save_round_action_histories(self, street: Street):
        self.round_action_histories[street.value] = self.action_histories
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

    def declare_action(self, valid_actions: List[Dict[str, Any]], hole_card: List[str], round_state: Dict[str, Any]) -> tuple[str, Union[int, float]]:
        """
        Declare action based on current game state and calculated equity.
        
        Args:
            valid_actions (list): List of valid action dictionaries
            hole_card (list): List of hole cards as strings
            round_state (dict): Current state of the round
            
        Returns:
            tuple: (action, amount)
        """
        # Convert hole cards from strings
        hole_cards = [parse_card_str(card_str) for card_str in hole_card]
            
        # Convert community cards from strings
        community_cards = [parse_card_str(card_str) for card_str in round_state['community_card']]
        
        # Calculate equity based on outs
        equity = self.count_outs(hole_cards, community_cards) * 4  # Each out is roughly 4% equity
        equity = min(equity, 100)  # Cap at 100%
        
        # Get the current pot and call amount
        pot = round_state['pot']['main']
        call_amount = valid_actions[1]['amount']  # Index 1 is always call
        
        # Decision making based on equity
        if equity > 50:  # Strong hand
            # Try to raise if possible
            if len(valid_actions) > 2:  # Raise is available
                raise_action = valid_actions[2]
                min_raise = raise_action['amount']['min']
                max_raise = min(raise_action['amount']['max'], self.stack)
                raise_amount = min(max_raise, min_raise * 2)  # Raise 2x minimum
                return 'raise', raise_amount
            return 'call', call_amount
        elif equity > 25:  # Medium hand
            return 'call', call_amount
        else:  # Weak hand
            return 'fold', 0

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
        if new_action['player_name'] != self.name:
            self.opponent_actions.append(new_action)
        
        # Update community cards
        self.community_cards = [parse_card_str(card_str) for card_str in round_state['community_card']]

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
