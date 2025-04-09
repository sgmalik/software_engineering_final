"""
tests for hand_evaluator module
"""
import pytest
from ..card import Card
from ..hand_evaluator import HandEvaluator


class TestHandEval():

    """
    will test each hand strength
    """
    test_cases = [
        (
            [Card('H', '2'), Card('D', '5')],
            [Card('S', '9'), Card('C', 'J'), Card('H', 'Q'), Card('S', '3'), Card('D', '7')],
            {
            "hand_rank": 1,
            "primary_cards_rank": [
                Card('H', 'Q'),
                Card('S', 'J'),
                Card('S', '9'),
                Card('D', '7'),
                Card('H', '5')
            ],
            "kickers": []
            },
            "high card"
        ),
          (
            [Card('H', '2'), Card('D', '5')],
            [Card('S', '9'), Card('C', '5'), Card('H', 'Q'), Card('S', '3'), Card('D', '7')],
            {
            "hand_rank": 2,
            "primary_cards_rank": [
                Card('D', '5'),
                Card('C', '5'),
            ],
            "kickers": [
                Card('H', 'Q'),
                Card('S', '9'),
                Card('D', '7'),
            ]
            },
            "pair"
        ),
        (
            [Card('H', '2'), Card('D', '5')],
            [Card('S', '9'), Card('C', '5'), Card('H', 'Q'), Card('S', '2'), Card('D', '7')],
            {
            "hand_rank": 3,
            "primary_cards_rank": [
                Card('D', '5'),
                Card('C', '5'),
                Card('H', '2'),
                Card('S', '2'),
            ],
            "kickers": [
               Card('H', 'Q')
            ]
            },
            "two pair"
        ),
         (
            [Card('H', '2'), Card('D', '5')],
            [Card('S', '5'), Card('C', '5'), Card('H', 'Q'), Card('S', '3'), Card('D', '7')],
            {
            "hand_rank": 4,
            "primary_cards_rank": [
                Card('D', '5'),
                Card('C', '5'),
                Card('S', '5'),
            ],
            "kickers": [
               Card('H', 'Q'),
               Card('D', '7'),
            ]
            },
            "three of a kind"
        ),
         (
            [Card('H', '2'), Card('D', '3')],
            [Card('S', '4'), Card('C', '5'), Card('H', '6'), Card('S', '2'), Card('D', '7')],
            {
            "hand_rank": 5,
            "primary_cards_rank": [
                Card('D', '7'),
                Card('H', '6'),
                Card('C', '5'),
                Card('S', '4'),
                Card('D', '3'),
            ],
            "kickers": [
            ]
            },
            "straight"
        ),
        (
            [Card('C', '2'), Card('C', '3')],
            [Card('S', '4'), Card('C', '5'), Card('C', '6'), Card('S', '2'), Card('C', '7')],
            {
            "hand_rank": 5,
            "primary_cards_rank": [
                Card('C', '7'),
                Card('C', '6'),
                Card('C', '5'),
                Card('C', '3'),
                Card('C', '2'),
            ],
            "kickers": [
            ]
            },
            "flush"
        ),
        (
            [Card('H', '2'), Card('D', '5')],
            [Card('S', '4'), Card('C', '5'), Card('H', '6'), Card('S', '5'), Card('D', '2')],
            {
            "hand_rank": 5,
            "primary_cards_rank": [
                Card('D', '5'),
                Card('S', '5'),
                Card('C', '5'),
                Card('H', '2'),
                Card('D', '2'),
            ],
            "kickers": [
            ]
            },
            "full house"
        ),
        (
            [Card('H', '2'), Card('D', '3')],
            [Card('S', '4'), Card('C', '5'), Card('H', '6'), Card('S', '2'), Card('D', '7')],
            {
            "hand_rank": 5,
            "primary_cards_rank": [
                Card('D', '7'),
                Card('H', '6'),
                Card('C', '5'),
                Card('S', '4'),
                Card('D', '3'),
            ],
            "kickers": [
               Card('H', '2')
            ]
            },
            "four of a kind"
        )
        
    ]

    def _change_to_ranks(self, hand_info):
        """
        change card objects to their ranks for testing
        """
        return {
            "hand_rank": hand_info["hand_rank"],
            "primary_cards_rank": [card.get_card_rank() for card in hand_info["primary_cards_rank"]],
            "kickers": [card.get_card_rank() for card in hand_info["kickers"]],
        }
        

    @pytest.mark.parametrize("hole_cards, community_cards, expected_info, id", test_cases, 
                              ids=[i[3] for i in test_cases])
    def test_hand_eval(self, hole_cards, community_cards, expected_info, id):
        """
        test hand eval function
        """
        hand_info = HandEvaluator.hand_eval(hole_cards, community_cards)

        hand_eval_rtn = self._change_to_ranks(hand_info)
        expected_info = self._change_to_ranks(expected_info)

        assert hand_eval_rtn["hand_rank"] == expected_info["hand_rank"]
        assert hand_eval_rtn["primary_cards_rank"] == expected_info["primary_cards_rank"]
        assert hand_eval_rtn["kickers"] == expected_info["kickers"]
        

       