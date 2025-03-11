from ..Deck import Deck
from ..Card import Card
from Hand_Evaluator import HandEvaluator

# python -m pytest


class Test_HandEval():

    # test when hand is high card
    def test_highcard(self):
        hole_cards = [
            Card('H', '2'),
            Card('D', '5'),
        ]

        community_cards = [
            Card('S', '9'),
            Card('C', 'J'),
            Card('H', 'Q'),
            Card('S', '3'),
            Card('D', '7'),
        ]

        high_card_hand = [
            Card('H', 'Q'),
            Card('C', 'J'),
            Card('S', '9'),
            Card('D', '7'),
            Card('D', '5'),
        ]
        
        expected_info = {
            "strength": {
                "hand_rank": 1,
                "primary_cards_rank": high_card_hand
            },
            "kickers": []
        }

        hand_info = HandEvaluator.hand_eval(hole_cards, community_cards)
        

        assert(hand_info == expected_info)



