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
    Card strings are in format like 'As', 'Kh', '2d', etc.
    where first char is rank and second char is suit.
    Also handles '10s' format for ten.
    """
    # Get rank and suit from the string
    if len(card_str) == 3:  # Handle '10s' format
        rank = card_str[:-1]  # '10'
        suit = card_str[-1].upper()  # 'S'
    else:  # Handle 'Ts' format
        rank = '10' if card_str[0] == 'T' else card_str[0]
        suit = card_str[1].upper()
    return Card(suit, rank)

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
        self.uuid: Optional[str] = None
        self.name = self.__class__.__name__
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
        Calculate the number of outs for AI without using PyPokerEngine's evaluate_hand().
        """
        suits = {"S": 0, "H": 0, "D": 0, "C": 0}
        ranks = {str(i): 0 for i in range(2, 10)}  # Numeric ranks
        ranks.update({"10": 0, "J": 0, "Q": 0, "K": 0, "A": 0})  # Face cards

        # Convert hole & community cards into structured form
        all_cards = hole_cards + community_cards
        for card in all_cards:
            suits[card.suit] += 1  # Count suits
            ranks[card.card_val] += 1  # Count ranks

        outs = 0  # Track number of outs

        # ---- FLUSH DRAW CHECK ----
        for suit, count in suits.items():
            if count == 4:  # 4 cards of the same suit present
                outs += 9  # 9 remaining suited cards

        # ---- STRAIGHT DRAW CHECK ----
        sorted_ranks = sorted(
            [
                int(
                    rank.replace("10", "10")
                    .replace("J", "11")
                    .replace("Q", "12")
                    .replace("K", "13")
                    .replace("A", "14")
                )
                for rank, count in ranks.items()
                if count > 0
            ]
        )

        # Open-ended straight draw (e.g., 5-6-7-8 needs a 4 or 9)
        for i in range(len(sorted_ranks) - 3):
            if sorted_ranks[i + 3] - sorted_ranks[i] == 3:  # Consecutive
                outs += 8  # 4 cards on each side

        # Gutshot straight draw (e.g., 5-6-8-9 needs a 7)
        for i in range(len(sorted_ranks) - 2):
            if (
                sorted_ranks[i + 2] - sorted_ranks[i] == 2
                and sorted_ranks[i + 1] - sorted_ranks[i] > 1
            ):
                outs += 4  # Only 1 missing rank

        # ---- PAIR TO TRIPS / SET TO FULL HOUSE ----
        for rank, count in ranks.items():
            if count == 2:  # AI has a pair
                outs += 2  # 2 more cards in the deck to make trips
            elif count == 3:  # AI has trips
                outs += 3  # 3 more cards to make a full house

        # ---- CARD IMPROVEMENT ----
        # if AI has no pair, add 6 outs for each overcard
        if ranks[hole_cards[0].card_val] == 1 and ranks[hole_cards[1].card_val] == 1:
            outs += 6
        return min(outs, 15)  # Cap at 15 outs

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
        
        # Find our seat and set UUID
        for seat in game_info['seats']:
            if seat['name'] == self.name:
                self.uuid = seat['uuid']
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
        if new_action['player_uuid'] != self.uuid:
            self.opponent_actions.append(new_action)
        
        # Update community cards
        self.community_cards = [parse_card_str(card_str) for card_str in round_state['community_card']]

    def receive_round_result_message(self, winners: List[Dict[str, Any]], hand_info: Dict[str, Any], round_state: Dict[str, Any]) -> None:
        """
        Called at the end of each round with results.
        """
        self.games_played += 1
        
        # Check if we won
        for winner in winners:
            if winner['uuid'] == self.uuid:
                self.games_won += 1
                break
        
        # Update our stack size
        for seat in round_state['seats']:
            if seat['uuid'] == self.uuid:
                self.stack = seat['stack']
                break
