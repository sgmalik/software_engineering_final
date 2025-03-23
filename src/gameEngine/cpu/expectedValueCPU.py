from pypokerengine.players import BasePokerPlayer
from Deck import Deck
from enum import Enum
from Constants import Action
from Constants import PlayerState

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


class expectedValueCPU(BasePokerPlayer):
    def __init__(self, initial_stack):
        self.hole_cards = []
        self.stack = initial_stack
        self.state = PlayerState.ACTIVE
        self.contribuition = 0

    @staticmethod
    def count_outs(hole_cards, community_cards):
        """
        Calculate the number of outs for AI without using PyPokerEngine's evaluate_hand().
        """
        suits = {"S": 0, "H": 0, "D": 0, "C": 0}
        ranks = {str(i): 0 for i in range(2, 10)}  # Numeric ranks
        ranks.update({"T": 0, "J": 0, "Q": 0, "K": 0, "A": 0})  # Face cards

        # Convert hole & community cards into structured form
        all_cards = hole_cards + community_cards
        for card in all_cards:
            suits[card[0]] += 1  # Count suits
            ranks[card[1]] += 1  # Count ranks

        outs = 0  # Track number of outs

        # ---- FLUSH DRAW CHECK ----
        for suit, count in suits.items():
            if count == 4:  # 4 cards of the same suit present
                outs += 9  # 9 remaining suited cards

        # ---- STRAIGHT DRAW CHECK ----
        sorted_ranks = sorted(
            [
                int(
                    rank.replace("T", "10")
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

        # ---- OVERCARD IMPROVEMENT ----
        # If AI holds high cards (A-K, A-Q, etc.) but no pair, outs may exist.
        hole_ranks = [hole[1] for hole in hole_cards]
        max_hole_rank = max(
            [
                int(
                    r.replace("T", "10")
                    .replace("J", "11")
                    .replace("Q", "12")
                    .replace("K", "13")
                    .replace("A", "14")
                )
                for r in hole_ranks
            ]
        )

        # If no pair and AI holds high cards, assume 6 outs (3 for each overcard)
        if ranks[hole_ranks[0]] == 1 and ranks[hole_ranks[1]] == 1:
            outs += 6  # Overcards improving

        return outs

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
        outs = self.count_outs(hole_card, round_state["community_card"])
        equity = min(outs * 4, 100)  # max 100%

        # extract the pot size and call cost
        pot_size = round_state[
            "pot"
        ][
            "main"
        ]  # unsure if amount needed, will need to look at the structure of the pot in round_state
        call_action = next(a for a in valid_actions if a["action"] == "call")
        amount_to_call = call_action["amount"]

        # compute expected value for the given scanario
        ev = (equity * pot_size) - ((1 - equity) * amount_to_call)

        if ev > 0:
            # +EV should be raising their hand
            raise_action = next(
                (a for a in valid_actions if a["action"] == "raise"), None
            )
            if raise_action:
                return "raise", raise_action["amount"]["min"]
            else:
                return "call", call_action["amount"]
        else:
            return "fold", 0

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
