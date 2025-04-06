"""
tests for hand_evaluator module
"""
from ..card import Card
from ..hand_evaluator import HandEvaluator


class TestHandEval():

    """
    will test each hand strength
    """

    def test_highcard(self):
        """
        simple high card test
        """
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
            "hand_rank": 1,
            "primary_cards_rank": high_card_hand,
            "kickers": []
        }

        hand_info = HandEvaluator.hand_eval(hole_cards, community_cards)

        assert hand_info == expected_info
