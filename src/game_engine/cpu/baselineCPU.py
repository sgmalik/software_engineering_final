from pypokerengine.players import BasePokerPlayer
from game_engine.deck import Deck
from enum import Enum
from game_engine.constants import Action, PlayerState

# assunuing that round_state is a dictionary with the following structure:

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


class baselineCPU(BasePokerPlayer):
    def __init__(self, initial_stack):
        self.hole_cards = []
        self.stack = initial_stack
        self.state = PlayerState.ACTIVE
        self.contribuition = 0

    def clear_hole_cards(self):
        self.hole_cards = []

    def fold(self):
        self.state = PlayerState.FOLDED

    def add_to_stack(self, amount):
        self.stack += amount

    def bet(self, amount):
        self.stack -= amount
        self.contribuition += amount

    def declare_action(self, valid_actions, hole_card, round_state):
        pass

    def receive_game_start_message(self, game_info):
        pass

    def receive_round_start_message(self, round_count, hole_card, seats):
        pass

    def receuve_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, new_action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass
